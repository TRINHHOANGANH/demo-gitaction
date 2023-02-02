
from kafka import KafkaProducer
from cConstants import GlobConstant
from cProjectTypes import cProjectTypes
from minio import Minio
from cConstants import *
class GlobVar(object):
    ProjectCurrent:cProjectTypes = cProjectTypes()
    DEBUG = True
    producer = KafkaProducer(bootstrap_servers= GlobConstant.BOOTSTRAP_SERVER)
    client = Minio(
        GlobConstant.MINIO_ADDRESS,
        access_key='minioadmin',
        secret_key='Vcc_AI@2022',
        secure=False 
    )
    dict_cam =[]
    task_lst_run=[]
    imgs={}

class cTableName_Template:
    VehicleEventPostGreSQL ="vcc_events_management.vehicle_detection_event"
    EventInfoPostGreSQL ="vcc_events_management.event"


        