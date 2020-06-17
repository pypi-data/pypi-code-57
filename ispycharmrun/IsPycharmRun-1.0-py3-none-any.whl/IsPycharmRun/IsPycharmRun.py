'''
@file       :   IsPycharmRum.py
@author     :   shiboxuan
@email      :   shiboxuan02@playcrab.com
@date       :   2020-06-10
@version    :   1.0
'''

from functools import wraps
import os
class IsPycharmRun:
    def __init__(self, deviceUrl, logDir=None):
        self.deviceUrl = deviceUrl
        self.logDir = logDir

    def __call__(self, func):
        @wraps(func)
        def wrapped_function(*args):
            if self.isPycharmRun():
                print(func.__name__ + " was called")
                return func(basedir=args[0], devices=self.deviceUrl, logdir=self.logDir)
            else:
                return func(*args)
        return wrapped_function

    def isPycharmRun(self):
        isRunningInPyCharm = "PYCHARM_HOSTED" in os.environ
        return isRunningInPyCharm
