# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 16:55:28 2020

@author: Jin Dou
"""
import sys
from .Logger import CLog

class CStageControl:
    
    def __init__(self,tartgetList,oLog=CLog()):
        self.targetList = tartgetList
        self.oLog = oLog
        
    def stage(self,stageNum):
        if(stageNum in self.targetList):
            self.oLog('Stage_' + str(stageNum) + ':')
            return True
        else:
#            sys.exit(0)
            return False
        
    def __call__(self,stageNum):
        return self.stage(stageNum)

stageList = [0]

def configStage(List):
    global stageList
    stageList = List

def decorStage(stageNum):
    def decorator(func):
        def wrapper(*args, **kw):
            if stageNum in stageList:
                return func(*args, **kw)
            else:
                return False
        return wrapper
    return decorator
