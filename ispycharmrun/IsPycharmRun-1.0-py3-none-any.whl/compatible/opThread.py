from base import base
from airtest.core.api import *
from airtest.core.android.adb import *
from airtest.core.android.android import *


class opThread(threading.Thread):
    def __init__(self,id):
        threading.Thread.__init__(self)
        self.id = id
    def run(self):
        print(self.id)
        self.runbase()
        #runbase2(self.id)

    def runbase(self):
        new = base(self.id)
        new.install()
        new.startup()
        new.update()