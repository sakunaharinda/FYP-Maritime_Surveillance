import cv2
import numpy as np
from sort import *



def tracking(dets,mot_tracker,thresh=0.5,):

     
    all = []
    for cat_name in dets:
        keep_inds = dets[cat_name][:, -1] > thresh
        for bbox in dets[cat_name][keep_inds]:
            bbl = bbox.tolist()
            bbl.append(cat_name)
            all.append(bbl)
    farr = np.array(all)
    #print(farr)
    tracked_objects = mot_tracker.update(farr)
    return tracked_objects