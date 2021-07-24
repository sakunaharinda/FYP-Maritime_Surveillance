from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import _init_paths

import os
import cv2

from opts import opts
from detectors.detector_factory import detector_factory

image_ext = ['jpg', 'jpeg', 'png', 'webp']
video_ext = ['mp4', 'mov', 'avi', 'mkv']
time_stats = ['tot', 'load', 'pre', 'net', 'dec', 'post', 'merge']
fps = 0
def demo(opt):
  global fps
  #opt.debug_dir = 'demo_res/'
  os.environ['CUDA_VISIBLE_DEVICES'] = opt.gpus_str
  opt.debug = max(opt.debug, 1)
  Detector = detector_factory[opt.task]
  detector = Detector(opt)

  if opt.demo == 'webcam' or \
    opt.demo[opt.demo.rfind('.') + 1:].lower() in video_ext:
    cam = cv2.VideoCapture(0 if opt.demo == 'webcam' else opt.demo)
    fps = cam.get(cv2.CAP_PROP_FPS)

    detector.pause = False
    while cam.isOpened():
        _, img = cam.read()
        #cv2.imshow('input', img)
        ret = detector.run(img)
        time_str = ''
        for stat in time_stats:
          time_str = time_str + '{} {:.3f}s |'.format(stat, ret[stat])
        print(time_str)
        if cv2.waitKey(1) == 27:
            return  # esc to quit
  else:
    
    if os.path.isdir(opt.demo):
      image_names = []
      ls = os.listdir(opt.demo)
      
      for file_name in sorted(ls):
          ext = file_name[file_name.rfind('.') + 1:].lower()
          if ext in image_ext:
              image_names.append(os.path.join(opt.demo, file_name))
    else:
      image_names = [opt.demo]
    
    for (image_name) in image_names:
      ret = detector.run(image_name)
      bboxes = ret['results']
      #print(bboxes)
      time_str = ''
      for stat in time_stats:
        time_str = time_str + '{} {:.3f}s |'.format(stat, ret[stat])
      print(time_str)
if __name__ == '__main__':
  opt = opts().init()


  debugdir = 'demo/'+ opt.demo.split('.')[0].split('/')[-1]
  if not os.path.isdir(debugdir):
    os.makedirs(debugdir)
  opt.debug_dir = debugdir
  print ("Debug Directory: ",opt.debug_dir)

  try:
    demo(opt)
    print(fps)
  except:
    print(fps)
