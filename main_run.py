from Read_message_consumer import ReadMessageConsumer
from Run_model_thread import RunModelThread

if __name__=='__main__':
    readMessageConsumer = ReadMessageConsumer()
    readMessageConsumer.start()
    runModelThread = RunModelThread()
    runModelThread.start()
    