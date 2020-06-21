import time
import numpy as np
import cv2
from .core.model import Model
from .core import vrep

class Vision_sensor(Model):
    def __init__(self, client, id = ""):
        self.objectName = "Vision_sensor" + id
        super().__init__(client, self.objectName)
        self.id = id

        #initialize the visionsensor
        errorCode, self.resolution, rawimage = vrep.simxGetVisionSensorImage(self.client.ID, self.objectHandle,0,vrep.simx_opmode_streaming)
        time.sleep(0.5)
        return

    def read(self):
        errorCode, resolution, rawimage = vrep.simxGetVisionSensorImage(self.client.ID, self.objectHandle, 0, vrep.simx_opmode_buffer)
        self.resolution = resolution
        if (errorCode != 0):
            raise Exception("%s read error, handle: %s" % (self.objectName, self.objectHandle))
        sensorImage = np.array(rawimage, dtype=np.uint8)
        sensorImage.resize([resolution[1], resolution[0], 3])
        cv2.flip(sensorImage, 0, sensorImage)
        return sensorImage
