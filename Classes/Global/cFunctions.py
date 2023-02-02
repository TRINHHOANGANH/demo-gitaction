import datetime
import json
from math import fabs
import threading

import kafka
import numpy as np
from cConstants import GlobConstant
from cProjectDataPostGreSQL import cProjectDataSQLGres
from cProjectTypes import CameraType, cProjectTypes
from cVariables import GlobVar

consumer = kafka.KafkaConsumer(GlobConstant.VEHICLETOPIC_MSG,bootstrap_servers=GlobConstant.BOOTSTRAP_SERVER,auto_offset_reset ='latest',enable_auto_commit=True)

class GlobFunc(object):
    def __init__(self, parent=None) -> None:
        super().__init__()
        

    def OpenEventPostGreSQL(name_column):
        '''Open ID in Event'''
        Results = False
        try:
            projectDataPostGreSQL = cProjectDataSQLGres()
            Results = projectDataPostGreSQL.Connect(GlobConstant.DB_HOST,GlobConstant.DB_NAME,GlobConstant.DB_USER,GlobConstant.DB_PASS,GlobConstant.DB_PORT)
            if Results: Value = projectDataPostGreSQL.OpenProject_EventInfo(name_column)
            return Value
        except BaseException as e:
            if GlobVar.DEBUG: print("cFunctions -- OpenCameraSQL -- "+ str(e))
            return ''


    def SaveEventInfoPostGreSQL(column_event,event_info):
        '''Save data to event table'''
        Results = False
        try:
            projectDataPostGreSQL = cProjectDataSQLGres()
            Results = projectDataPostGreSQL.Connect(GlobConstant.DB_HOST,GlobConstant.DB_NAME,GlobConstant.DB_USER,GlobConstant.DB_PASS,GlobConstant.DB_PORT)
            if Results: Results = projectDataPostGreSQL.SaveProject_EventInfo(column_event,event_info)
            return Results
        except BaseException as e:
            if GlobVar.DEBUG: print("cFunctions --SaveEventInfoPostGreSQL-- "+ str(e))
            return False

    def SaveVehicleDetectEventInfoPostGreSQL(column_event,event_info):
        '''Save data to vehicle_detect_event table'''
        Results = False
        try:
            projectDataPostGreSQL = cProjectDataSQLGres()
            Results = projectDataPostGreSQL.Connect(GlobConstant.DB_HOST,GlobConstant.DB_NAME,GlobConstant.DB_USER,GlobConstant.DB_PASS,GlobConstant.DB_PORT)
            if Results: Results = projectDataPostGreSQL.SaveProject_VehicleDetectEvent(column_event,event_info)
            return Results
        except BaseException as e:
            if GlobVar.DEBUG: print("cFunctions --SaveEventInfoPostGreSQL-- "+ str(e))
            return False


    def readMessage():
            message = consumer.poll(1.0)
            if len(message.keys()) == 0:
                pass

            if kafka.TopicPartition(topic=GlobConstant.VEHICLETOPIC_MSG, partition=0) in message.keys():
                data = message[kafka.TopicPartition(topic=GlobConstant.VEHICLETOPIC_MSG, partition=0)]
                print(data)
                try:
                    GlobVar.dict_cam =[]
                    for _ in range(data.__len__()):
                        cam = CameraType()
                        cam.command = json.loads(data[_].value)['cmd']
                        cam.cameraID = json.loads(data[_].value)['cameraID']
                        cam.streaming_url = json.loads(data[_].value)['streaming_url']
                        cam.coordinates = json.loads(data[_].value)['coordinates']['vehicleRecognition'][0]
                        cam.construction_id = json.loads(data[_].value)['construction_id']

                        GlobVar.dict_cam.append(cam)
                    return True
                except Exception as e:
                    if GlobVar.DEBUG: print("cFunctions --readMessage-- "+ str(e))
                    return False
