import pycocotools.coco as coco
from pycocotools.cocoeval import COCOeval
import json
import numpy as np
import copy

def boost_fusion(rgb, flow, thresh):
    '''
    Function to carry out boost fusion of rgb detections and flow detections
    Arguments:
        rgb: list of rgb detections
        flow: list of flow detections
        each item in the above lists is a dictionary containing
            detections[i] = {   'image_id'      : id, 
                                'category_id'   : cat_id, 
                                'bbox'          : [x1, y1, x2, y2], (Not normalized - for a 256x256 image)
                                'score'         : conf_score}
        thresh: IOU Threshold
    
    Outputs:
        fused : list of fused detections in the above format
    '''
    #Pseudocode
    #Extract detections into a convenient format: 
    print ('converting formats...', end = '')
    rgb_dets = convert_dets(rgb)
    flow_dets = convert_dets(flow)
    print ('done')
    #A dictionary for each type containing 
        #a dictionary for each image with  
            # a dictionary of detections {'bboxes': [], 'scores':[], 'category_ids':[]}
    
    
    fused_dets = {}
    #For each image:
    for image_id, dets in rgb_dets.items():
        if not image_id % 1000:
            print ('prcessing image id {:d}\r'.format(image_id), end = '')
        
        #Empty list of boxes, scores, cat_ids
        flow_img = flow_dets[image_id]
        fused_boxes = []
        fused_scores = []
        fused_ids = []
        covered_boxes = set()
        #Iterate through rgb detections
        for box, score, cat_id in zip(dets['bboxes'], dets['scores'], dets['category_ids']):
            box = box[:]
            #get flow box with max iou above threshold
            max_iou, max_ind = IOU(box, flow_img['bboxes'])
            
            #if non_empty and max_iou> thresh,
            if max_ind not in covered_boxes and max_iou > thresh:
                #update score
                if cat_id == flow_img['category_ids'][max_ind]:
                    score = min(1, score + flow_img['scores'][max_ind] * max_iou)
                elif score < flow_img['scores'][max_ind] * max_iou:
                    score = flow_img['scores'][max_ind]
                    box = flow_img['bboxes'][max_ind][:]
                    cat_id = flow_img['category_ids'][max_ind]
                #cover flow box
                covered_boxes.add(max_ind)

            #add rgb detection, score and cat_ids to lists
            fused_boxes.append(box)
            fused_scores.append(score)
            fused_ids.append(cat_id)
        
        #Iterated through non-covered flow detections
        for ind, (box, score, cat_id) in enumerate(zip(dets['bboxes'], dets['scores'], dets['category_ids'])):
            if ind not in covered_boxes:
                #add them to lists
                fused_boxes.append(box)
                fused_scores.append(score)
                fused_ids.append(cat_id)

        fused_dets[image_id] = {
                                'bboxes': fused_boxes,
                                'scores': fused_scores,
                                'category_ids': fused_ids,
        }
    print ('\nfinished boost fusion')
    return reconvert_dets(fused_dets) 

def convert_dets(all_det_list):
    '''
    each item in the above lists is a dictionary containing
            detections[i] = {   'image_id'      : id, 
                                'category_id'   : cat_id, 
                                'bbox'          : [x1, y1, w, h], (Not normalized - for a 256x256 image)
                                'score'         : conf_score}
    returns:
    dictionary of images, each item containing the following:
        images[id] = {          'category_id'   : cat_id, 
                                'bbox'          : [x1, y1, w, h], (Not normalized - for a 256x256 image)
                                'score'         : conf_score}
    '''
    images = {}
    for det in all_det_list:
        id = det['image_id']
        if id not in images:
            images[id] = {'bboxes':[], 'category_ids':[], 'scores':[]}
        ##Test
        if det['score'] < 0.001:
            all_det_list.remove(det)
            continue
        images[id]['bboxes'].append(det['bbox'])
        images[id]['category_ids'].append(det['category_id'])
        images[id]['scores'].append(det['score'])
    return images

