from .vrep import *
from .vrepConst import *

class Model(object):
    def __init__(self, client, objectName):
        self.client = client
        self.objectName = objectName
        self.objectHandle = client.bind(self.objectName)
        return

class Joint(Model):
    def set_velocity(self, speed):
        simxSetJointTargetVelocity(self.client.ID, self.objectHandle, speed, simx_opmode_streaming)
