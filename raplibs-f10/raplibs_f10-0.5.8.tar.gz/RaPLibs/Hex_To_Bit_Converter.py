"""
Created on Mon Jan 21 00:14:58 2019

@author: malgo
"""

import numpy as np

def HexToBit(DataHex):
    
    DataArray=''
    for i in np.arange(0,len(DataHex)):
        if DataHex[i]=='0':
            DataArray += '0000'
        if DataHex[i]=='1':
            DataArray += '0001' 
        if DataHex[i]=='2':
            DataArray += '0010'
        if DataHex[i]=='3':
            DataArray += '0011'
        if DataHex[i]=='4':
            DataArray += '0100'
        if DataHex[i]=='5':
            DataArray += '0101'
        if DataHex[i]=='6':
            DataArray += '0110'
        if DataHex[i]=='7':
            DataArray += '0111'
        if DataHex[i]=='8':
            DataArray += '1000'
        if DataHex[i]=='9':
            DataArray += '1001'
        if DataHex[i]=='A' or DataHex[i]=='a':
            DataArray += '1010'
        if DataHex[i]=='B' or DataHex[i]=='b':
            DataArray += '1011'
        if DataHex[i]=='C' or DataHex[i]=='c':
            DataArray += '1100'
        if DataHex[i]=='D' or DataHex[i]=='d':
            DataArray += '1101'
        if DataHex[i]=='E' or DataHex[i]=='e':
            DataArray += '1110'
        if DataHex[i]=='F' or DataHex[i]=='f':
            DataArray += '1111'
            
    return DataArray;
        
                
                
        
def HexToBit_INT(DataHex):
    
    DataArray=np.zeros((4*len(DataHex),));
    for i in np.arange(0,len(DataHex)):
        if DataHex[i]=='0':
            DataArray[i*4:(i*4)+4] = [0, 0, 0, 0]
        if DataHex[i]=='1':
            DataArray[i*4:(i*4)+4] = [0, 0, 0, 1]
        if DataHex[i]=='2':
            DataArray[i*4:(i*4)+4] = [0, 0, 1, 0]
        if DataHex[i]=='3':
            DataArray[i*4:(i*4)+4] = [0, 0, 1, 1]
        if DataHex[i]=='4':
            DataArray[i*4:(i*4)+4] = [0, 1, 0, 0]
        if DataHex[i]=='5':
            DataArray[i*4:(i*4)+4] = [0, 1, 0, 1]
        if DataHex[i]=='6':
            DataArray[i*4:(i*4)+4] = [0, 1, 1, 0]
        if DataHex[i]=='7':
           DataArray[i*4:(i*4)+4] = [0, 1, 1, 1]
        if DataHex[i]=='8':
            DataArray[i*4:(i*4)+4] = [1, 0, 0, 0]
        if DataHex[i]=='9':
            DataArray[i*4:(i*4)+4] = [1, 0, 0, 1]
        if DataHex[i]=='A' or DataHex[i]=='a':
            DataArray[i*4:(i*4)+4] = [1, 0, 1, 0]
        if DataHex[i]=='B' or DataHex[i]=='b':
            DataArray[i*4:(i*4)+4] = [1, 0, 1, 1]
        if DataHex[i]=='C' or DataHex[i]=='c':
            DataArray[i*4:(i*4)+4] = [1, 1, 0, 0]
        if DataHex[i]=='D' or DataHex[i]=='d':
            DataArray[i*4:(i*4)+4] = [1, 1, 0, 1]
        if DataHex[i]=='E' or DataHex[i]=='e':
            DataArray[i*4:(i*4)+4] = [1, 1, 1, 0]
        if DataHex[i]=='F' or DataHex[i]=='f':
            DataArray[i*4:(i*4)+4] = [1, 1, 1, 1]
            
    return DataArray;





