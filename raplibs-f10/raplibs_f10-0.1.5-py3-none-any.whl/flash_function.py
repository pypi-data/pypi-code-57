# -*- coding: utf-8 -*-
"""
Created on Fri Apr  30 15:13:37 2020

@author: mb
"""
import time

flashSuccess = (0x00004F4B).to_bytes(4, 'big')
flashFailure = (0x00455252).to_bytes(4, 'big')
FlashPageSize = 256
    
def flashInitialize(dev):
    TDC_Engage ='A5 00 00 D0'
    dev.write(bytes.fromhex(TDC_Engage))
    A=dev.getStatus()
    while(A[0] < 8):
        time.sleep(11)
        A=dev.getStatus()
    Command=dev.read(4)
    if Command == (0xD0).to_bytes(4, 'big'):
        Status = dev.read(4)
        if Status == flashSuccess:
            #print('Initialization succeeded!\n')
            Success=True
        else: 
            print('Initialization failed!\n')
            raise ValueError('Initialization failed!')
    else:
        print('Initialization: Not proper command in echo. Check/flush input buffer\n')
        raise ValueError('Initialization: Not proper command in echo. Check/flush input buffer')    
            
def flashErase(dev):
    TDC_Engage ='A5 00 00 D1'
    dev.write(bytes.fromhex(TDC_Engage));
    A=dev.getStatus()
    while(A[0] < 8):
        time.sleep(10)
        A=dev.getStatus()
    Command=dev.read(4)
    if Command == (0xD1).to_bytes(4, 'big'):
        Status = dev.read(4)
        if Status == flashSuccess:
            #print('Erase succeeded!\n')
            Success=True;

        else: 
            print('Erase failed!\n')
            raise ValueError('Erase failed!')
    else:
        print('Erase: Not proper command in echo. Check/flush input buffer\n')
        raise ValueError('Erase: Not proper command in echo. Check/flush input buffer') 

def flashWrite(dev,flashDataBytes):
    FlashPageSize = 256
    TDC_Engage ='A5 00 00 D2'
    dev.write(bytes.fromhex(TDC_Engage));
    dev.write(flashDataBytes);
    A=dev.getStatus()
    while(A[0] < 8):
        time.sleep(10)
        A=dev.getStatus()
    Command=dev.read(4)
    if Command == (0xD2).to_bytes(4, 'big'):
        Status = dev.read(4)
        if Status == flashSuccess:
            #print('Write succeeded!\n')
            Success=True;
        else: 
            print('Write failed!\n')
            raise ValueError('Write failed!')
    else:
        print('Write: not proper command in echo. Check/flush input buffer')
        raise ValueError('Write: Not proper command in echo. Check/flush input buffer') 
    
def flashRead(dev):
    TDC_Engage ='A5 00 00 D3'
    dev.write(bytes.fromhex(TDC_Engage))
    A=dev.getStatus()
    while(A[0] < 8):
        time.sleep(10)
        A=dev.getStatus()
    Command=dev.read(4) 
    if Command == (0xD3).to_bytes(4, 'big'):
        Status = dev.read(4)
        if Status == flashSuccess:
            numOfBajtsRead = 0
            flashDataRead = bytes()
            while numOfBajtsRead < FlashPageSize: 
                A=dev.getStatus()
                if(A[0]>0):
                    numOfBajtsRead += A[0]
                    flashDataRead += dev.read(A[0])

                    return flashDataRead
        else: 
            print('Read failed!\n')
            raise ValueError('Read failed!\n')
    else:
        print('Read: not proper command in echo. Check/flush input buffer\n')
        raise ValueError('Read: Not proper command in echo. Check/flush input buffer') 

def flashPrepareData(dev,flashData):

    flashDataBytes = flashCheckData(dev,flashData)
    return flashDataBytes
    
def flashCheckData(dev,flashData):
    if len(flashData) != 64:
        raise ValueError('Not proper length of flashData list. Should be 64 and is ' + str(len(flashData)))
            
    flashDataBytes = bytes()
    for element in flashData:
        if isinstance(element, int):
            flashDataBytes += element.to_bytes(4, 'big')
        elif isinstance(element, bytes):
            if len(element) == 4:
                flashDataBytes += element
            else:
                raise ValueError('Not proper format of the flashData list. Check element: "'+ element.decode("utf-8") + '"')              
        elif isinstance(element, str):
            if len(element) == 4:
                flashDataBytes += bytes(element, 'utf-8')
            else:
                raise ValueError('Not proper format of the flashData list. Check element: "'+ element + '"')  
        else:
            raise ValueError('Unsuported data type in the flashData list')  
            
    #print('\nSize of data from flash_data.py file: '+ str(len(flashDataBytes)))
    #print('flash_data.py file:')
    #print(flashDataBytes)
    
    if len(flashDataBytes) != 256:
        raise ValueError('Not proper length of flashDataBytes. Should be 256')
        
    #print('\nChecking succeeded!\n')  
    return flashDataBytes

def flashLoadDefaultSettings(dev):
    TDC_Engage ='A5 00 00 D4'
    dev.write(bytes.fromhex(TDC_Engage));
    A=dev.getStatus()
    while(A[0] < 8):
        time.sleep(10)
        A=dev.getStatus()
    Command=dev.read(4) 
    if Command == (0xD4).to_bytes(4, 'big'):
        Status = dev.read(4)
        if Status == flashSuccess:
            numOfBajtsRead = 0
            frontEndDefaultSettings = bytes()
            while numOfBajtsRead < 2*4: # in response there are two dwords (4 bajts): HV, DAC
                A=dev.getStatus()
                if(A[0]>0):
#                    print(f'bajts: {numOfBajtsRead:d}')
                    numOfBajtsRead += A[0]
                    frontEndDefaultSettings += dev.read(A[0])
                    print('\nSize of data: '+ str(len(frontEndDefaultSettings)))
                    print('Default settings (HV, DAC):')
                    print(frontEndDefaultSettings)
                    print('Loading default settings succeeded!\n')
                    return frontEndDefaultSettings
        else: 
            print('Loading default settings failed!\n')
            raise ValueError('Loading default settings failed!\n')
    else:
        print('Loading default settings: not proper command in echo. Check/flush input buffer\n')
        raise ValueError('Loading default settings: Not proper command in echo. Check/flush input buffer') 


def flashData_Creator(BoardNumber, HV_Val,DAC_Val,T_Val):
    flashData = [
    BoardNumber,      # board number/ID
    '4v1 ', # board version
    'v10 ', # hardware version
    'v8  ', # software version (Microblaze)
    HV_Val,   # high voltage
    DAC_Val,  # DAC
    T_Val,     # Temperature in Celsius
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    'HAMA', # detector S1, manufacturer
    'MATS',
    'U   ',
    'S133', # type no
    '60-1',
    '350P',
    'E   ',
    '4826', # serial no
    '3   ',
    '53.9', # Vop
    '9V  ',
    '0.03', # Id
    '1uA ',
    'HAMA', # detector S2, manufacturer
    'MATS',
    'U   ',
    'S133', # type no
    '60-3',
    '050P',
    'E   ',
    '7080', # serial no
    '8   ',
    '54.9', # Vop
    '8V  ',
    '0.12', # Id
    '3uA '
    ]
    return flashData


def DecodeFlash(FlashList):
    
    H_Val=int(FlashList[17:20].hex(),16)/100
    DAC_Val=int(FlashList[21:24].hex(),16)
    T_Ref=int(FlashList[25:28].hex(),16)/10
    return H_Val,DAC_Val,T_Ref

