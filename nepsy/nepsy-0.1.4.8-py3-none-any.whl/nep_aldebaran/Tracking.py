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

class Tracking(ALModule):

    def __init__(self, ip, port):

        self.port = 9559
        self.ip = ip

        self.name = "FaceTrackingEventListener"
        proxy_name = "ALTracker"

        self.tracker = ALProxy("ALTracker",self.ip, self.port)
        self.memory = ALProxy("ALMemory",self.ip, self.port)
        self.soundLocation = ALProxy("ALSoundLocalization",self.ip, self.port)
        self.targetName = "People"
        self.distanceX = 0.0
        self.distanceY = 0.0
        self.angleWz = 0.0
        self.soundDistance = 0.5
        self.thresholdX = 0.0
        self.thresholdY = 0.0
        self.thresholdWz = 0.0
        self.effector = "None"
        self.subscribeDone = False
        self.isRunning = False
        
        self.distance = 0.3
        self.soundDistance = 0.5
        self.confidence = 0.4
        self.sensitivity = 0.9
        self.memory.subscribeToEvent("ALTracker/ActiveTargetChanged", self.name, "onTargetChanged")
        print ( proxy_name + " success")
        self.running = False


    def onRun(self, input_ = "People", parameters = {"use_body":"Head", "use_arms":"None"}, parallel = False):

        if self.running == True:
            self.onStop()
            print("stoping last tracking and starting new one")
            self.onStart(input_, parameters, parallel)
        else:
            self.onStart(input_, parameters, parallel)
            
        #else:
            #self.onStop()


    def use_arms(self,parameters):

        value = "None"

        if parameters["LeftArm"] == True and parameters["RightArm"] == True:
            value = "Arms"

        elif parameters["LeftArm"] == True:
            value = "LArm"

        elif parameters["RightArm"] == True:
            value = "RArm"

        else:
            value = "None"

        return value

    def onTrackSound(self, input_ = "Head", parameters = {"LeftArm":False, "RigthArm":False}, parallel = False):

        new_parameters = {"use_body":input_, "use_arms":self.use_arms(parameters)}

        self.sensitivity = 0.9
        self.soundLocation.setParameter("Sensitivity", self.sensitivity)
        
        if self.running == True:
            self.onStop()
            print("stoping last tracking")
            if input_ != "None":
                self.onStart("Sound", new_parameters, parallel)   
        else:
            if input_ != "None":
                self.onStart("Sound", new_parameters, parallel)



    def onTrackPeople(self, input_ = "Head", parameters = {"LeftArm":False, "RigthArm":False}, parallel = False):

        new_parameters = {"use_body":input_, "use_arms":self.use_arms(parameters)}
        
        if self.running == True:
            self.onStop()
            print("stoping last tracking")
            if input_ != "None":
                self.onStart("People", new_parameters, parallel)   
        else:
            if input_ != "None":
                self.onStart("People", new_parameters, parallel)
            

    def onTrackRedBall(self, input_ = "Head", parameters = {"LeftArm":False, "RigthArm":False}, parallel = False):

        new_parameters = {"use_body":input_, "use_arms":self.use_arms(parameters)}
        
        if self.running == True:
            self.onStop()
            print("stoping last tracking")
            if input_ != "None":
                self.onStart("RedBall", new_parameters, parallel)   
        else:
            if input_ != "None":
                self.onStart("RedBall", new_parameters, parallel)


    def onWalkTowards(self, input_ = "People", parameters = {"LeftArm":False, "RigthArm":False}, parallel = False):

        new_parameters = {"use_body":"Move", "use_arms":self.use_arms(parameters)}
        
        if self.running == True:
            self.onStop()
            print("stoping last tracking")
            if input_ != "None":
                self.onStart(input_, new_parameters, parallel)   
        else:
            if input_ != "None":
                self.onStart(input_, new_parameters, parallel)
            
        
    def onUnload(self):
        if self.subscribeDone:
            self.memory.unsubscribeToEvent("ALTracker/TargetLost", self.name)
            self.memory.unsubscribeToEvent("ALTracker/TargetReached", self.name)
            self.subscribeDone = False

        if self.isRunning:
            self.tracker.setEffector("None")
            self.tracker.stopTracker()
            self.tracker.unregisterTarget(self.targetName)
            self.isRunning = False

    def onStart(self, input_, parameters = {"use_body":"Head", "use_arms":"None"}, parallel = False):
        self.running = True
        if not self.isRunning:

            mode = "Head"
            self.effector ="None"

            try:
                mode = parameters["use_body"]   # "WholeBody", "Move", "Head"
                self.effector = parameters["use_arms"]  #  "None", "Arms", "LArms", "RArms"
            except:
                pass

            self.targetName = input_   #"People", "Face", "RedBall", Sound
            self.distanceX = 0.3
            self.threshodX = 0.1
            self.distanceY = 0.0
            self.thresholdY = 0.1
            self.angleWz = 0.0
            self.thresholdWz = 0.3
            

            if self.subscribeDone:
                self.memory.unsubscribeToEvent("ALTracker/TargetLost", self.name)
                self.memory.unsubscribeToEvent("ALTracker/TargetReached", self.name)
                self.subscribeDone = False
            
            self.memory.subscribeToEvent("ALTracker/TargetLost", self.name, "onTargetLost")
            self.memory.subscribeToEvent("ALTracker/TargetReached", self.name, "onTargetReached")
            self.subscribeDone = True

            self.tracker.setEffector(self.effector)

            if input_ == "Sound":
                self.tracker.registerTarget(self.targetName, [self.soundDistance, self.confidence])
                self.tracker.setRelativePosition([-self.distance, 0.0, 0.0,
                                            self.thresholdX, 0.1, 0.3])
            else:
                #follow people
                peopleIds = []
                self.tracker.registerTarget(self.targetName, peopleIds)
                #follow ball

                if input_ == "RedBall":
                    diameter = 0.06000
                    self.tracker.registerTarget(self.targetName, diameter)


                    
                self.tracker.setRelativePosition([-self.distanceX, self.distanceY, self.angleWz,
                                                   self.thresholdX, self.thresholdY, self.thresholdWz])
            self.tracker.setMode(mode)
            self.tracker.track(self.targetName) # Start tracker
            print ("Tracking activated")
            self.isRunning = True

    def onStop(self):
        if self.isRunning:
            self.onUnload()
            print ("Tracking not activated")

    def onTargetLost(self, key, value, message):
        print ("Target lost")
        #self.targetLost()

    def onTargetReached(self, key, value, message):
        print ("Target reached")
        #self.targetReached()

    def onTargetChanged(self, key, value, message):
        if value == self.targetName and not self.subscribeDone:
            self.memory.subscribeToEvent("ALTracker/TargetLost", self.name, "onTargetLost")
            self.memory.subscribeToEvent("ALTracker/TargetReached", self.name, "onTargetReached")
            self.subscribeDone = True
        elif value != self.targetName and self.subscribeDone:
            self.memory.unsubscribeToEvent("ALTracker/TargetLost", self.name)
            self.memory.unsubscribeToEvent("ALTracker/TargetReached", self.name)
            self.subscribeDone = False



