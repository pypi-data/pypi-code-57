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

class PeoplePerception(ALModule):

    def __init__(self, ip, port, memory, sharo, robot_name, th = 0.7):

        self.memory = memory
        self.robot = robot_name
        self.sharo = sharo
        self.port = 9559
        self.ip = ip

        self.name = "FaceEmotionEventListener"
        try:
            self.faceC = ALProxy("ALFaceCharacteristics",self.ip, self.port)
        except Exception as e:
            raise RuntimeError(str(e) + "Make sure you're not connected to a virtual robot." )        

        self.confidence = 0.35
        self.threshNeutralEmotion = self.confidence + 0.15
        self.threshHappyEmotion = self.confidence
        self.threshSurprisedEmotion = self.confidence + 0.05
        self.threshAngryEmotion = self.confidence + 0.2
        self.threshSadEmotion = self.confidence + 0.15
        self.emotions = ["neutral", "happy", "surprised", "angry", "sad"]
        self.counter = 0
        self.bIsRunning = False
        self.delayed = []
        self.errorMes = ""
        #print ( proxy_name + " success")
        self.timeOut = 1
        self.neutral = True
        self.happy = True
        self.surprised = True
        self.angry = True
        self.sad = True
        self.th = th

        
    def onStop(self):
            print("Emotion recognition stop")
            self.onUnload()
        
    def onUnload(self):
        self.counter = 0
        self.tProperties = [0,0,0,0,0]
        self.bIsRunning = False
        self.cancelDelays()


    def sendEmotion(self, emotion):
        data = {"primitive":"emotion", "input":{emotion:1}, "robot":self.robot}
        # print(emotion)
        self.sharo.send_json(data)

    def detectEmotion(self, ids, index):
        emotion = "none"
        try:

            #analyze only one face - Limitation of the NAO SDK?
            self.faceC.analyzeFaceCharacteristics(ids[0])
            time.sleep(0.2)
            properties = self.memory.getData("PeoplePerception/Person/"+str(ids[index])+"/ExpressionProperties")
            self.tProperties[0] = properties[0]
            self.tProperties[1] = properties[1]
            self.tProperties[2] = properties[2]
            self.tProperties[3] = properties[3]
            self.tProperties[4] = properties[4]

            recognized = [0,0,0,0,0]

            value = 0
            x = 0
            
            for i in range(len(recognized)):
                if (self.tProperties[i]>value and self.tProperties[i] > self.th ):
                    value = self.tProperties[i]
                    x = i

            if(x == 0 and not emotion == "neutral"):
                    self.sendEmotion("neutral")
                    
            elif(x == 1 and not emotion == "happy"):
                    self.sendEmotion("happy")
                
            elif(x == 2 and not emotion == "surprised"):
                    self.sendEmotion("surprised")
                    
            elif(x == 3 and not emotion == "angry"):
                    self.sendEmotion("angry")

            elif(x == 4 and not emotion == "sad"):
                    self.sendEmotion("sad")            
        except:
            time.sleep(.1)
                
        

    def onRun(self):
        print ("Emotion recognition started")
        self.tProperties = [0,0,0,0,0]
        self.bIsRunning = True
        time_not_seen = 10
        shirt_color = "white"
        face_detected = 0
        people_visible = 0
        distance = 1000
        alone = True
        time_th = 2
        
        while self.bIsRunning:

                #identify user
                ids = self.memory.getData("PeoplePerception/PeopleList")
                # print(ids)
                # print(len(ids))

                if len(ids) == 0:
                    self.errorMes = "No face detected"
                    alone = True

                    data = {"primitive":"human_detected", "input":{"no":1}, "robot":self.robot}
                    self.sharo.send_json(data)
                            
                elif len(ids) == 1:
                    try:
                        shirt_color = self.memory.getData("PeoplePerception/Person/"+str(ids[0])+"/ShirtColor")
                        time_not_seen = self.memory.getData("PeoplePerception/Person/"+str(ids[0])+"/NotSeenSince")
                        face_detected = self.memory.getData("PeoplePerception/Person/"+str(ids[0])+"/IsFaceDetected")
                        people_visible = self.memory.getData("PeoplePerception/Person/"+str(ids[0])+"/IsVisible")
                        distance = self.memory.getData("PeoplePerception/Person/"+str(ids[0])+"/Distance")
                        #print(time_not_seen)
                        
                        if time_not_seen > time_th:
                            if alone == False:
                                data = {"primitive":"people", "input":{"just_left":1}, "robot":self.robot}
                                self.sharo.send_json(data)
                                #print("alone")   
                            alone = True
                        else:
                            if alone == True:
                                data = {"primitive":"people", "input":{"just_arrived":1}, "robot":self.robot}
                                self.sharo.send_json(data)
                                #print("arrived")
                         
                            if face_detected==1:
                                self.detectEmotion(ids,0)

                            alone = False

                        data = {"primitive":"human_detected", "input":{"yes":1}, "robot":self.robot}
                        self.sharo.send_json(data)
                    

                    except:
                        time.sleep(.1)
                        
                elif len(ids) > 1:
                    data = {"primitive":"human_detected", "input":{"yes":1}, "robot":self.robot}
                    self.sharo.send_json(data)
                    
                time.sleep(1)

        
            

    def onTimeout(self):
        self.errorMes = "Timeout"
        self.onUnload()

    def cleanDelay(self, fut, fut_ref):
        self.delayed.remove(fut)

    def cancelDelays(self):
        cancel_list = list(self.delayed)
        for d in cancel_list:
            d.cancel()

##
##import nep
##import rize
##import nep_aldebaran
##
##robot_port = "9559"
##robot_name = "pepper"
##robot_ip = '192.168.11.47'
##middleware = "ZMQ"
##robot_info = {}
##type_robot = "pepper"
##
##pip   = robot_ip
##pport = int(robot_port)
##
##name_ = robot_name + "_sensors"
##node = nep.node(name_)  
##sharo = node.new_pub("/blackboard","json")
##
##sensors = nep_aldebaran.SensorEvents(robot_ip, int(robot_port))
##memory = sensors.getMemory()
##
##SpeechEventListener = PeoplePerception(robot_ip,pip, memory, sharo, robot_name)
##SpeechEventListener.onRun()
##time.sleep(5)
##SpeechEventListener.onStop()


