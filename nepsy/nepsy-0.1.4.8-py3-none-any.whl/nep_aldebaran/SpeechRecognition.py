#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

# Luis Enrique Coronado Zuniga

# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import nep
import threading
import time
import sys



class SpeechRecognition(ALModule):
    def __init__(self, name, ip, sharo, robot_name):
        ALModule.__init__(self, name)

        self.sharo = sharo
        self.name = name
        print("event id name = " + self.name)
        self.ip = ip
        self.word_spotting = True # If false the robot will only understand exact expressions
        self.visualExpression = True # Led feedback
        self.port = 9559
        self.proxy_name = "ALSpeechRecognition"
        self.visualExpression = True
        self.wordSpotting = True
        self.sensitivity = 0.45
        self.robot_name = robot_name

        try:
            self.asr = ALProxy(self.proxy_name, ip, 9559)
            print ( self.proxy_name + " success")
            #self.onLoad(vocabulary)

        except():
            print ( self.proxy_name + " error")
            #self.memory.unsubscribeToEvent("WordRecognized")
            #self.onLoad(vocabulary)

        self.word = 0


    def onFeedback(self,value):
        self.asr.pause(True)
        self.asr.setAudioExpression(value)
        self.asr.setVisualExpression(value)
        self.asr.pause(False)

    def onSetSensitivity(self,value):
        self.sensitivity = value
        
    
    def onLoad(self,vocabulary, feedback, language):
        
        self.onFeedback(feedback)
        self.asr.pause(True)
        self.asr.setLanguage(language)
        self.asr.setVocabulary(vocabulary, False)

        self.asr.setVisualExpression(self.visualExpression)
        self.asr.pushContexts()
        self.asr.setVocabulary(vocabulary, self.wordSpotting )

        self.memory = ALProxy("ALMemory",self.ip, self.port)
        self.memory.subscribeToEvent("WordRecognized", self.name, "onWordRecognized")
        self.memory.subscribeToEvent("SpeechDetected", self.name, "onSpeechDetected")
        self.asr.pause(False)


    def onSetVocabulary(self, vocabulary, feedback, language):
        try:
            self.onLoad(vocabulary,feedback,language)
        except():
            self.onStop()
            try: 
                print ( self.proxy_name + "restarting ..")
                self.onLoad(vocabulary, feedback, language)
            except():
                print ( self.proxy_name + " error")


    def onSpeechDetected(self,  key, value, message):
        data = {"primitive":"speech", "input":{"speech":1}, "robot":self.robot_name}
        self.sharo.publish(data)
        

    def onWordRecognized(self, key, value, message):

        print "Key: ", key
        print "Value: " , value
        #print "Message: " , message
        word = ""
        if (len(value) > 1 and value[1] > self.sensitivity):

            if self.wordSpotting:
                values_rest = value[0].split("<...> ")
                values_final = values_rest[1].split(" <...>")
                word  = values_final[0]
            
            data = {"primitive":"word", "input":{word:1}, "robot":self.robot_name}
            self.sharo.publish(data)

    def onStop(self):
        self.memory.unsubscribeToEvent("WordRecognized",self.name)
        self.memory.unsubscribeToEvent("SpeechDetected",self.name)
        print("Event closed")


##
##robot_ip= "192.168.0.101"
##robot_port= "9559"
##
##pip   = robot_ip
##pport = int(robot_port)
##name_ = "nao" + "_speech"
##node = nep.node(name_)  
##sharo = node.new_pub("/blackboard","json")
##
##try:
##    # We need this broker to be able to construct
##    # NAOqi modules and subscribe to other modules
##    # The broker must stay alive until the program exists
##    myBroker = ALBroker("myBroker",
##       "0.0.0.0",   # listen to anyone
##       0,           # find a free port and use it
##       pip,         # parent broker IP
##       pport)       # parent broker port
##
##
##    SpeechEventListener = SpeechRecognition("SpeechEventListener",pip,sharo,"pepper")
##    SpeechEventListener.onSetVocabulary(["hello", "gym", "weather" , "stop", "good morning", "thank you", "yes", "no"], "English")
##    
##except Exception as e: 
##    print(e)
##    time.sleep(5)
##    sys.exit(0)
##
##time.sleep(30)
##       
##SpeechEventListener.onStop()
##myBroker.shutdown()
##sys.exit(0)

