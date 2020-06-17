from ctypes import *
from ctypes.wintypes import *
from enum import Enum
import time
import platform
import sys
import pkg_resources  # part of setuptools
import enum
import struct
from abc import ABCMeta, abstractmethod
from Anapass import Util

PackageName="anapass-python"
ModuleName="TModule"
version = pkg_resources.require(PackageName)[0].version

DisplayName="[" + PackageName + ":" + ModuleName + "] "


print("--------------------------------------------------------------------------------")
print(DisplayName + version)


#print(platform.architecture())
is64bit = sys.maxsize > 2**32
if is64bit :
    dllName="AnapassTModule.dll"
else :
    dllName="AnapassTModule32.dll"

print(DisplayName + "Try:  Loading DLL (" + dllName + ")")

try:
    Load_DLL = WinDLL(dllName)
except OSError as err:
    print("OS error: {0}".format(err))
    print("Load DLL from CurrentFolder " + "(./" + dllName + ")")
    Load_DLL = WinDLL('./' + dllName)

print(DisplayName + "Success:  Loading DLL (" + dllName + ")")

print(DisplayName + "Try:  Loading Symbol ")
#TDEVICE_API TED_RESULT TSys_WinInit();
TSys_WinInit = Load_DLL['TSys_WinInit']
TSys_WinInit.restype=c_int;

#TDEVICE_API TDEVICE_HDL TDeviceCreate(const TED_CHAR* fileName);
TDeviceCreate=Load_DLL['TDeviceCreate']
TDeviceCreate.restype=c_void_p
TDeviceCreate.argtypes=[c_int]

#TDEVICE_API TED_RESULT TDeviceDestroy(TDEVICE_HDL hdl);
TDeviceDestroy=Load_DLL['TDeviceDestroy']
TDeviceDestroy.restype=c_int;
TDeviceDestroy.argtypes=[c_void_p]

#TDEVICE_API TED_RESULT TDeviceConnect(TDEVICE_HDL hdl); 
TDeviceConnect = Load_DLL['TDeviceConnect']
TDeviceConnect.restype=c_int;
TDeviceConnect.argtypes=[c_void_p]

#TDEVICE_API TED_RESULT TDeviceDisconnect(TDEVICE_HDL hdl);
TDeviceDisconnect = Load_DLL['TDeviceDisconnect']
TDeviceDisconnect.restype=c_int;
TDeviceDisconnect.argtypes=[c_void_p]

#TDEVICE_API TED_RESULT TDeviceIsConnect(TDEVICE_HDL hdl);
TDeviceIsConnect = Load_DLL['TDeviceIsConnect']
TDeviceIsConnect.restype=c_int;
TDeviceIsConnect.argtypes=[c_void_p]

#TDEVICE_API TED_RESULT TDeviceSendTxtCmd(TDEVICE_HDL hdl, const TED_CHAR* cmd,  /*OUT*/ TED_CHAR* resp, TED_INT respMaxSize, TED_INT respDurMileSecond);
TDeviceSendTxtCmd = Load_DLL['TDeviceSendTxtCmd']
TDeviceSendTxtCmd.restype=c_int;
TDeviceSendTxtCmd.argtypes=[c_void_p, c_char_p, c_char_p, c_int, c_int]

#TDEVICE_API TED_RESULT TDeviceSendCtrlCmd(TDEVICE_HDL hdl, const TED_CHAR* cmd,  /*OUT*/ TED_CHAR* resp, TED_INT respMaxSize, TED_INT respDurMileSecond);
TDeviceSendCtrlCmd = Load_DLL['TDeviceSendCtrlCmd']
TDeviceSendCtrlCmd.restype=c_int;
TDeviceSendCtrlCmd.argtypes=[c_void_p, c_char_p, c_char_p, c_int, c_int]

#TDEVICE_API TED_RESULT TDeviceReadRegValue(TDEVICE_HDL hdl, TED_REGADDR regAddr, TED_INT byteOffset, TED_INT readCnt, /*OUT*/ TED_REGVALUE* regValue);
TDeviceReadRegValue = Load_DLL['TDeviceReadRegValue']
TDeviceReadRegValue.restype=c_int;
TDeviceReadRegValue.argtypes=[c_void_p, c_char, c_int, c_int, c_char_p]

