from base import base
from airtest.core.api import *
from airtest.core.android.adb import *
from airtest.core.android.android import *
from opThread import opThread
from logThread import logThread

class devices(object):
    def __init__(self):
        self.devicess = ADB().devices()
        self.list = []
        self.processlist = []
        self.threadlist = []
        self.logthreadlist = []

    def connect(self):
        for i in self.devicess:
            self.list.append(i[0])
        print(self.list)
    def addthread(self):
        for j in self.list:
            self.threadlist.append(opThread(j))
            self.logthreadlist.append(logThread(j))
    def startthread(self):
        for startlogthread in self.logthreadlist:
            startlogthread.setDaemon(True)
            startlogthread.start()
        for startthread in self.threadlist:
            startthread.start()










if __name__ == '__main__':
    device = devices()
    device.connect()
    device.addthread()
    device.startthread()




