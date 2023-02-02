from collections import deque
import glob
import math
import time
from unicodedata import name
import cv2,io, json, bisect, psycopg2,torch
from sympy import true
from datetime import datetime,timezone
import numpy as np
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from minio import Minio
import threading
from deep_sort import Tracker
from load_model import load_model
from kafka.errors import KafkaError
models = load_model()

class RunModel(threading.Thread):
    def __init__(self):
        super().__init__()
        self.doStop = False
        self.model_yolov5 = models.yolov5
        self.memory = {}
        self.already_counted = []
        self.save_vid = False
        self.infile = "/home/aitraining/workspace/anhth57/dataset_vehicle"
        if not threading.Thread.is_alive(self):
            self.start()
        

    def run(self):
        ''' Run Model Thread'''
        img_lst = self.getImages(self.infile)
        img_lst_sort = sorted(img_lst, key=lambda date: int(date.split('/')[-1].replace('.jpg','').replace("image_",'')))
        for i in range (img_lst_sort.__len__()):
            try:
                if self.doStop:
                    print("do stop")
                    break
                timer = cv2.getTickCount()
                frame = cv2.imread(img_lst_sort[i])
                image_w = frame.shape[1]
                image_h = frame.shape[0]
                    # Inference
                boxes = self.model_yolov5(frame).pandas().xyxy[0]
                if len(boxes)>0:
                    print_buffer = []
                    for output in boxes.values:
                        conf= output[4]
                        id = output[5]
                        cls = output[6]
                        box = output[0:4]
                        # Transform the bbox co-ordinates as per the format required by YOLO v5
                        b_center_x = (box[0] + box[2]) / 2 
                        b_center_y = (box[1] + box[3]) / 2
                        b_width    = (box[2] - box[0])
                        b_height   = (box[3] - box[1])
                        
                        # Normalise the co-ordinates by the dimensions of the image
                        
                        b_center_x /= image_w 
                        b_center_y /= image_h 
                        b_width    /= image_w 
                        b_height   /= image_h

                        x1= box[0]/1920
                        y1 = box[1]/1080
                        x2= box[2]/1920
                        y2 = box[3]/1080
                        print_buffer.append("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(id, b_center_x, b_center_y, b_width, b_height))
                    name_file_text = img_lst_sort[i].replace(".jpg",".txt")
                    file= open(name_file_text, "w")   
                    file.write("\n".join(print_buffer))
                    file.close()
                    if i > 400:
                        cv2.imshow("imshow",frame)
                     
            except BaseException as e:
                print(str(e))
        time.sleep(0.01)
        print("Done")

    def getImages(self,infile):
        dir1 = glob.glob(infile+'/*.jpg')
        return dir1


    def _intersect(self, A, B, C, D):
        # kiem tra (A,C,D) co khac chieu voi (B,C,D)
        # kiem tra (A,B,C) co khac chieu voi (A,B,D)
        return self._ccw(A,C,D) != self._ccw(B, C, D) and self._ccw(A,B,C) != self._ccw(A,B,D)


    def _ccw(self, A,B,C):
        # Neu return true (A,B,C) cung chieu kim dong ho va ngc lai
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
    
    
    def _vector_angle(self, midpoint, previous_midpoint):
        x = midpoint[0] - previous_midpoint[0]
        y = midpoint[1] - previous_midpoint[1]
        return math.degrees(math.atan2(y, x))


if __name__ == '__main__':
    timelapse = RunModel()