#TDEVICE_API TED_RESULT TDeviceReadRegValue1Byte(TDEVICE_HDL hdl, TED_REGADDR regAddr, TED_INT byteOffset, /*OUT*/TED_REGVALUE* regValue);
TDeviceReadRegValue1Byte = Load_DLL['TDeviceReadRegValue1Byte']
TDeviceReadRegValue1Byte.restype=c_int;
TDeviceReadRegValue1Byte.argtypes=[c_void_p, c_char, c_int, c_char_p]

#TDEVICE_API TED_RESULT TDeviceWriteRegValue(TDEVICE_HDL hdl, TED_REGADDR regAddr, TED_INT byteOffset, TED_INT writeCnt,  TED_REGVALUE* regValue);
TDeviceWriteRegValue = Load_DLL['TDeviceWriteRegValue']
TDeviceWriteRegValue.restype=c_int;
TDeviceWriteRegValue.argtypes=[c_void_p, c_char, c_int, c_int, c_char_p]

#TDEVICE_API TED_RESULT TDeviceWriteRegValue1Byte(TDEVICE_HDL hdl, TED_REGADDR regAddr, TED_INT byteOffset, TED_REGVALUE regValue);
TDeviceWriteRegValue1Byte = Load_DLL['TDeviceWriteRegValue1Byte']
TDeviceWriteRegValue1Byte.restype=c_int;
TDeviceWriteRegValue1Byte.argtypes=[c_void_p, c_char, c_int, c_char]

#TDEVICE_API TED_RESULT TDeviceCatchPowerInfo(TDEVICE_HDL hdl, /*OUT*/struct TED_POWER_INFO* p_pwrinfo, TED_INT timeOut /*milisec */)
TDeviceCatchPowerInfo = Load_DLL['TDeviceCatchPowerInfo']
TDeviceCatchPowerInfo.restype=c_int;
TDeviceCatchPowerInfo.argtypes=[c_void_p, c_char_p, c_int]


# enum TFileTransferType {
#    TFileTransferTypeT5 = 0,
#    TFileTransferTypeMaxCount
#};

# enum TFileTransferError {
#    TFileTransferErrorSuccess = 0,
#    TFileTransferErrorSendPacket,
#    TFileTransferErrorNoResp,
#    TFileTransferErrorFileOpen,
#    TFileTransferErrorStorageSize,
#    TFileTransferErrorCRC
#};

#TDEVICE_API TFILETRANSFER_HDL TFileTransferCreate(enum TFileTransferType type, TDEVICE_HDL deviceHandle);
#TDEVICE_API TED_BOOL TFileTransferDestroy(TFILETRANSFER_HDL fileTransferHandle);
#TDEVICE_API TED_BOOL TFileTransferStart(TFILETRANSFER_HDL fileTransferHandle, const char* fileName);
#TDEVICE_API TED_BOOL TFileTransferStop(TFILETRANSFER_HDL fileTransferHandle);
#TDEVICE_API int TFileTransferGetFileByteSize(TFILETRANSFER_HDL fileTransferHandle);
#TDEVICE_API int TFileTransferGetTransferByteSize(TFILETRANSFER_HDL fileTransferHandle);
#TDEVICE_API TED_BOOL TFileTransferIsStart(TFILETRANSFER_HDL fileTransferHandle);
#TDEVICE_API TED_BOOL TFileTransferIsDone(TFILETRANSFER_HDL fileTransferHandle);
#TDEVICE_API TED_BOOL TFileTransferIsError(TFILETRANSFER_HDL fileTransferHandle);
#TDEVICE_API enum TFileTransferError TFileTransferGetLastError(TFILETRANSFER_HDL fileTransferHandle);

#TDEVICE_API TFILETRANSFER_HDL TFileTransferCreate(enum TFileTransferType type, TDEVICE_HDL deviceHandle);
TFileTransferCreate = Load_DLL['TFileTransferCreate']
TFileTransferCreate.restype=c_void_p;
TFileTransferCreate.argtypes=[c_int, c_void_p]

#TDEVICE_API TED_BOOL TFileTransferDestroy(TFILETRANSFER_HDL fileTransferHandle);
TFileTransferDestroy=Load_DLL['TFileTransferDestroy']
TFileTransferDestroy.restype=c_int;
TFileTransferDestroy.argtypes=[c_void_p]

#TDEVICE_API TED_BOOL TFileTransferStart(TFILETRANSFER_HDL fileTransferHandle, const char* fileName);
TFileTransferStart=Load_DLL['TFileTransferStart']
TFileTransferStart.restype=c_int;
TFileTransferStart.argtypes=[c_void_p, c_void_p]

