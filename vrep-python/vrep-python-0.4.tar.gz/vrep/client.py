from .core import vrep, model

class Client(object):
    @staticmethod
    def close_all():
        vrep.simxFinish(-1)  # close all connections
        return

    def __init__(self, ip = '127.0.0.1', port = 19999):
        self.ID = vrep.simxStart(ip, port, True, True, 5000, 5)
        if self.ID == -1:
            raise Exception('V-REP API server not found, please launch simualtion first')

        return

    def bind(self, objectName):
        handle = get_handle(self.ID, objectName)
        return handle


def get_handle(clientID, objectName):
    errorCode, handle = vrep.simxGetObjectHandle(clientID, objectName, vrep.simx_opmode_oneshot_wait)
    if (errorCode != 0):
        raise Exception('Object %s not found' % objectName)
    return handle
