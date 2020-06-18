# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 12:07:00 2020

@author: Jin Dou
"""
import array,os
import numpy as np
from .DirManage import checkFolder

''' Python Object IO'''
def saveObject(Object,folderName,tag, ext = '.bin'):
    checkFolder(folderName)
    file = open(folderName + '/' + str(tag) + ext, 'wb')
    import pickle
    pickle.dump(Object,file)
    file.close()
    
def loadObject(filePath):
    import pickle
    file = open(filePath, 'rb')
    temp = pickle.load(file)
    return temp

''' End '''

''' Load Bin and Text File '''
def loadBinFast(Dir,Type:str = 'd'):
    f = open(Dir,'rb')
    a = array.array(Type)
    a.fromfile(f, os.path.getsize(Dir) // a.itemsize)
    return np.asarray(a)
    

def loadText(Dir):
    f=open(Dir, "r")
    contents = f.read()
    f.close()
    return contents
''' End '''