#TDEVICE_API TED_BOOL TFileTransferStop(TFILETRANSFER_HDL fileTransferHandle);
TFileTransferStop=Load_DLL['TFileTransferStop']
TFileTransferStop.restype=c_int;
TFileTransferStop.argtypes=[c_void_p]

#TDEVICE_API int TFileTransferGetFileByteSize(TFILETRANSFER_HDL fileTransferHandle);
TFileTransferGetFileByteSize=Load_DLL['TFileTransferGetFileByteSize']
TFileTransferGetFileByteSize.restype=c_int;
TFileTransferGetFileByteSize.argtypes=[c_void_p]

#TDEVICE_API int TFileTransferGetTransferByteSize(TFILETRANSFER_HDL fileTransferHandle);
TFileTransferGetTransferByteSize=Load_DLL['TFileTransferGetTransferByteSize']
TFileTransferGetTransferByteSize.restype=c_int;
TFileTransferGetTransferByteSize.argtypes=[c_void_p]

#TDEVICE_API TED_BOOL TFileTransferIsStart(TFILETRANSFER_HDL fileTransferHandle);
TFileTransferIsStart=Load_DLL['TFileTransferIsStart']
TFileTransferIsStart.restype=c_int;
TFileTransferIsStart.argtypes=[c_void_p]

#TDEVICE_API TED_BOOL TFileTransferIsDone(TFILETRANSFER_HDL fileTransferHandle);
TFileTransferIsDone=Load_DLL['TFileTransferIsDone']
TFileTransferIsDone.restype=c_int;
TFileTransferIsDone.argtypes=[c_void_p]

#TDEVICE_API TED_BOOL TFileTransferIsError(TFILETRANSFER_HDL fileTransferHandle);
TFileTransferIsError=Load_DLL['TFileTransferIsError']
TFileTransferIsError.restype=c_int;
TFileTransferIsError.argtypes=[c_void_p]

#TDEVICE_API enum TFileTransferError TFileTransferGetLastError(TFILETRANSFER_HDL fileTransferHandle);
TFileTransferGetLastError=Load_DLL['TFileTransferGetLastError']
TFileTransferGetLastError.restype=c_int;
TFileTransferGetLastError.argtypes=[c_void_p]





print(DisplayName + "Success:  Loading Symbol ")


print(DisplayName + "Try: System Init")
TSys_WinInit()
print(DisplayName + "Success: System Init")
print("--------------------------------------------------------------------------------")
print("")


class TString :
    def __init__(this, str):
        this.__String = str

    def ToCTypeString(this) :
        return this.__String.encode('utf-8')

    #static method
    def ConvertToCTypeStrng(x) :
        return x.encode('utf-8')

    def ConvertCTypeStringToUnicode(x) :
        return x.decode('utf-8')


class TPower :

    class Type(enum.IntEnum) :
        VBAT1=0
        ELVSS=1
        VDD1=2
        VCI1=3
        VBAT2=4
        VDD2=5
        VCI2=6

    def __init__(this):
        this.No = 0
        this.Avail=[0 for _ in range(10)]
        this.Value1=[0 for _ in range(10)]
        this.Voltage=[0.0 for _ in range(10)]
        this.Current=[0.0 for _ in range(10)]
        this.Range1=[0.0 for _ in range(10)]
        this.Range2=[0.0 for _ in range(10)]


class TChip :
    class Type(enum.IntEnum) : 
        Common=0
        ANA6705=1
        ANA6706=2

class TBoard :
    class Type(enum.IntEnum) : 
        Common=0
        
