from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import torch.utils.data as data
import numpy as np
import torch
import json
import cv2
import os
from utils.image import flip, color_aug
from utils.image import get_affine_transform, affine_transform
from utils.image import gaussian_radius, draw_umich_gaussian, draw_msra_gaussian
from utils.image import draw_dense_reg
import math

class CTDetDataset_UCF24(data.Dataset):
  def _coco_box_to_bbox(self, box):
    bbox = np.array([box[0], box[1], box[0] + box[2], box[1] + box[3]],
                    dtype=np.float32)
    return bbox

  def _transform_to_coco(self, bboxs, labels):
    anns = []
    for t in range(len(labels)):
      bbox = bboxs[t, :]
      bbox[2] = bbox[2] - bbox[0]
      bbox[3] = bbox[3] - bbox[1]
      label = labels[t]
      anns.append({'bbox': bbox, 'category_id': label + 1})
    return anns
    
  def _scale_bbox(self, bbox, i_h, i_w, h, w):
    bbox[0] = float(bbox[0])*i_w/w
    bbox[2] = float(bbox[2])*i_w/w
    bbox[1] = float(bbox[1])*i_h/h
    bbox[3] = float(bbox[3])*i_h/h
    return bbox

  def _get_border(self, border, size):
    i = 1
    while size - border // i <= border // i:
        i *= 2
    return border // i

  def __getitem__(self, index):
    img_id = index  #
    # file_name = self.coco.loadImgs(ids=[img_id])[0]['file_name']
    # img_path = os.path.join(self.img_dir, file_name)
    annot_info = self.ids[index]
    frame_num = annot_info[1]
    video_id = annot_info[0]
    videoname = self.video_list[video_id]
    img_dir = os.path.join(self._imgpath, videoname)
    # ann_ids = self.coco.getAnnIds(imgIds=[img_id])
    # anns = self.coco.loadAnns(ids=ann_ids)
    anns = self._transform_to_coco(annot_info[3], annot_info[2])
    num_objs = min(len(anns), self.max_objs)

    inp = []
    start = frame_num - 7
    if start < 0:
      start = 1
    
    for i in range(start, frame_num + 1):
      base_output = np.load(os.path.join(img_dir, '{:05d}.npy'.format(i)))
      inp.append(base_output)
    
    if len(base_output) < self.num_frames:
      out_shape = base_output[0].shape
      padding = np.zeros((num_frames - len(base_outputs)*out_shape[0], 
                          out_shape[1], out_shape[2]))
      inp = np.concatenate((padding, *inp))
    else:
      inp = np.concatenate((*inp))
      


    height, width = 240,320
    c = np.array([320 / 2., 240 / 2.], dtype=np.float32)
    if self.opt.keep_res:
      input_h = (height | self.opt.pad) + 1
      input_w = (width | self.opt.pad) + 1
      s = np.array([input_w, input_h], dtype=np.float32)
    else:
      s = max(320, 240) * 1.0
      input_h, input_w = self.opt.input_h, self.opt.input_w

    output_h = input_h // self.opt.down_ratio
    output_w = input_w // self.opt.down_ratio
    num_classes = self.num_classes
    trans_output = get_affine_transform(c, s, 0, [output_w, output_h])

    hm = np.zeros((num_classes, output_h, output_w), dtype=np.float32)
    wh = np.zeros((self.max_objs, 2), dtype=np.float32)
    dense_wh = np.zeros((2, output_h, output_w), dtype=np.float32)
    reg = np.zeros((self.max_objs, 2), dtype=np.float32)
    ind = np.zeros((self.max_objs), dtype=np.int64)
    reg_mask = np.zeros((self.max_objs), dtype=np.uint8)
    cat_spec_wh = np.zeros((self.max_objs, num_classes * 2), dtype=np.float32)
    cat_spec_mask = np.zeros((self.max_objs, num_classes * 2), dtype=np.uint8)
    
    draw_gaussian = draw_msra_gaussian if self.opt.mse_loss else \
                    draw_umich_gaussian

    gt_det = []
    for k in range(num_objs):
      ann = anns[k]
      bbox = self._coco_box_to_bbox(ann['bbox'])
      # bbox = self._scale_bbox(bbox, input_h, input_w, height, width)
      cls_id = int(self.cat_ids[ann['category_id']])
      bbox[:2] = affine_transform(bbox[:2], trans_output)
      bbox[2:] = affine_transform(bbox[2:], trans_output)
      bbox[[0, 2]] = np.clip(bbox[[0, 2]], 0, output_w - 1)
      bbox[[1, 3]] = np.clip(bbox[[1, 3]], 0, output_h - 1)
      h, w = bbox[3] - bbox[1], bbox[2] - bbox[0]
      if h > 0 and w > 0:
        radius = gaussian_radius((math.ceil(h), math.ceil(w)))
        radius = max(0, int(radius))
        radius = self.opt.hm_gauss if self.opt.mse_loss else radius
        ct = np.array(
          [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2], dtype=np.float32)
        ct_int = ct.astype(np.int32)
        draw_gaussian(hm[cls_id], ct_int, radius)
        wh[k] = 1. * w, 1. * h
        ind[k] = ct_int[1] * output_w + ct_int[0]
        reg[k] = ct - ct_int
        reg_mask[k] = 1
        cat_spec_wh[k, cls_id * 2: cls_id * 2 + 2] = wh[k]
        cat_spec_mask[k, cls_id * 2: cls_id * 2 + 2] = 1
        if self.opt.dense_wh:
          draw_dense_reg(dense_wh, hm.max(axis=0), ct_int, wh[k], radius)
        gt_det.append([ct[0] - w / 2, ct[1] - h / 2, 
                       ct[0] + w / 2, ct[1] + h / 2, 1, cls_id])
    
    ret = {'input': inp, 'hm': hm, 'reg_mask': reg_mask, 'ind': ind, 'wh': wh}
    if self.opt.dense_wh:
      hm_a = hm.max(axis=0, keepdims=True)
      dense_wh_mask = np.concatenate([hm_a, hm_a], axis=0)
      ret.update({'dense_wh': dense_wh, 'dense_wh_mask': dense_wh_mask})
      del ret['wh']
    elif self.opt.cat_spec_wh:
      ret.update({'cat_spec_wh': cat_spec_wh, 'cat_spec_mask': cat_spec_mask})
      del ret['wh']
    if self.opt.reg_offset:
      ret.update({'reg': reg})
    if self.opt.debug > 0 or not self.split == 'train':
      gt_det = np.array(gt_det, dtype=np.float32) if len(gt_det) > 0 else \
               np.zeros((1, 6), dtype=np.float32)
      meta = {'c': c, 's': s, 'gt_det': gt_det, 'img_id': img_id}
      ret['meta'] = meta
    return ret