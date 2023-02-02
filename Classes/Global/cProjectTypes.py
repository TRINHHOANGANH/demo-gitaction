from setuptools import Command


class cProjectTypes:
    FileName = None
    ProjectName:str =None
    Description = None
    CameraQuality :int =0
    Camera = None
    TypesModelAI = None
    TypesModelAINoSort = None
    def __init__(self) -> None:
        self.FileName = None
        self.ProjectName =None
        self.Description = None
        self.Camera = list()
        self.TypesModelAI = list()
        self.TypesModelAINoSort = list()
        

class CameraType:
    command = None
    cameraID = None
    name = None
    description = None
    construction_id = None
    streaming_url = None
    coordinates = None


class TypesModelAI:
    id = None
    name = None
    description = None