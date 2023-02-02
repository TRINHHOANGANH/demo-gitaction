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
        self.already_counted = deque(maxlen=200)
        self.count_up = 0
        self.count_down = 0
        self.count_total = 0
        self.save_path = '/home/aitraining/workspace/anhth57/Vehicle_test/output_img/video.mp4'
        self.save_vid = False
        self.vid_path = ''
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
                    # Draw line
                    cv2.arrowedLine(frame,line[0],line[1],(255,255,0),8)
                    # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # Inference
                    boxes = self.model_yolov5(frame).pandas().xyxy[0]
                    list_bboxs = Tracker.update(boxes, frame)
                    output_image_frame = Tracker.draw_bboxes(frame, list_bboxs, line_thickness=2)
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
                            cv2.line(frame, midpoint, previous_midpoint, (0, 255, 0), 2)
                            if self._intersect(midpoint, previous_midpoint, line[0], line[1]) and (id not in self.already_counted):
                                self.count_total += 1
                                # draw red line
                                cv2.line(frame, line[0], line[1], (255, 0, 0), 2)
                                self.already_counted.append(id)  # Set already counted for ID to true.
                                # angle = self._vector_angle(origin_midpoint, origin_previous_midpoint)
                                angle = self._ccw(line[0], line[1],previous_midpoint)
                                if angle == True:
                                    self.count_up += 1
                                    time_in = datetime.now()
                                    dt_string_in = time_in.strftime("%d:%m:%Y:%H:%M:%S")
                                    self.angle_in_out = "in"
                                    self.time_check = dt_string_in
                                    #endregion
                                elif angle == False:
                                    self.count_down += 1
                                    time_out = datetime.now()
                                    dt_string_out = time_out.strftime("%d:%m:%Y:%H:%M:%S")
                                    self.angle_in_out = "out"
                                    self.time_check = dt_string_out
                                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                                # if angle < 0 or angle > 0:
                                # cv2.putText(frame, "Total: {} ({} in, {} out)".format(str(self.count_total), str(self.count_up), str(self.count_down)), (int(0.05 * frame.shape[1]), int(0.1 * frame.shape[0])), 0, 
                                #     1.5e-3 * frame.shape[0], (0, 0, 0), 2)
                                # cv2.imwrite("/home/aitraining/workspace/anhth57/Vehicle_test/output_img/2.jpg",frame)
                                cv2.putText(frame,"Vehicle: {} -- Direction: {}".format(str(cls), str(self.angle_in_out)), (int(0.05 * frame.shape[1]), int(0.1 * frame.shape[0])), 0, 1.5e-3 * frame.shape[0], (255, 255, 255), 2)
                                #region Send Kafka
                                
                                retval, buffer = cv2.imencode('.jpg', frame)
                                image_name = 'vehicleRecognition/events/image_{}_{}_{}_{}.jpg'.format(id, self.time_check, cls, self.angle_in_out )
                                image_string = buffer.tostring()       
                                image_url = f'https://{GlobConstant.MINIO_HTTPS}/{GlobConstant.BUCKET_NAME}/{image_name}'       
                                GlobVar.client.put_object(bucket_name = GlobConstant.BUCKET_NAME, object_name = image_name, data = io.BytesIO(image_string), length = len(image_string), content_type="image/jpg")
                                data_send_kafka = {'cameraID': int(self.cameraID), 
                                                    'contructionID': int(self.construction_id),
                                                    'imageURL': [image_url]}                                              
                                get_events = GlobVar.producer.send(GlobConstant.VEHICLETOPIC_IOC, json.dumps(data_send_kafka).encode('utf-8'))                                 
                                try:
                                    get_events.get(timeout=1)
                                except KafkaError as e:
                                    print(e)
                                    continue
                                #endregion

                                #region Send DB
                                value_event =(GlobConstant.TYPESMODELAI_VEHICLE, self.cameraID, current_time, image_url)
                                if GlobFunc.SaveEventInfoPostGreSQL(GlobConstant.COLUMN_EVENT, value_event):
                                    value_event_vehicle_detect = (GlobFunc.OpenEventPostGreSQL(GlobConstant.EVENT_VEHICLE_ID)[0][0],self.angle_in_out,cls )
                                    GlobFunc.SaveVehicleDetectEventInfoPostGreSQL(GlobConstant.COLUMN_EVENT_VEHICLE_DETECTION,value_event_vehicle_detect)
                                #endregion
                    if len(self.memory) > 200:
                        del self.memory[list(self.memory)[0]]
                    FPS = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
                    print("FPS:",round(FPS))
                    #cv2.imshow("vid_out", output_image_frame)
                    frame_count += 1

                # region Save Video
                if self.save_vid:
                    if self.vid_path != self.save_path:  # new video
                        self.vid_path = self.save_path
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