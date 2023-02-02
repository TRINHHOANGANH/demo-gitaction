from importlib.resources import path
import sys
import os
from typing import Tuple
from matplotlib.pyplot import title

# import class
sys.path.append("/home/aitraining/workspace/anhth57/Vehicle_test/Classes/Global")
sys.path.append("/home/aitraining/workspace/anhth57/Vehicle_test/Classes/ConnectDataBase")

from cConnectPostgres import cPostGreSQL
from cProjectTypes import CameraType, TypesModelAI, cProjectTypes
from cVariables import GlobVar, cTableName_Template

class cProjectDataSQLGres(object):
    MyConn:cPostGreSQL = None

    def __init__(self) -> None:
        super().__init__()
        self.Project = []
        self.Camera=[]

    
    def Connect (self,_DB_host,_DB_name,_DB_user,_DB_pass,_DB_port):
        self.MyConn = cPostGreSQL(_DB_host,_DB_name,_DB_user,_DB_pass,_DB_port)
        return self.MyConn.Connect()
    

    def Disconnect(self, _DataFileName: str):
        if not (self.MyConn is None):
            self.MyConn.Close() 


    def OpenProject_EventInfo(self,name_column):
        try:
            if not (self.MyConn.Connect()): return False
            ValueData = self.MyConn.GetDataTable('SELECT '+ name_column+' FROM ' +cTableName_Template.EventInfoPostGreSQL+' ORDER BY '+ name_column+ ' DESC LIMIT 1')
            return ValueData
        except BaseException as e:
            if GlobVar.DEBUG: print("cProjectData --OpenProject_EventInfo-- "+str(e))
            return ''  


    def SaveProject_EventInfo(self, column_event, value_event):
        
        try:
            if not (self.MyConn.Connect()): return False
            Result = self.MyConn.AddRowIncrease(column_event, value_event,cTableName_Template.EventInfoPostGreSQL)
            return Result
        except BaseException as e:
            if GlobVar.DEBUG: print("cProjectDataPostGreSQL -- SaveProject_EvenIfno-- "+str(e))
            return False
        

    def SaveProject_VehicleDetectEvent(self, column_event, value_event):
        
        try:
            if not (self.MyConn.Connect()): return False
            Result = self.MyConn.AddRowIncrease(column_event, value_event,cTableName_Template.VehicleEventPostGreSQL)
            return Result
        except BaseException as e:
            if GlobVar.DEBUG: print("cProjectDataPostGreSQL -- SaveProject_VehicleDetectEvent-- "+str(e))
            return False