#
# class TDevice
#
class TDevice :

    class Type(enum.IntEnum) : 
        T5 = 0
        T4 = 0
        T5PacketAnalysis=1
        TESys=2

    class ErrorString(enum.Enum) :
        GetResp="ErrorGetResp"
    
    def __init__(this, deviceType):
        #print(DisplayName +"TRY: create " + deviceType.name )
        this.__DeviceHandle = TDeviceCreate(deviceType.value)
        this.__DeviceType = deviceType

        #struct TED_POWER_INFO {
        #    TED_S32 no;
        #    TED_S32 available[10];
        #    TED_S32 value1[10];
        #    TED_FLOAT fV[10];
        #    TED_FLOAT fA[10];
        #    TED_FLOAT fRange1[10];
        #    TED_FLOAT fRange2[10];dir

        #};

        this.__PowerStructFmt = 'i'    #    TED_S32 no;    
        this.__PowerStructFmt+='10i'   # TED_S32 available[10];
        this.__PowerStructFmt+='10i'   # TED_S32 value[10];
        this.__PowerStructFmt+='10f'   # TED_FLOAT fV[10];
        this.__PowerStructFmt+='10f'   # TED_FLOAT fV[10];
        this.__PowerStructFmt+='10f'   # TED_FLOAT fRange1[10];
        this.__PowerStructFmt+='10f'   # TED_FLOAT fRange2[10];
        
        # arg=list(range(61))

        this.__PowerStructData = struct.pack(this.__PowerStructFmt, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                           0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                           0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                           0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                           )

    def __del__(this):
        #print("TDevice::~TDevice")
        TDeviceDestroy(this.__DeviceHandle)

    def GetName(this) :
        return this.__DeviceType.name
     
    def __getattr__(this, attrName) :
        if attrName == 'Handle' :
            return this.__DeviceHandle
        else :
            raise AttributeError(attrName)

    def Connect(this) :
        ret = TDeviceConnect(this.__DeviceHandle)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def Disonnect(this) :
        ret = TDeviceDisconnect(this.__DeviceHandle)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag
    
    def SendTxtCmd(this, cmd) :
        ret = TDeviceSendTxtCmd(this.__DeviceHandle, TString.ConvertToCTypeStrng(cmd), c_char_p(0), 0, 0)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def SendTxtCmdReadResp(this, cmd, maxRespByteSize) :
        respBytesArray=bytes(maxRespByteSize)
        ret = TDeviceSendTxtCmd(this.__DeviceHandle, TString.ConvertToCTypeStrng(cmd), respBytesArray, maxRespByteSize, 1000)
        if ret==1 :
            bflag = True
            resp = TString.ConvertCTypeStringToUnicode(respBytesArray)
        else :
            bflag = False;
            resp = TDevice.ErrorString.GetResp
        return resp


    #private methond
    def __SendCtrlCmd(this, cmd) :  
        ret = TDeviceSendCtrlCmd(this.__DeviceHandle, TString.ConvertToCTypeStrng(cmd), c_char_p(0), 0, 0)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def Reset(this) :
        return this.__SendCtrlCmd('RESET')

    def Next(this) :
        return this.__SendCtrlCmd('NEXT')

    def Back(this) :
        return this.__SendCtrlCmd('BACK')

    def ReadReg(this, regAddr, byteOffset, readCount, regValueList, regValueListStartIdx=0) :
        regValueInt = 0
        regValueByteArray=bytes(readCount)
        ret = TDeviceReadRegValue(this.__DeviceHandle, regAddr, byteOffset, readCount, regValueByteArray)
        if ret==1 :
            for idx, regValueByte in enumerate(regValueByteArray) :
                regValueInt = regValueByte
                regValueInt &= 0xFF
                regValueList[idx + regValueListStartIdx] = regValueInt
            bflag = True
        else :
            bflag = False;
        return bflag

    def ReadReg1Byte(this, regAddr, byteOffset) :
        regValueArray=bytes(1)
        ret = TDeviceReadRegValue1Byte(this.__DeviceHandle, regAddr, byteOffset, regValueArray)
        if ret==1 :
            regValue = regValueArray[0]
            regValue &= 0xFF
        else :
            regValue = -1
        return regValue

    def WriteReg(this, regAddr, byteOffset, writeCount, regValueList, writeDataStartIdx=0) :

        if writeDataStartIdx == 0 :
            regValueByteArray=bytes(regValueList)
        else :
            listTmp = regValueList[writeDataStartIdx:(writeDataStartIdx+writeCount)]
            regValueByteArray=bytes(listTmp)

        ret = TDeviceWriteRegValue(this.__DeviceHandle, regAddr, byteOffset, writeCount, regValueByteArray)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def WriteReg1Byte(this, regAddr, byteOffset, regValue) :
        ret = TDeviceWriteRegValue1Byte(this.__DeviceHandle, regAddr, byteOffset, regValue)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def WriteCtrlReg(this, regAddr) :
        return this.WriteReg1Byte(regAddr, 0, 1)

    def CatchPower(this, powerInfo) :

        ret = TDeviceCatchPowerInfo(this.__DeviceHandle,  this.__PowerStructData, 1000)

        result= struct.unpack(this.__PowerStructFmt, this.__PowerStructData)

        resIdx=0
        
        powerInfo.No = result[resIdx] 
        resIdx += 1

        for i in range(10) :
            powerInfo.Avail[i] = result[i+resIdx]
        resIdx += 10

        for i in range(10) :
            powerInfo.Value1[i] = result[i+resIdx]
        resIdx += 10

        for i in range(10) :
            powerInfo.Voltage[i] = result[i+resIdx]
        resIdx += 10

        for i in range(10) :
            powerInfo.Current[i] = result[i+resIdx]
        resIdx += 10

        for i in range(10) :
            powerInfo.Range1[i] = result[i+resIdx]
        resIdx += 10

        for i in range(10) :
            powerInfo.Range2[i] = result[i+resIdx]
        resIdx += 10

        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag




