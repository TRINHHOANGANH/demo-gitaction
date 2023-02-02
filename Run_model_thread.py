import threading
import time
from cFunctions import GlobFunc
from cVariables import GlobVar
from Run_model import RunModel

class RunModelThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.name = "RunModelThread"
        GlobVar.task_lst_run = []


    def run(self):
        ''' Run Thread Main'''
        while True:
            try:
                lst_name = [x.getName() for x in GlobVar.task_lst_run]
                for i in range(GlobVar.dict_cam.__len__()):
                    if (GlobVar.dict_cam[i].command == 'Add') and ("thread-RunModel--"+str(GlobVar.dict_cam[i].cameraID) not in lst_name):
                        print('add')
                        camerathread = RunModel(GlobVar.dict_cam[i])
                        GlobVar.task_lst_run.append(camerathread)
                    elif (GlobVar.dict_cam[i].command == 'Delete') and ("thread-RunModel--"+str(GlobVar.dict_cam[i].cameraID) in lst_name):
                        print('delete')
                        for thread in threading.enumerate():
                            if (str(thread.getName()) == "thread-RunModel--" +str(GlobVar.dict_cam[i].cameraID)) or (str(thread.getName()) == "ThreadCamera--" +str(GlobVar.dict_cam[i].cameraID)):
                                thread.doStop = True
                                if str(thread.getName()) == "thread-RunModel--" +str(GlobVar.dict_cam[i].cameraID):
                                    GlobVar.task_lst_run.remove([x for x in GlobVar.task_lst_run if x.cameraID == GlobVar.dict_cam[i].cameraID][0])
                                print('done delete')
                             
                    elif (GlobVar.dict_cam[i].command == 'Update') and ("thread-RunModel--"+str(GlobVar.dict_cam[i].cameraID) in lst_name):
                        print('update')
                        for thread in threading.enumerate():
                            if (str(thread.getName()) == "thread-RunModel--" +str(GlobVar.dict_cam[i].cameraID)) or (str(thread.getName()) == "ThreadCamera--" +str(GlobVar.dict_cam[i].cameraID)):
                                thread.doStop = True
                    
                                if str(thread.getName()) == "thread-RunModel--" +str(GlobVar.dict_cam[i].cameraID):
                                    GlobVar.task_lst_run.remove([x for x in GlobVar.task_lst_run if x.cameraID == GlobVar.dict_cam[i].cameraID][0])
                                 
                                print('done delete part of update')
                                

                        time.sleep(2)
                        GlobVar.dict_cam[i].command = 'Add'
                        camerathread = RunModel(GlobVar.dict_cam[i])
                        GlobVar.task_lst_run.append(camerathread)
            except BaseException as e:
                print(str(e))
                continue
            time.sleep(1)