##
##robot_port = "9559"
##robot_name = "pepper"
##robot_ip = '192.168.2.34'
##
##pip   = robot_ip
##pport = int(robot_port)
##import nep_aldebaran
##say = nep_aldebaran.SayText(robot_ip, robot_port)
##
##
##track = Tracking(robot_ip,pip)
##times = 8
####say.onRun("Following people with head")
####track.onTrackPeople("Head", {"LeftArm":False, "RightArm":True})
####time.sleep(times)
####track.onTrackPeople("None", {"LeftArm":False, "RightArm":True})
####
####say.onRun("Following people with body")
####track.onTrackPeople("WholeBody", {"LeftArm":False, "RightArm":True})
####time.sleep(times)
####track.onTrackPeople("None", {"LeftArm":False, "RightArm":True})
####
####say.onRun("Following red ball with head")
####track.onTrackRedBall("Head", {"LeftArm":False, "RightArm":True})
####time.sleep(times)
####
####say.onRun("Following red ball with body")
####track.onTrackRedBall("WholeBody", {"LeftArm":False, "RightArm":True})
####time.sleep(times)
##
##say.onRun("Sound")
##track.onTrackSound("Head", {"LeftArm":False, "RightArm":True})
##time.sleep(50)
##
####say.onRun("Walking towards People")
####track.onWalkTowards("People", {"LeftArm":False, "RightArm":True})
####time.sleep(times)
####
####say.onRun("Walking towards RedBall")
####track.onWalkTowards("RedBall", {"LeftArm":False, "RightArm":True})
####time.sleep(times)
##
##track.onStop()


