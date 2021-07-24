from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .ctdet import CtdetTrainer
#from .ctdet_smd import CtdetTrainer
from .track import TrackTrainer
from .double import DoubleTrainer
from .sm import SMTrainer
from .ddd import DddTrainer
from .exdet import ExdetTrainer
from .multi_pose import MultiPoseTrainer
from .doublesm import DoubleSMTrainer

train_factory = {
  'exdet': ExdetTrainer, 
  'ddd': DddTrainer,
  'ctdet': CtdetTrainer,
  'ctdet_smd': CtdetTrainer,
  'double': DoubleTrainer,
  'track': TrackTrainer,
  'multi_pose': MultiPoseTrainer, 
  'sm': SMTrainer,
  'doublesm': DoubleSMTrainer
}
