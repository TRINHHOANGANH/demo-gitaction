from asyncio.constants import SSL_HANDSHAKE_TIMEOUT
import os

from numpy import BUFSIZE

from cProjectTypes import TypesModelAI


class GlobConstant(object):
    #---------DB----------------
    DB_HOST = '10.248.243.110'
    DB_NAME = 'vcc_ai_events'
    DB_USER = 'postgres'
    DB_PASS = 'Vcc_postgres@2022'
    DB_PORT = 5432
    COLUMN_EVENT = "type_id, camera_id, created_at, captured_image_url"
    COLUMN_EVENT_VEHICLE_DETECTION = "vehicle_id, vehicle_detect_direction, vehicle_detect_type"
    EVENT_VEHICLE_ID ="id"
    #-----------Mode----------------
    MODE_RTSP = "1"
    MODE_FRAME = "0"
    #------------Kafka-------------
    BOOTSTRAP_SERVER = "10.248.243.110:39092"
    VEHICLETOPIC_MSG ="vehicleRecognition_Msg"
    VEHICLETOPIC_IOC ="vehicleRecognition"

    #--------------------------
    TYPESMODELAI_VEHICLE = 6
    #---------MinIO------------
    MINIO_ADDRESS = '10.248.243.110:9000'
    BUCKET_NAME = 'ai-images'
    MINIO_HTTPS = 'minio.congtrinhviettel.com.vn'
    #----------MODEL----------
    THRES_SCORE = 0.5
    THRES_IOU = 0.5