#
# class TFileTransfer
#
class TFileTransfer :

    class Type(enum.IntEnum) : 
        T5 = 0
        
    class ErrorType(enum.IntEnum) : 
        Success = 0,
        SendPacket=1,
        NoResp=2,
        FileOpen=3,
        StorageSize=4,
        CRC=5
    
    #TDEVICE_API TFILETRANSFER_HDL TFileTransferCreate(enum TFileTransferType type, TDEVICE_HDL deviceHandle);
    def __init__(this, type, device) :
        this.__TFileTransferHandle = TFileTransferCreate(type, device.Handle)
        this.__FileName = ""

    def __getattr__(this, attrName) :
        if attrName == 'LastErrorString' : 
            return this.GetLastErrorString()
        if attrName == 'FileName' : 
            return this.__FileName
        else :
            raise AttributeError(attrName)


    #TDEVICE_API TED_BOOL TFileTransferDestroy(TFILETRANSFER_HDL fileTransferHandle);

    #TDEVICE_API TED_BOOL TFileTransferStart(TFILETRANSFER_HDL fileTransferHandle, const char* fileName);
    def Start(this, fileName) : 
        this.__FileName = fileName
        bytesString = fileName.encode('euc-kr')
        #bytesString = fileName.encode('ascii')
        #bytesString = fileName.encode('utf-8')
        ret = TFileTransferStart(this.__TFileTransferHandle, bytesString)
        return ret

    #TDEVICE_API TED_BOOL TFileTransferStop(TFILETRANSFER_HDL fileTransferHandle);
    def Stop(this) : 
        ret = TFileTransferStop(this.__TFileTransferHandle)
        return ret

    #TDEVICE_API int TFileTransferGetFileByteSize(TFILETRANSFER_HDL fileTransferHandle);
    def GetFileByteSize(this) : 
        ret = TFileTransferGetFileByteSize(this.__TFileTransferHandle)
        return ret

    #TDEVICE_API int TFileTransferGetTransferByteSize(TFILETRANSFER_HDL fileTransferHandle);
    def GetTransferByteSize(this) : 
        ret = TFileTransferGetTransferByteSize(this.__TFileTransferHandle)
        return ret

    #TDEVICE_API TED_BOOL TFileTransferIsStart(TFILETRANSFER_HDL fileTransferHandle);
    def IsStart(this) : 
        ret = TFileTransferIsStart(this.__TFileTransferHandle)
        return ret

    #TDEVICE_API TED_BOOL TFileTransferIsDone(TFILETRANSFER_HDL fileTransferHandle);
    def IsDone(this) : 
        ret = TFileTransferIsDone(this.__TFileTransferHandle)
        return ret

    #TDEVICE_API TED_BOOL TFileTransferIsError(TFILETRANSFER_HDL fileTransferHandle);
    def IsError(this) : 
        ret = TFileTransferIsError(this.__TFileTransferHandle)
        return ret

    #TDEVICE_API enum TFileTransferError TFileTransferGetLastError(TFILETRANSFER_HDL fileTransferHandle);
    def GetLastError(this) : 
        ret = TFileTransferGetLastError(this.__TFileTransferHandle)
        return ret

    def GetLastErrorString(this) :
        err = this.GetLastError()
        if err == TFileTransfer.ErrorType.Success :
            return "Success"
        elif err == TFileTransfer.ErrorType.SendPacket :
            return "SendPacket Error"
        elif err == TFileTransfer.ErrorType.NoResp :
            return "NoResp Error"
        elif err == TFileTransfer.ErrorType.FileOpen :
            return "FileOpen Error"
        elif err == TFileTransfer.ErrorType.StorageSize :
            return "StorageSize Error"
        elif err == TFileTransfer.ErrorType.CRC :
            return "CRC Error"
        else :
            return "Unknown Error"
    
