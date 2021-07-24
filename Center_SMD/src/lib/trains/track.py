from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import torch
import numpy as np
import time
from progress.bar import Bar
from utils.utils import AverageMeter

from models.losses import FocalLoss
from models.losses import RegL1Loss, RegLoss, NormRegL1Loss, RegWeightedL1Loss
from models.decode import ctdet_decode
from models.utils import _sigmoid
from utils.debugger import Debugger
from utils.post_process import ctdet_post_process
from utils.oracle_utils import gen_oracle_map
from .ctdet import CtdetTrainer

class TrackModelWithLoss(torch.nn.Module):
  def __init__(self, model, loss):
    super(TrackModelWithLoss, self).__init__()
    self.model = model
    self.loss = loss
  
  def forward(self, batch, prev_hm = None):
    if prev_hm is None:
      outputs = self.model(batch['prev_input'], batch['input'], batch['prev_hm'])
    else:
      outputs = self.model(batch['prev_input'], batch['input'], prev_hm)
    loss, loss_stats = self.loss(outputs, batch)
    return outputs[-1], loss, loss_stats

class TrackTrainer(CtdetTrainer):
  def __init__(self, opt, model, optimizer=None):
    super(TrackTrainer, self).__init__(opt, model, optimizer=optimizer)
    self.model_with_loss = TrackModelWithLoss(model, self.loss)
    self.prev_hm = 'Invalid String'

  def run_epoch(self, phase, epoch, data_loader):
    model_with_loss = self.model_with_loss
    if phase == 'train':
      model_with_loss.train()
    else:
      if len(self.opt.gpus) > 1:
        model_with_loss = self.model_with_loss.module
      model_with_loss.eval()
      torch.cuda.empty_cache()

    opt = self.opt
    results = {}
    data_time, batch_time = AverageMeter(), AverageMeter()
    avg_loss_stats = {l: AverageMeter() for l in self.loss_stats}
    num_iters = len(data_loader) if opt.num_iters < 0 else opt.num_iters
    bar = Bar('{}/{}'.format(opt.task, opt.exp_id), max=num_iters)
    end = time.time()
    for iter_id, batch in enumerate(data_loader):
      if iter_id >= num_iters:
        break
      data_time.update(time.time() - end)

      for k in batch:
        if k != 'meta':
          batch[k] = batch[k].to(device=opt.device, non_blocking=True)
      if phase == 'train':
        output, loss, loss_stats = model_with_loss(batch)
      else:
        if batch['meta']['first_frame'].cpu().numpy()[0]: #IMPORTANT: BATCH SIZE SHOULD BE 1
          prev_hm = torch.zeros_like(batch['prev_hm'])
        else:
          prev_hm = self.prev_hm
        output, loss, loss_stats = model_with_loss(batch, prev_hm)
      loss = loss.mean()
      if phase == 'train':
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
      batch_time.update(time.time() - end)
      end = time.time()

      Bar.suffix = '{phase}: [{0}][{1}/{2}]|Tot: {total:} |ETA: {eta:} '.format(
        epoch, iter_id, num_iters, phase=phase,
        total=bar.elapsed_td, eta=bar.eta_td)
      for l in avg_loss_stats:
        avg_loss_stats[l].update(
          loss_stats[l].mean().item(), batch['input'].size(0))
      Bar.suffix = Bar.suffix + '|{} {:.4f} '.format('loss', avg_loss_stats['loss'].avg)
      if not opt.hide_data_time:
        Bar.suffix = Bar.suffix + '|Data {dt.val:.3f}s({dt.avg:.3f}s) ' \
          '|Net {bt.avg:.3f}s'.format(dt=data_time, bt=batch_time)
      if opt.print_iter > 0:
        if iter_id % opt.print_iter == 0:
          print('{}/{}| {}'.format(opt.task, opt.exp_id, Bar.suffix)) 
      else:
        bar.next()
      
      if opt.debug > 0:
        self.debug(batch, output, iter_id)
      
      if phase == 'val':
        prev_hm = output['hm']
        mask = prev_hm < 0.1
        prev_hm[mask] = 0
        prev_hm_flat = torch.sum(prev_hm, 1, keepdim=True)
        self.prev_hm = torch.clamp(prev_hm_flat, 0, 1)
        self.save_result(output, batch, results)
      del output, loss, loss_stats
    
    bar.finish()
    ret = {k: v.avg for k, v in avg_loss_stats.items()}
    ret['time'] = bar.elapsed_td.total_seconds() / 60.
    return ret, results