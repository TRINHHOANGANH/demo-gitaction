
import glob
import os
import pathlib
import datetime
import threading
import cv2

class Timlapse_Module (threading.Thread):
    '''Init Function'''
    def __init__(self):
        threading.Thread.__init__(self)
        self.lst_Camera_Sort =[]
        self.outfile = "/home/aitraining/workspace/anhth57/dataset_vehicle"
        self.infile = "/home/aitraining/workspace/anhth57/dataset_vehicle_1"

    def run(self):
        img_lst = self.getImages(self.infile)
        img_lst_time = sorted(img_lst, key=lambda date: datetime.datetime.strptime(date.split('/')[-1].replace('.jpg','').replace("image_",''),"%Y-%m-%d %H:%M:%S"))
        for i in range(img_lst_time.__len__()):
            frame_read = cv2.imread(img_lst_time[i])
            cv2.imwrite(self.outfile + "/image_{}.jpg".format(i),frame_read)
        print("Done")

    def getImages(self,infile):
        dir1 = glob.glob(infile+'/*.jpg')
        return dir1


if __name__ == '__main__':
    timelapse = Timlapse_Module()
    timelapse.start()
