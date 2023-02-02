import sys
import cv2
import numpy as np

from deep_sort import DeepSort
# from module.yolov5.utils.plots import Annotator,colors

deepsort = DeepSort(
                    model_type='osnet_x0_25',
                    use_cuda=True,
                    max_dist=0.2,
                    max_iou_distance=0.7,
                    max_age=30, n_init=3, nn_budget=100,
                )


def draw_bboxes(image, bboxes, line_thickness):
    line_thickness = line_thickness or round(
        0.002 * (image.shape[0] + image.shape[1]) / 2) + 1
    print('bboxes:',bboxes)
    for (x1, y1, x2, y2, pos_id,cls_id,conf,lbl) in bboxes:
        color = (0, 255, 0)
        midpoint = (x1+int((x2-x1)/2) , y1+int((y2-y1)/2))
        c1, c2 = (x1, y1), (x2, y2)
        
        cv2.rectangle(image, c1, c2, color, thickness=line_thickness, lineType=cv2.LINE_AA)
        cv2.circle(image,midpoint,4,[255,255,0],1)
        font_thickness = max(line_thickness - 1, 1)
        cv2.putText(image, '{}--ID: {}--{}'.format(lbl, pos_id,conf), (c1[0], c1[1] - 2), 0, line_thickness / 3,
                    [0, 0, 255], thickness=font_thickness, lineType=cv2.LINE_AA)

    return image

def draw_image_2(im0,bboxes,line_thickness):
    annotator = Annotator(im0, line_width=line_thickness)
    for output in bboxes:
        
        box = output[0:4]
        id = output[4]
        cls = output[5]
        names = output[6]
        conf = output[7]
        #count
        # count_obj(bboxes,w,h,id)
        c = int(cls)  # integer class
        label = f'{id} {names[c]} {conf:.2f}'
        annotator.box_label(box, label, color=colors(c, True))
    im0 = annotator.result()
    return im0

def update(bboxes, image):
    
    bbox_xywh = []
    clss = []
    confs = []
    bboxes2draw = []
    lal_class =['motorbike','truck','excavator','scooptram','roller truck','conrete truck','car']
    if len(bboxes) > 0:
        for x1, y1, x2, y2, conf,cls, lbl in bboxes.values:
            obj = [
                int((x1 + x2) / 2), int((y1 + y2) / 2),
                x2 - x1, y2 - y1
            ]
            bbox_xywh.append(obj)
            clss.append(cls)
            confs.append(round(conf,3))
        xywhs = np.array(bbox_xywh)
        confss = np.array(confs)
        outputs = deepsort.update(bbox_xywh= xywhs,classes= clss,confidences= confss,ori_img= image)

        for value in list(outputs):
            x1, y1, x2, y2, track_label, track_id,conf_id = value
            bboxes2draw.append((int(x1), int(y1), int(x2), int(y2), track_label, track_id,conf_id,lal_class[track_id]))
        pass
    pass

    return bboxes2draw
