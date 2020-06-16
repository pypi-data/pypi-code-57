'''
Created on 29 May 2020

@author: malgo

This program connect to the board, read the defauls settings and adjusts the HV according to the actual temperature

Output: BITStream
'''

import RaPLibs.Hex_To_Bit_Converter as Hex
import RaPLibs.RaPLib as RaP
import RaPLibs.flash_function as F 
import RaPLibs.NistTest as NIST
import numpy as np
import time


def GetBytes(dev,HV_Ref,DAC_Ref,T_Ref,MaxNumBit=1000000,TC=True,Bytes_Per_Run=1000):

    BytesReturn=[]
    RaP.setTDCInputSignal(0,dev)
    TempRefTDC=RaP.readTemp(dev)
    TNow=RaP.readTemp(dev)
    HVNow=RaP.VCompensate(TNow, T_Ref,HV_Ref)
    RaP.setHVDac(HVNow,dev)
    RaP.setThDac(DAC_Ref,dev)   
    BitRead=0
    RaP.resetTDC(dev)
    while BitRead < MaxNumBit:
        if TC==True:
            TNow=RaP.readTemp(dev)
            HVNow=RaP.VCompensate(TNow, T_Ref,HV_Ref)
            HVNow=HV_Ref
            RaP.setHVDac(HVNow,dev)
            if abs(TempRefTDC-TNow)>2:
                TempRefTDC=TNow
                RaP.resetTDC(dev)    

        RaP.tdc_BitsMB_9Events(Bytes_Per_Run,dev)
        A=dev.getStatus()
        while A[0]<4*Bytes_Per_Run:
            time.sleep(0.01)
            A=dev.getStatus()
        Bytes=dev.read(A[0])
        BitRead=BitRead+len(Bytes)*8
        BytesReturn.append(Bytes)

    return BytesReturn


def GetBits(dev,HV_Ref,DAC_Ref,T_Ref,MaxNumBit=1000000,TC=True):
    
    BitsReturn=[]
    RaP.setTDCInputSignal(0,dev)
    TempRefTDC=RaP.readTemp(dev)
    TNow=RaP.readTemp(dev)
    HVNow=RaP.VCompensate(TNow, T_Ref,HV_Ref)
    RaP.setHVDac(HVNow,dev)
    RaP.setThDac(DAC_Ref,dev)   
    BitRead=0
    RaP.resetTDC(dev)
    while BitRead < MaxNumBit:
        if TC==True:
            TNow=RaP.readTemp(dev)
            HVNow=RaP.VCompensate(TNow, T_Ref,HV_Ref)
            HVNow=HV_Ref
            RaP.setHVDac(HVNow,dev)
            if abs(TempRefTDC-TNow)>2:
                TempRefTDC=TNow
                RaP.resetTDC(dev)    

        RaP.tdc_BitsMB_9Events(1000,dev)
        A=dev.getStatus()
        while A[0]<4000:
            time.sleep(0.01)
            A=dev.getStatus()
        Bytes=dev.read(A[0])
        Aux=Hex.HexToBit(Bytes.hex())
        BitRead=BitRead+len(Aux)
        BitsReturn.append(Aux)

    return BitsReturn           
        
