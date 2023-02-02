import sys
from cv2 import HOUGH_STANDARD
import psycopg2
from cVariables import GlobVar

class cPostGreSQL(object):
    __conn=None 
    __IsConnected = False
    __FileName:str = None
    def __init__(self,DB_Host,DB_FileName,DB_User,DB_Pass,DB_Port) -> None:
        self.__FileName = DB_FileName
        self.__Host = DB_Host
        self.__User = DB_User
        self.__Pass = DB_Pass
        self.__Port = DB_Port
        super().__init__()

    def Connect(self):
        try:
            if self.__IsConnected: return self.__IsConnected
            self.__conn = psycopg2.connect(host=self.__Host, database=self.__FileName,user=self.__User, password=self.__Pass, port=self.__Port)
            cursor = self.__conn.cursor()
            print("Opened database successfully")  
            self.__IsConnected = True   
        except BaseException as err:
            print(err) 
            self.__IsConnected = False    
            pass
        finally:
            print(self.__IsConnected)
            return self.__IsConnected


    def CloseDB(self):
        if not self.__conn is None:
            self.__IsConnected =False
            self.__conn.commit()
            self.__conn.close()
            print('Close DB')
    

    def GetDataTable (self, sqlQuery:str):
        rows =None
        try:
            if self.Connect() is False: return rows
            cur = self.__conn.cursor()
            cur.execute(sqlQuery)
            rows = cur.fetchall()
            cur.close()
            self.CloseDB()
            return rows           
        except BaseException as e:
            if GlobVar.DEBUG: print("cConnectDB -- "+str(e))
            return rows
    

    def ExecuteQuery(self,sqlQuery:str):
        try:
            if self.Connect() is False: return False
            cur = self.__conn.cursor()
            cur.execute(sqlQuery)
            self.CloseDB()
            return True
        except BaseException as e:
            if GlobVar.DEBUG: print("cConnectDB -- "+str(e))
            return False


    def AddRow(self,tuples_rows:tuple, table_name:str):
        try:
            
            if self.Connect() is False: return False
            cur= self.__conn.cursor()
            for row in  tuples_rows:
               # sqlQuery = "INSERT INTO " + table_name + " VALUES(?,?,?,?,?,?)" 
                sqlQuery = "INSERT INTO " + table_name + " VALUES(" + ("%s,"*len(row)).rstrip(',') + ")"
                cur.execute(sqlQuery,(row))
                self.__conn.commit()
            self.CloseDB()
            return True
        except BaseException as e:
            if GlobVar.DEBUG: print("cConnectDB --- " + str(e))
            return False


    def AddRowIncrease(self, column_event, tuples_rows:tuple, table_name:str):
        try:
            
            if self.Connect() is False: return False
            cur= self.__conn.cursor()
            # for row in  tuples_rows:
            sqlQuery = "INSERT INTO " + table_name + "(" + column_event + ")" + " VALUES (" + ("%s,"*len(tuples_rows)).rstrip(',') + ")"
            cur.execute(sqlQuery,(tuples_rows))
            self.__conn.commit()
            self.CloseDB()
            return True
        except BaseException as e:
            if GlobVar.DEBUG: print("cConnectDB --- AddRowIncrease--" + str(e))
            return False
