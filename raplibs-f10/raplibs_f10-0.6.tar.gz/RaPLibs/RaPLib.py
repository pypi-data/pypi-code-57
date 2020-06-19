import ftd2xx as ftd
import sys
import time
import binascii
from RaPLibs.flash_function import flashLoadDefaultSettings, flashInitialize,flashRead, DecodeFlash
import math


def ReadConfigDevice(dev):
    try:
        flashInitialize(dev)
    except:
        print('Not Initialised - Reading Config')
    
    return DecodeFlash(flashRead(dev))

def ConvHV(HV):
    return  int(- 0.81*(HV**2) + 58*HV - 6.3e+02)

def ConvToHV(HV_DAC):
    return -58-math.sqrt(  58**2  +  4*(0.81)*(6.3e+02+HV_DAC)    )  /  (-0.81*2)


def ListAll():
    return ftd.listDevices()

def Connect(IdXDev):
    
    try:
        dev = ftd.open(IdXDev)
        ftd.FTD2XX.resetDevice(dev)
        dev.setBitMode(0xff,0x00)
        dev.setBitMode(0xff,0x40)
        dev.setFlowControl(ftd.ftd2xx.FLOW_RTS_CTS,0x11,0x13)
        dev.setTimeouts(250,250)
        dev.purge(ftd.ftd2xx.PURGE_RX)
        dev.purge(ftd.ftd2xx.PURGE_TX)
        return dev
    except:
        return None

def setHVDac(HV_Val,dev):
    if HV_Val>58.2:
        HV_Val=58.2

    if ConvHV(HV_Val) > 0:
        A=str(hex(ConvHV(HV_Val)))
        if len(A)>=5:
            B=' 0'+ A[2]+' '+A[3:]+' '
            
        if len(A)<5 and len(A)>3:
            B=' 00 '+ A[2:]+ ' ' 

        if len(A)==3:
            B=' 00 '+ '0'+A[2:]+ ' ' 

        StrTot='A5'+B+'A3'
        dev.write(bytes.fromhex(StrTot))
        return True
    else:
        return None

def setThDac(DAC_Val,dev):
    A=str(hex(DAC_Val))
    B='0'+ A[2]+ ' ' + A[3:5] + '' 
    StrTot='A5'+B+'A4'
    dev.write(bytes.fromhex(StrTot))
    return True


def readTemp(dev):
    TDC_Engage ='A5 00 00 A5'
    dev.write(bytes.fromhex(TDC_Engage))   
    A=dev.getStatus() 
    while(A[0] < 4):
            time.sleep(0.1)
            A=dev.getStatus() 
    TempDAC_RAW=dev.read(4) 
    TempDAC=int(TempDAC_RAW.hex(),16) 
    if TempDAC <=2048:
        Temp=(128/2048)*TempDAC 
    else:
        Temp=-(128/2048)*(4096-TempDAC) 
        
    return Temp 

def ReadDCR(dev):
    TDC_Engage ='A5 00 00 A6'
    dev.write(bytes.fromhex(TDC_Engage))

def DisableDCR(value,dev):
    TDC_Engage ='A5' + format(value,'04X') + 'A7'
    dev.write(bytes.fromhex(TDC_Engage))

def SetGateDCR(value,dev):

    TDC_Engage ='A5' + format(value,'04X') + 'A8'
    dev.write(bytes.fromhex(TDC_Engage))


def stop(dev):
    TDC_Engage ='A5 00 00 00'
    dev.write(bytes.fromhex(TDC_Engage)) 
    
def flushFIFO(dev):
    TDC_Engage ='A5 00 00 01'
    dev.write(bytes.fromhex(TDC_Engage)) 
    
def loadDefaultSettings(dev):
    TDC_Engage ='A5 00 0011'
    dev.write(bytes.fromhex(TDC_Engage)) 
    
def readDefaultSettings(dev):
    TDC_Engage ='A5 00 00 12'
    dev.write(bytes.fromhex(TDC_Engage)) 
    
def LEDTestA(dev):
    TDC_Engage ='A5 00 00 A1'
    dev.write(bytes.fromhex(TDC_Engage))    

def tdc_TsBitsMB(value,dev):
    TDC_Engage ='A5' + format(value,'04X') + 'B4'
    dev.write(bytes.fromhex(TDC_Engage)) 
    
def tdc_BitsMB(value,dev):   
    TDC_Engage ='A5' + format(value,'04X') + 'B5'
    dev.write(bytes.fromhex(TDC_Engage)) 

def tdc_BitsMBSwap(value,dev):
    TDC_Engage ='A5' + format(value,'04X') + 'B6'
    dev.write(bytes.fromhex(TDC_Engage)) 
    
def resetTDC(dev):
    TDC_Engage ='A5 00 00 C2'
    dev.write(bytes.fromhex(TDC_Engage)) 

def readHistogram(dev):
    TDC_Engage ='A5 00 00 C1'
    dev.write(bytes.fromhex(TDC_Engage)) 
    
def setOnlineCallibration(value,dev):
    TDC_Engage ='A5 00 00 C3' #OFF
    dev.write(bytes.fromhex(TDC_Engage)) 

# Bits no Burst
def readFIFO(dev):
    A=dev.getStatus()
    print(A)
    Results=dev.read(A[0]) 
    print(binascii.hexlify(bytearray(Results)))

def setTDCInputSignal(value,dev):
    TDC_Engage ='A5' + format(value,'04X') + 'C4'
    dev.write(bytes.fromhex(TDC_Engage)) 
    
#New function to read only the time stamps
#This one run continuously, to stop you have to send stop()

def tdc_TsMB(value,dev):
    TDC_Engage ='A5' + format(value,'04X') + 'B7'
    dev.write(bytes.fromhex(TDC_Engage)) 

def tdc_BitsMB_9Events(value,dev):
    TDC_Engage ='A5' + format(value,'04X') + 'B8'
    dev.write(bytes.fromhex(TDC_Engage)) 
   
def tdc_TsBitsMB_9Events(value,dev):
    TDC_Engage ='A5' + format(value,'04X') + 'B9'
    dev.write(bytes.fromhex(TDC_Engage)) 

#### Function for the FTD2xx wrapper


def Close(dev):
    try:
        dev.close()   
        return 1
    except:
        return 0
    

def VCompensate(TNow,TRef,VRef):
    return VRef+(TNow-TRef)*0.054