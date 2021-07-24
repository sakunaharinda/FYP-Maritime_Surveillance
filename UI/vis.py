import cv2
import numpy as np

def draw_bboxes(image, bboxes, type = "smd",font_size=1, thresh=0.5, colors=None):
    """Draws bounding boxes on an image.

    Args:
        image: An image in OpenCV format
        bboxes: A dictionary representing bounding boxes of different object
            categories, where the keys are the names of the categories and the
            values are the bounding boxes. The bounding boxes of category should be
            stored in a 2D NumPy array, where each row is a bounding box (x1, y1,
            x2, y2, score).
        font_size: (Optional) Font size of the category names.
        thresh: (Optional) Only bounding boxes with scores above the threshold
            will be drawn.
        colors: (Optional) Color of bounding boxes for each category. If it is
            not provided, this function will use random color for each category.

    Returns:
        An image with bounding boxes.
    """

    smd_class_name = [
  '__background__','Ferry', 'Buoy', 'Vessel/ship', 'Speed boat', 'Boat',
  'Kayak', 'Sail boat', 'Swimming person', 'Flying bird/plane', 'Other']

    flir_class_name = ['__background__','Person', 'Bicycle', 'Car']

    if type == 'smd':
        class_name = smd_class_name
    elif type == 'flir':
        class_name = flir_class_name


    categories = []

    image = image.copy()
    for bbox in bboxes:
        conf = bbox[-1]
        cat_name = int(bbox[-2])-1
        cat_id = int(bbox[-3])
        cat_size  = cv2.getTextSize(class_name[cat_name]+"0.99 - ID: 100", cv2.FONT_HERSHEY_SIMPLEX, font_size, 3)[0]

        if colors is None:
            color = np.random.random((3, )) * 0.6 + 0.4
            color = (color * 255).astype(np.int32).tolist()
            
        else:
            color = colors[cat_name]

        
        bbox = bbox[0:4].astype(np.int32)
        if bbox[1] - cat_size[1] - 2 < 0:
            cv2.rectangle(image,
                (bbox[0], bbox[1] + 2),
                (bbox[0] + cat_size[0], bbox[1] + cat_size[1] + 2),
                color, -1
            )
            categories.append(class_name[cat_name])
            cv2.putText(image, class_name[cat_name]+" {:.1f} - ID: {}".format(conf,cat_id),
                (bbox[0], bbox[1] + cat_size[1] + 2),
                cv2.FONT_HERSHEY_SIMPLEX, font_size, (0, 0, 0), thickness=2
            )
        else:
            cv2.rectangle(image,
                (bbox[0], bbox[1] - cat_size[1] - 2),
                (bbox[0] + cat_size[0], bbox[1] - 2),
                color, -1
            )
            categories.append(class_name[cat_name])
            cv2.putText(image, class_name[cat_name]+" {:.1f} - ID: {}".format(conf,cat_id),
                (bbox[0], bbox[1] - 2),
                cv2.FONT_HERSHEY_SIMPLEX, font_size, (0, 0, 0), thickness=2
            )
        cv2.rectangle(image,
            (bbox[0], bbox[1]),
            (bbox[2], bbox[3]),
            color, 2
        )
    return image, set(categories)
