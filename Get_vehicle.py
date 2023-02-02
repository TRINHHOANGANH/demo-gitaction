from collections import deque
import math
import time
import cv2,io, json, bisect, psycopg2,torch
from sympy import true
from datetime import datetime,timezone
import numpy as np
from shapely.geometry import Polygon
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from minio import Minio
import threading
from cFunctions import GlobFunc
from cVariables import *
from deep_sort import Tracker
from load_model import load_model
from kafka.errors import KafkaError
models = load_model()

class RunModel(threading.Thread):
    def __init__(self,cam_dict):
        super().__init__()
        self.cameraID = cam_dict.cameraID
        self.rtsp = cam_dict.streaming_url
        self.coordinates = cam_dict.coordinates
        self.construction_id = cam_dict.construction_id
        self.doStop = False
        self.name ="thread-RunModel--" + str(self.cameraID)
        self.threadID = int(self.cameraID)
        self.model_yolov5 = models.yolov5
        self.memory = {}
        self.already_counted = []
        self.save_vid = False
        if not threading.Thread.is_alive(self):
            self.start()


    def run(self):
        ''' Run Model Thread'''
        frame_count = 0
        self.cap = cv2.VideoCapture(self.rtsp)
        x1 = int(self.coordinates[0][0])
        y1 = int(self.coordinates[0][1])
        x2 = int(self.coordinates[1][0])
        y2 = int(self.coordinates[1][1])
        line = [(x1, y1), (x2, y2)]
        while True:
            try:
                if self.doStop:
                    print("do stop")
                    break
                print(self.name)
                timer = cv2.getTickCount()
                ret, frame = self.cap.read()
                if not ret:
                    self.cap = cv2.VideoCapture(self.rtsp)
                    continue
                
                if frame_count%1==0:
                    # Inference
                    boxes = self.model_yolov5(frame).pandas().xyxy[0]
                    list_bboxs = Tracker.update(boxes, frame)
                    if len(list_bboxs)>0:
                        for output in list_bboxs:
                            conf= output[6]
                            id = output[4]
                            cls = output[7]
                            box = output[0:4]
                            midpoint = (int(box[0]+(box[2]-box[0])/2) , int(box[1]+(box[3]-box[1])/2))
                            origin_midpoint = (midpoint[0], frame.shape[0] - midpoint[1])
                            if id not in self.memory:
                                    self.memory[id] = deque(maxlen=2)
                            self.memory[id].append(midpoint)
                            previous_midpoint = self.memory[id][0]
                            origin_previous_midpoint = (previous_midpoint[0], frame.shape[0] - previous_midpoint[1])
                            if self._intersect(midpoint, previous_midpoint, line[0], line[1]) and (id not in self.already_counted):
                                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                cv2.imwrite("/home/aitraining/workspace/anhth57/Vehicle_test/dataset/image_{}.jpg".format(current_time),frame)
                # region Save Video
                if self.save_vid:
                    if vid_path != self.save_path:  # new video
                        vid_path = self.save_path
                        if isinstance(vid_writer, cv2.VideoWriter):
                            vid_writer.release()  # release previous video writer
                        if self.cap:  # video
                            fps = self.cap.get(cv2.CAP_PROP_FPS)
                            w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        else:  # stream
                            fps, w, h = 30, frame.shape[1], frame.shape[0]
                        vid_writer = cv2.VideoWriter(self.save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                    vid_writer.write(frame)
                #end region
                if cv2.waitKey(1) & 0xFF == ord('q'): 
                    break
            except BaseException as e:
                print(str(e))
        time.sleep(0.01)
        self.cap.release()
        cv2.destroyAllWindows()

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