def reconvert_dets(images):
    '''
    dictionary of images, each item containing the following:
        images[id] = {          'category_id'   : cat_id, 
                                'bbox'          : [x1, y1, w, h], (Not normalized - for a 256x256 image)
                                'score'         : conf_score}
    returns:
    list containing dictionaries containing
            detections[i] = {   'image_id'      : id, 
                                'category_id'   : cat_id, 
                                'bbox'          : [x1, y1, w, h], (Not normalized - for a 256x256 image)
                                'score'         : conf_score}
    '''
    detections = []
    for image_id, dets in images.items():
        for box, score, cat_id in zip(dets['bboxes'], dets['scores'], dets['category_ids']):
            det = { 'image_id'      : image_id, 
                    'category_id'   : cat_id, 
                    'bbox'          : box,
                    'score'         : score}
            detections.append(det)
    return detections

def IOU(b1, boxes):
    '''
    function to calculate IOU between b1 and boxes
    Arguments:
        b1: [x1, y1, w, h] not normalized
        boxes: list of boxes against which to compare in same format as b1
    returns
    max_iou: value of max iou with b1
    max_ind: indice of box with max iou with b1
    '''
    boxes = np.array(boxes).copy()
    b1 = np.array(b1).copy()

    areas = np.maximum(0, boxes[:, 2] * boxes [:, 3])
    ar1 = np.maximum(0, b1[2] * b1[3])
    boxes[:,2] += boxes[:,0]
    boxes[:,3] += boxes[:,1]
    b1[2] += b1[0]
    b1[3] += b1[1]
    intersections = np.array([  np.minimum(b1[2], boxes[:, 2]) - np.maximum(b1[0], boxes[:, 0]), 
                                np.minimum(b1[3], boxes[:, 3]) - np.maximum(b1[1], boxes[:, 1])])
    intersections = np.maximum(intersections, 0)
    intersections = intersections[0, :] * intersections[1, :]
    unions = areas + ar1 - intersections
    ious = np.divide(intersections, unions, out=np.zeros_like(intersections), where=unions!=0)
    return np.amax(ious), np.argmax(ious)

anot_file = "lib/data/ucf24/splitfiles/ucf24-test-rgb-images-parttest.json"
rgb_det_file = "../exp/ctdet_ucf24/default/results.json"
flow_det_file = "../exp/ctdet_ucf24/fastOF-flow/results.json"

##Combine the results files (For fusion)
with open(rgb_det_file, 'r') as f:
    rgb_results = json.load(f)

with open(flow_det_file, 'r') as f:
    flow_results = json.load(f)

assert (len(rgb_results) == len(flow_results))
results  = copy.deepcopy(rgb_results)
results.extend(copy.deepcopy(flow_results))

# print ('carrying out boost fusion')
# results = boost_fusion(rgb_results, flow_results, 0.25)
# print ('rgb detections:', len(rgb_results))
# print ('flow detections:', len(flow_results))
# print ('fused detections:', len(results))
# det_file = "../exp/ctdet_hmdb21/combined_results.json"
# json.dump(results, open(det_file, 'w'))

###Run the Evaluation
print ('RGB Results')
coco_gt = coco.COCO(anot_file)
coco_dets = coco_gt.loadRes(rgb_results)
coco_eval = COCOeval(coco_gt, coco_dets, "bbox")
coco_eval.evaluate()
coco_eval.accumulate()
coco_eval.summarize()

print ('Brox-flow Results')
coco_gt = coco.COCO(anot_file)
coco_dets = coco_gt.loadRes(flow_results)
coco_eval = COCOeval(coco_gt, coco_dets, "bbox")
coco_eval.evaluate()
coco_eval.accumulate()
coco_eval.summarize()


print ('Combined Results')
coco_gt = coco.COCO(anot_file)
coco_dets = coco_gt.loadRes(results)
coco_eval = COCOeval(coco_gt, coco_dets, "bbox")
coco_eval.evaluate()
coco_eval.accumulate()
coco_eval.summarize()