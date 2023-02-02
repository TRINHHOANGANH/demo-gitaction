import sys
import sqlite3

from cVariables import GlobVar

class cSQLite(object):
    __conn=None 
    __IsConnected = False
    __FileName:str = None
    def __init__(self,FileName) -> None:
        self.__FileName = FileName
        super().__init__()

    def Connect(self):
        try:
            if self.__IsConnected: return self.__IsConnected
            self.__conn = sqlite3.connect(self.__FileName)
            cursor = self.__conn.cursor()
            print("Opened database successfully")  
            self.__IsConnected = True   
        except BaseException as err:
            self.__IsConnected = False    
            print(err) 
            pass
        finally:
            print(self.__IsConnected)
            return self.__IsConnected


    def CloseDB(self):
        #print(cSQLite.IsConnected)
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
                sqlQuery = "INSERT INTO " + table_name + " VALUES(" + ("?,"*len(row)).rstrip(',') + ")"
                cur.execute(sqlQuery,(row))
                self.__conn.commit()
            self.CloseDB()
            return True
        except BaseException as e:
            if GlobVar.DEBUG: print("cConnectDB --- " + str(e))
            return False
