from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .exdet import ExdetDetector
from .ddd import DddDetector
from .ctdet import CtdetDetector
from .ctdet_double import CtdetDetectorDouble
from .ctdet_sm import CtdetDetectorSM
from .multi_pose import MultiPoseDetector

detector_factory = {
  'exdet': ExdetDetector, 
  'ddd': DddDetector,
  'ctdet': CtdetDetector,
  'seaships':CtdetDetector,
  'ctdet_smd': CtdetDetector,
  'ctdet_ucf24': CtdetDetector,
  'ctdet_hmdb21': CtdetDetector,
  'ctdet_ucf24_double': CtdetDetectorDouble,
  'ctdet_hmdb21_double': CtdetDetectorDouble,
  'ctdet_ucf24_sm': CtdetDetectorSM,
  'ctdet_hmdb21_sm': CtdetDetectorSM,
  'sm': CtdetDetectorSM,
  'multi_pose': MultiPoseDetector, 
}
