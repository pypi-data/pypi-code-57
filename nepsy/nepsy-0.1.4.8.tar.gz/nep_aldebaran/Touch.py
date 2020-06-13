#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

# Luis Enrique Coronado Zuniga

# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import time
import os
import sys
import copy

# Template action funtion:
"""

class name:
    def __init__(self,ip,port=9559):
        self.ip = ip
        self.port = port

    def onLoad(self):
        try: 
            proxy_name "AL.."
            self.proxy = ALProxy(proxy_name, self.ip, self.port)
            print ( proxy_name + " success")
        except:
            print ( proxy_name + " error")

    #onRun for action, onInput for peception.
    def onRun(self, input_ = "", parameters = {}, parallel = "false"):   

    def onStop(self, input_ = "", parameters = {}, parallel = "false"):


"""
# Template module:
"""

class NameModule(ALModule):
    def __init__(self, name, robot, ip  port = 9559):
        ALModule.__init__(self, name)
        self.name = name
        self.robot = robot
        self.ip = ip
        self.port = port
        try: 
            proxy_name = "AL.."
            self.proxy = ALProxy(proxy_name,self.ip,self.port)
            self.memory = ALProxy("ALMemory",self.ip, self.port)
            print ( proxy_name + " success")

            try:
                self.memory.subscribeToEvent(EventName, self.name, "EventListener")
            except():
                self.memory.unsubscribeToEvent(EventName, self.name)
                self.memory.subscribeToEvent(EventName, self.name, "EventListener")

        except:
            print ( proxy_name + " error")

    def EventListener(self, key, value, message):


"""


class Touch:

    def __init__(self, memory, sharo, robot_name, type_robot = "pepper", debug = False):
        self.memoryProxy = memory
        self.robot = robot_name
        self.sharo = sharo
        self.run = True
        self.type_robot = type_robot
        self.debug = debug

    def onRun(self):
        import copy
        
        body = { "left_hand": 0,  "right_hand": 0,  "head": 0}
        old_body = copy.deepcopy(body)
        value_touched = 0.4

        while self.run:
            
            try:

                if self.type_robot=="pepper":

                    self.Lhand_touched = self.memoryProxy.getData("Device/SubDeviceList/LHand/Touch/Back/Sensor/Value")
                    self.Rhand_touched = self.memoryProxy.getData("Device/SubDeviceList/RHand/Touch/Back/Sensor/Value")
                    
                else:

                    Lhand_touched1 = self.memoryProxy.getData("Device/SubDeviceList/LHand/Touch/Back/Sensor/Value")
                    Lhand_touched2 = self.memoryProxy.getData("Device/SubDeviceList/LHand/Touch/Left/Sensor/Value")
                    Lhand_touched3 = self.memoryProxy.getData("Device/SubDeviceList/LHand/Touch/Right/Sensor/Value")
                    self.Lhand_touched = max([Lhand_touched1,Lhand_touched2,Lhand_touched3])
                    
                    Rhand_touched1 = self.memoryProxy.getData("Device/SubDeviceList/RHand/Touch/Back/Sensor/Value")
                    Rhand_touched2 = self.memoryProxy.getData("Device/SubDeviceList/RHand/Touch/Left/Sensor/Value")
                    Rhand_touched3 = self.memoryProxy.getData("Device/SubDeviceList/RHand/Touch/Right/Sensor/Value")
                    self.Rhand_touched =  max(Rhand_touched1,Rhand_touched2,Rhand_touched3)
                    
                
                self.Head_touched = self.memoryProxy.getData("Device/SubDeviceList/Head/Touch/Middle/Sensor/Value")
                self.Head_touched_front = self.memoryProxy.getData("Device/SubDeviceList/Head/Touch/Front/Sensor/Value")
                self.Head_touched_rear = self.memoryProxy.getData("Device/SubDeviceList/Head/Touch/Rear/Sensor/Value")

                if self.Lhand_touched > value_touched:
                    value = 1
                    if body["left_hand"] != value:
                        data = {"primitive":"touched", "input":{"left_hand":value}, "robot":self.robot}
                        self.sharo.send_json(data)
                        body["left_hand"] = value
                        if self.debug:
                            print (data)
                else:
                    value = 0
                    if body["left_hand"] != value:
                        data = {"primitive":"touched", "input":{"left_hand":value}, "robot":self.robot}
                        self.sharo.send_json(data)
                        body["left_hand"] = value
                        if self.debug:
                            print (data)

                if self.Rhand_touched > value_touched:
                    value = 1
                    if body["right_hand"] != value:
                        data = {"primitive":"touched", "input":{"right_hand":value}, "robot":self.robot}
                        self.sharo.send_json(data)
                        if self.debug:
                            print (data)
                else:
                    value = 0
                    if body["right_hand"] != value:
                        data = {"primitive":"touched", "input":{"right_hand":value}, "robot":self.robot}
                        self.sharo.send_json(data)
                        body["right_hand"] = value
                        if self.debug:
                            print (data)
                    
                if self.Head_touched > value_touched or self.Head_touched_front > value_touched or self.Head_touched_rear > value_touched:
                    value = 1
                    if body["head"] != value:
                        data = {"primitive":"touched", "input":{"head":value}, "robot":self.robot}
                        self.sharo.send_json(data)
                        body["head"] = value
                        if self.debug:
                            print (data)
                else:
                    value = 0
                    if body["head"] != value:
                        data = {"primitive":"touched", "input":{"head":value}, "robot":self.robot}
                        self.sharo.send_json(data)
                        body["head"] = value
                        if self.debug:
                            print (data)
                            
                old_body = copy.deepcopy(body)
                
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                
            time.sleep(.01)
