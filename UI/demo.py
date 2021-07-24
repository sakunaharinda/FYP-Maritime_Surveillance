from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import _init_paths


import os.path as osp
import sys

import os
import cv2

from opts_flir import opts_flir
from detectors.detector_factory import detector_factory
from vis import draw_bboxes
from vis_utils import draw_bboxes_notrack
from track import tracking
from sort import *


image_ext = ['jpg', 'jpeg', 'png', 'webp']
video_ext = ['mp4', 'mov', 'avi', 'mkv']
time_stats = ['tot', 'load', 'pre', 'net', 'dec', 'post', 'merge']

color = [[255,255,255],[237,2,11],
[244,101,40],
[255,202,43],
[64,120,211],
[238,47,127],
[127,176,5],
[255,169,206],
[204,255,0],
[173,222,250],
[189,122,246]]


fps = 0
def demo(opt):
  global fps
  os.environ['CUDA_VISIBLE_DEVICES'] = opt.gpus_str
  opt.debug = max(opt.debug, 1)
  Detector = detector_factory[opt.task]
  detector = Detector(opt)
  print(opt.exp_id, opt.dataset)


  cam = cv2.VideoCapture(0 if opt.demo == 'webcam' else opt.demo)
  fps = cam.get(cv2.CAP_PROP_FPS)

  detector.pause = False
  mot_tracker = Sort()
  i=0
  while cam.isOpened():
      _, img = cam.read()
      #cv2.imshow('input', img)
      ret = detector.run(img)
      bboxes = ret['results']
      print(i)
      #print(bboxes)
      #tracked = tracking(bboxes,mot_tracker)
      img ,_= draw_bboxes_notrack(img,bboxes,type='flir',colors=color)
      
      
      cv2.imwrite(debugdir+'/{:05}.png'.format(i),img)
      i+=1
      
      
      
      if cv2.waitKey(1) == 27:
          return  # esc to quit
      



if __name__ == '__main__':
  opt = opts_flir().init()


  debugdir = 'demo/'+ str(opt.demo).split('/')[-1].split('.')[0]
  
  if not os.path.isdir(debugdir):
    os.makedirs(debugdir)
  opt.debug_dir = debugdir
  #opt.exp_id = "coco_dla" #'smd_split1'
  #opt.load_model = "../Center_SMD/exp/smd/dla_34/rgb/smd_split1/model_best.pth"
  opt.load_model = "../Center_SMD/exp/flir/dla_34/rgb/coco_dla/model_best.pth"
  #opt.dataset = "flir"

  demo(opt)

  # try:
  #   demo(opt)
  #   print(fps)
  # except:
  #   print(fps)
