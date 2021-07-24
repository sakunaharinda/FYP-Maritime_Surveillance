from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .sample.ddd import DddDataset
from .sample.exdet import EXDetDataset
from .sample.ctdet import CTDetDataset
from .sample.ctdet_smd import CTDetDataset_SMD
from .sample.multi_pose import MultiPoseDataset
from .sample.ctdet_double import CTDetDataset_Double
from .sample.ctdet_sm import CTDetDataset_SM
from .sample.ctdet_doublesm import CTDetDataset_DoubleSM
from .sample.ctdet_track import CTDetDataset_Track

from .dataset.coco import COCO
from .dataset.smd import SMD
from .dataset.SeaShips import SeaShips
from .dataset.flir import flir
from .dataset.pascal import PascalVOC
from .dataset.kitti import KITTI
from .dataset.coco_hp import COCOHP
from .dataset.ucf24_draft import UCF24
from .dataset.hmdb21 import HMDB21


dataset_factory = {
  'coco': COCO,
  'smd': SMD,
  'seaships': SeaShips,
  'pascal': PascalVOC,
  'kitti': KITTI,
  'coco_hp': COCOHP,
  'flir':flir,
  'ucf24': UCF24,
  'hmdb21': HMDB21
}

_sample_factory = {
  'exdet': EXDetDataset,
  'ctdet': CTDetDataset,
  'ctdet_smd': CTDetDataset_SMD,
  'ddd': DddDataset,
  'multi_pose': MultiPoseDataset,
  'double': CTDetDataset_Double,
  'track': CTDetDataset_Track,
  'sm':CTDetDataset_SM,
  'doublesm': CTDetDataset_DoubleSM

}


def get_dataset(dataset, task):
  class Dataset(dataset_factory[dataset], _sample_factory[task]):
    pass
  return Dataset
  
