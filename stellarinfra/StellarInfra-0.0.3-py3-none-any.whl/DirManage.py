# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 12:11:13 2020

@author: Jin Dou
"""

import os
import warnings
from configparser import ConfigParser,BasicInterpolation


def checkFolder(folderPath):
    if not os.path.isdir(folderPath):
        warnings.warn("path: " + folderPath + "doesn't exist, and it is created")
        os.makedirs(folderPath)

def getFileList(folder_path,extension):
    ans = [folder_path+file for file in os.listdir(folder_path) if file.endswith(extension)]
    if(len(ans)==0):
        warnings.warn("getFileList's error: folder: '" + str(folder_path) + "'is empty with '" + str(extension) + "' kind of file")
        return None
    else:
        return ans
    
def getFileName(path):
    dataSetName, extension = os.path.splitext(os.path.basename(path))    
    return dataSetName,extension

def getSubFolderName(folder):
    subfolders = [f.name for f in os.scandir(folder) if f.is_dir() ]
    return subfolders

class CDirectoryConfig:
    
    def __init__(self,dir_List, confFile):
        self._dir_dict = dict()
        self._confFile = confFile
        for i in dir_List:
            self._dir_dict[i] = ''
        self._load_conf()
        self._addAttr()
        self._checkFolders()
            
    def _load_conf(self):
        conf_file = self._confFile
        config = ConfigParser(interpolation=BasicInterpolation())
        config.read(conf_file,encoding = 'utf-8')
        conf_name, ext = getFileName(conf_file)
        for dir_1 in self._dir_dict:
            self._dir_dict[dir_1] = config.get(conf_name, dir_1)
#            print(dir_1,config.get(conf_name, dir_1))
    
    def __getitem__(self,keyName):
        return self._dir_dict[keyName]
    
    def _checkFolders(self,foldersList = None):
        if foldersList != None:
            pass
        else:
            foldersList = self._dir_dict.keys()
        
        for folder in foldersList:
                checkFolder(self._dir_dict[folder])
    
    def _addAttr(self):
        for name in self._dir_dict:
            setattr(CDirectoryConfig,name,self._dir_dict[name])
    
