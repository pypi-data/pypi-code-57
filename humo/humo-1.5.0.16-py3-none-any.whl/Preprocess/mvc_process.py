from .processing import *
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm
import pathlib
import os
from ..motion.main.CoreProcessor import *

class MVCProcess:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = pd.read_csv("{}.csv".format(file_name),usecols=[0],sep=",",header=None,dtype=object)
        self.SwitchCount = None
        self.MVC = None
        self.Device = None
        self.DeviceHeader = None
        self.NumberOfTrials = None
        self.spep = None
        self.MMT_order = None
        self.EMG_name = None


    def AuteCheckData(self):
        for i in tqdm(range(2), desc="Now Loading..."):
            if i == 0:
                self.setDevice()
            elif i == 1:
                self.setDeviceHeader()
        self.setTriggerInfo()
        EMGs = int(input("How many muscles did you measure? : "))
        self.EMGs = EMGs
        self.setEMG_name_Aute()
        self.SetSwitch()

    @calc_MVC_values_with_proportion
    def setMVCValues(self,ratio):
        return

    def outputMVC(self):
        MVC_parames = {
            "MVCvalues": self.MVC,
            "EMG_name" : self.EMG_name,
            "MMT_order": self.MMT_order
        }
        return MVC_parames







    def setDevice(self):
        self.Device = self.getDevice()

    def setDeviceHeader(self):
        self.DeviceHeader = self.getDeviceHeader()

    @findSwitch
    def SetSwitch(self):
        return

    def setTriggerInfo(self):
        self.SwitchCount = int(input("How many times did you press the switch between the trials? : "))
        self.NumberOfTrials = int(input("How many trials do you have? : "))

    def setEMG_name_Aute(self):
        self.EMG_name = self.getEMG_set()

    def setEMG_name(self,*args):
        self.EMG_name = dict(zip(args, np.arange(len(args))))

    def setMMT_order(self,order):
        self.MMT_order = dict(zip(self.EMG_name.keys(), order))








    @sp_process4MVC
    def getStartPoint(self):
        return

    @length_process4MVC
    def getDeviceLength(self):
        return

    @readingData4MVC
    def getDevice(self):
        return

    @header("device")
    def getDeviceHeader(self):
        return

    @findEMG
    def getEMG_set(self):
        return self.EMGs

    @retrivingMMTData(adjustframes=True)
    @isMMTName(types="Delsys")
    def getEMGraw(self,name):
        return

# The method to use when you forget to press the switch
    def getSwitch_MMT(self):
        from ..dataIO.IO import SSP
        ssp = SSP()
        try:
            TriggerName = list(set(ssp.getSSP()["Trigger"]) & set(self.DeviceHeader))[0]
            switch = self.Device[TriggerName].values.astype("float32")
            return switch
        except TypeError:
            print("Please execute the AuteCheckData method first.")
            print("Processing was interrupted.")


    def getEMG_MMT(self,number):
        from ..dataIO.IO import SSP
        ssp = SSP()
        emg_device_name = set([i.lower() for i in ssp.getSSP()["EMGdevice"]])
        try:
            device_name = [i.lower() for i in self.DeviceHeader]
            emg_device = list(emg_device_name & set(device_name))[0]
            emg_num = list(device_name).index(emg_device) - 1
            emg = self.Device.iloc[:,emg_num + number].values.astype("float32")
            return emg
        except TypeError:
            print("Please execute the AuteCheckData method first.")
            print("Processing was interrupted.")

