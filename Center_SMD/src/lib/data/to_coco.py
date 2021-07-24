import os
import os.path
import cv2, pickle, json
import numpy as np
from collections import defaultdict

from hmdb21 import make_lists, CLASSES

def _transform_to_coco(bboxs, labels):
    anns = []
    for t in range(len(labels)):
      bbox = bboxs[t, :]
      bbox[2] = bbox[2] - bbox[0]
      bbox[3] = bbox[3] - bbox[1]
      label = labels[t]
      anns.append({'bbox': bbox.astype(np.float).tolist(), 'category_id': int(label) + 1})
    return anns

dataset = 'hmdb21'
root = 'hmdb21/'
input_type = 'rgb-images'
fulltest = True
trainlist, testlist, video_list, _ = make_lists(root, input_type, split = 1, fulltest = fulltest)

categories = []
for i, cl in enumerate(CLASSES):
  d = {"supercategory": cl,"id": i+1, "name": cl}
  categories.append(d)

# print (categories)
for list_number, filelist in enumerate([trainlist, testlist]):
  images = []
  annotations = []
  set = "test" if list_number else "train"
  filename = '-'.join((dataset, set, input_type,'fulltest' if fulltest else 'parttest'))
  print ('Ouput will be written to', filename)


  count = 0
  for index, info in enumerate(filelist):
    img_id = index
    annot_info = info
    frame_num = annot_info[1]
    video_id = annot_info[0]
    videoname = video_list[video_id]
    img_path = '{:s}/{:05d}.jpg'.format(videoname, frame_num)

    images.append({ 'id':img_id, 
                    'file_name': img_path,
                    'height': 240, #Check for HMDB
                    'width': 320    #Check for HMDB
                    })
    
    anns = _transform_to_coco(annot_info[3], annot_info[2])
    for ann in anns:
      count +=1
      area = ann['bbox'][2]*ann['bbox'][3]
      annotations.append({'bbox': ann['bbox'],
                          'image_id':img_id,
                          'category_id': ann['category_id'],
                          'area': area,
                          'iscrowd':0,
                          'id': count})
      if not (count % 1000):
        print ('Finished processing {} annotations'.format(count))
  # print (images)
  # print (annotations)

  coco_dataset = {'images':images,
                  'categories':categories,
                  'annotations':annotations}
  full_file_name = dataset + '/splitfiles/'+ filename +'.json'
  print ('Writing to json file')
  with open(full_file_name, 'w') as f:
    json.dump(coco_dataset, f)
    
