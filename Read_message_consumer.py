import sys
sys.path.append("/home/aitraining/workspace/anhth57/Vehicle_test/Classes/Global")
from cFunctions import GlobFunc

import threading
import time

class ReadMessageConsumer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.name = "Thread -- ReadMessageConsumer"
    def run(self):
        while True:
            GlobFunc.readMessage()
            time.sleep(2)
