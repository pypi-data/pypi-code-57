from base import base
from airtest.core.api import *
from airtest.core.android.adb import *
from airtest.core.android.android import *

class logThread(threading.Thread):
    def __init__(self,id):
        threading.Thread.__init__(self)
        self.id = id
        self.dir()
    def run(self):
        self.log()

    def log(self):
        new = base(self.id)
        new.log('%s' % self.id)
    def dir(self):
        if os.path.isdir(self.id) == False:
            os.mkdir(self.id)
        elif os.path.isdir(self.id) == True:
            for i in os.listdir(self.id):
                path = os.path.join(self.id, i)
                os.remove(path)
            os.rmdir(self.id)
            os.mkdir(self.id)