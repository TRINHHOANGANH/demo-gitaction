import os
import sys
from datetime import datetime
from cVariables import *

log_file = os.path.join(GlobConstant.PATH, "%s.log" % os.path.splitext(GlobConstant.SCRIPT)[0])

# def logit(fileObj, msg):
#     fileObj.write("[ %s ] %s" %(datetime.now().ctime(), msg))
#     if msg[-1] != '\n':
#         fileObj.write('\n')
#     fileObj.flush()


# def logmsg(msg):
#     logit(sys.stdout, msg)


# def logerr(msg):
#     logit(sys.stderr, msg)


def logMsg(msg):
    '''Write to the log and print to the screen.'''

    f = open(log_file, 'a')
    f.write("[ %s ] %s" %(datetime.now().ctime(), msg))
    print(msg)
    f.write("\n")
    f.close()
