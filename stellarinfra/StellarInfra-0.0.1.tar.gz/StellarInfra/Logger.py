# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 14:37:03 2020

@author: Jin Dou
"""
import datetime
from .DirManage import checkFolder
#maybe considering the offcial logging lib in the future

LOG_MODE = ['safe','fast',False]
PRINT_MODE = [True,False]
TRUE_FALSE= [True,False]
import sys
class CLog:
    #
    def __init__(self,folder=None,Name=None,ext = '.txt'):
        self._mode = 'safe' # 'fast' | 'safe'
        self._printFlag = True
        self._buffer = list()
        self.folder = None
        self.name = None
        self._fileName = None
        self.fileHandle = None
        if folder != None and Name != None:
            checkFolder(folder)
            self._fileName = folder+Name + ext
            self.Open()
            self.Save()
            self.folder = folder
            self.name = Name
        else:
            self.fileHandle = None
    
    @property
    def fileName(self):
        return self._fileName
    
    @fileName.setter
    def fileName(self,value):
        if self.fileHandle != None:
            self._fileName = value
            self.Open()
            self.Save()
    
    @property
    def Mode(self):
        return self._mode
    
    @Mode.setter
    def Mode(self,value):
        if value not in LOG_MODE:
            raise ValueError('value of mode is wrong ',LOG_MODE)
        else:
            self._mode = value
            
    @property
    def ifPrint(self):
        return self._printFlag
    
    @ifPrint.setter
    def ifPrint(self,value):
        if value not in PRINT_MODE:
            raise ValueError('value of mode is wrong ',PRINT_MODE)
        else:
            self._printFlag = value
            
    @property
    def ifLog(self):
        if self._mode == False:
            return False
        else:
            return True
    
    @property
    def usable(self):
        if(self.fileHandle != None):
            return True
        else:
            return False
    
    def Open(self):
        if self._fileName == None:
            return False
        self.fileHandle = open(self._fileName, "a+")
        
    def Save(self):
        if not self.usable:
            return False
        self.flushBuffer()
        self.fileHandle.close()
        
    def Write(self,Str,FlagLog,FlagPrint):
        '''
        flagLog for self.Write: 
            0: safe mode
            1: fast mode
            2: can't write
        flagPrint for self.Write:
            0: Print
            1: don't Print
        '''
#        print(FlagLog)
        if FlagPrint == 0:
            sys.stdout.write(Str)
#            sys.stdout.flush()
        if FlagLog == 2:
            return False
        if FlagLog == 0:
            self.fileHandle.write(Str)
        elif FlagLog == 1:
            self._buffer.append(Str)
        else:
            raise ValueError(FlagLog)
        
    def record(self,*logs,splitChar:str=' ',newline:bool = True):
        '''
        flagLog for self.Write: 
            0: safe mode
            1: fast mode
            2: can't write
        flagPrint for self.Write:
            0: Print
            1: don't Print
        '''
        flagLog = 2
        flagPrint = 1
        if self._printFlag:
            flagPrint = 0
        
        if not self.usable:
            flagLog = 2
        elif not self.ifLog:
            flagLog = 2
        else:
            if self._mode == 'safe':
                # to avoid leaving the content of the buffer behind, we need to flush it
                # this will reduce the difficulty of users' using
                self.flushBuffer()
                flagLog = 0
                self.Open()
            elif self._mode == 'fast':
                flagLog = 1
            else:
                flagLog = 2
        
        for idx,log in enumerate(logs):
            Str = str(log)
            if idx != len(logs) - 1 :
                self.Write(Str + splitChar,FlagLog=flagLog, FlagPrint=flagPrint)
            else:
                self.Write(Str,FlagLog=flagLog, FlagPrint=flagPrint)
        
        if(newline == True):
            self.Write('\n',FlagLog=flagLog, FlagPrint=flagPrint)
        else:
            self.Write(splitChar,FlagLog=flagLog, FlagPrint=flagPrint)
            
        if self.usable and flagLog == 0:
            # save the content to the file
            self.Save()
        
    def safeRecord(self,*logs,splitChar=' ',newline:bool = True):
        temp = self._mode
        self.Mode = 'safe'
        self.record(*logs,splitChar=splitChar,newline = newline)
        self.Mode = temp
    
    def safeRecordTime(self,*logs,splitChar=' ',newline:bool = True):
        now = datetime.datetime.now()
        self.safeRecord(*logs,now,splitChar=splitChar ,newline = newline)
        
    def flushBuffer(self):
        self.Open()
        if not self.usable:
            return False
        if(len(self._buffer) > 0):
            for log in self._buffer:
                self.fileHandle.write(log)
        self._buffer.clear()
        
    def __call__(self,*logs,splitChar=' ',newline:bool = True):
        return self.record(*logs,splitChar = splitChar, newline = newline)
    
    def t(self,*logs,splitChar=' ',newline:bool = True):
        now = datetime.datetime.now()
        return self.record(*logs,now,splitChar=splitChar ,newline = newline)
        
    def __del__(self):
        self.Save()
    