#-*- coding:utf-8 -*-
import os
from hashlib import md5
import base64
import hashlib
class FileHelper:
    @staticmethod
    def get_file_md5_with_block(filename,block=204800):
        ret = None
        i = 0
        if not os.path.isfile(filename):
            return None,None,None
        with open(filename,'rb') as f:
            while True:
                myhash = hashlib.md5()
                b = f.read(block)
                if not b:
                    break
                myhash.update(b)
                yield myhash.hexdigest(),b,i
                i += 1
    @staticmethod
    def get_file_md5(filename):
        ret = None
        if not os.path.isfile(filename):
            return ret
        with open(filename, 'rb') as f:
            myhash = hashlib.md5()
            b = f.read()
            myhash.update(b)
            return myhash.hexdigest()

    @staticmethod
    def get_smallfile_md5(filename):
        ret = None
        if not os.path.isfile(filename):
            return None,None,None
        myhash = hashlib.md5()
        f = open(filename,'rb')
        b = f.read()
        myhash.update(b)
        f.close()
        return myhash.hexdigest(),b,os.path.splitext(filename)[-1][1:]
    @staticmethod
    def remove_file_dir(path,flag=True):
        if path:
            if flag:
                if os.path.isdir(path):
                    os.rmdir(path)
            else:
                if os.path.exists(path):  
                    os.remove(path)
    @staticmethod
    def get_stuffix_name(file_name,is_dot=True):
        '''
        '''
        if is_dot:
            return os.path.splitext(file_name)[-1]
        else:
            return os.path.splitext(file_name)[-1][1:]
    @staticmethod
    def get_current_path(file):
        ret =  os.path.dirname(os.path.abspath(file))
        return ret
    @staticmethod
    def get_parent_path(file,walk='..'):
        ret = os.path.abspath(FileHelper.get_current_path(file) + os.path.sep + walk)
        return ret
    @staticmethod
    def exist(path):
        ret = True
        if not os.path.isfile(path):
            if not os.path.isdir(path):
                ret = False
        return ret

    @staticmethod
    def read_file_cotent(path,blocksize= 1024):
        if FileHelper.exist(path):
            file_ptr = open(path,mode='r',encoding='utf-8')
            while True:
                part = file_ptr.read(blocksize)
                if part:
                    yield part
                else:
                    return None
        return None

    @staticmethod
    def walk_path(path):
        for root, dirs, files in os.walk(path, topdown=True):
            return root,dirs,files