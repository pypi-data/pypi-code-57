#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 15:15:29 2020

@author: ele
"""

import logging 
import json
import shutil
import glob
import pickle

logger = logging.getLogger(__name__)
logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(module)s: %(message)s', level = 'INFO')


class IOUtils:
    
    @staticmethod
    def mkdir(path):
        """
        Create directory (with subdirectories). Equivalent to bash `mkdir -p`.
        
        args:
            path (str) : system path
        """
        if not glob.os.path.exists(path):
            glob.os.makedirs(path)
            logger.info("Created `{}`".format(path))

    @staticmethod
    def rm(path):
        """
        Remove directory/file. Equivalent to bash `rm -r`.
        
        args:
            path (str) : system path
        """
        if glob.os.path.exists(path):
            if glob.os.path.isdir(path):
                shutil.rmtree(path)
            else:
                glob.os.remove(path)
            logger.info("Deleted `{}`".format(path))
    
    @staticmethod
    def exists(path):
        """
        Check if directory/file exists.
        
        args:
            path (str) : system path
        
        return:
            res (bool) : response
            
        >>> IOUtils.exists('.')
        True
        """
        
        res = glob.os.path.exists(path)
        
        return res
    
    @staticmethod
    def join_paths(paths):
        """
        Create system paths from elements.
        
        args:
            paths (list) : elements to create path
        
        return:
            path (str) : system path
        
        >>> IOUtils.join_paths(['new','path','to','be','created'])
        'new/path/to/be/created'
        """
        
        path = glob.os.path.join(*paths)
        return path
    
    @staticmethod
    def dname(path):
        """
        Return name of main directory.
        
        args:
            path (str) : system path
        
        return:
            name (str) : directory name
        
        >>> IOUtils.dname('/path/to/file.txt')
        '/path/to'
        """
        
        if path[-1] == glob.os.sep:
            path = path[:-1]
        
        name = glob.os.path.dirname(path)
        
        return name
    
    @staticmethod
    def fname(path):
        """
        Return name of file in system path.
        
        args:
            path (str) : system path
        
        return:
            name (str) : file name
        
        >>> IOUtils.fname('/path/to/file.txt')
        'file.txt'
        """
        
        if path[-1] == glob.os.sep:
            path = path[:-1]
            
        name = glob.os.path.basename(path)
        return name

    @staticmethod
    def readf(path,encoding = None):
        """
        Return content of a file.
        
         args:
            path (str) : system path
            encoding (str) : file encondigs
        
        return:
            content (str) : file content
        """
        with open(path,encoding = encoding) as infile:
            content = infile.read()
        return content
    
    @staticmethod
    def load_json(path):
        """
        Load JSON file into dict.
        
         args:
            path (str) : system path
        
        return:
            json_file (dict) : file content
        """
        with open(str(path)) as infile:
            json_file = json.load(infile)
        return json_file
    
    @staticmethod
    def save_json(path,item):
        """
        Save dict into JSON file .
        
         args:
            path (str) : system path
            item (dict) : dictionary
        
        return:
            json_file (dict) : file content
        """
        with open(str(path),'w') as outfile:
            json.dump(item, outfile)
            
        logger.info("Saved JSON `{}`".format(path))

    @staticmethod
    def load_pickle(path):
        """
        Load pickled python object.
        
         args:
            path (str) : system path
        
        return:
            item (object) : python object
        """
        with open(str(path), mode = "rb") as infile:
            item = pickle.load(infile)
        return item
      
    @staticmethod
    def save_pickle(item,path):
        """
        Save python object to pickle file .
        
         args:
            path (str) : system path
            item (dict) : python object 
        
        return:
            json_file (dict) : file content
        """
        
        with open(str(path), mode = "wb") as outfile:
            pickle.dump(item, outfile)
        logger.info("Saved pickle `{}`".format(path))
    
    @staticmethod
    def ioglob(path, ext = None, recursive = False):
        """
        Iterator yielding the SORTED paths matching a pathname pattern.
        
        args:
            path (str) : system path
            ext (str) : file extension
            recursive (bool) : check subfolder
            
        >>> list(IOUtils.ioglob(path = '.', ext = 'py'))
        ['./__init__.py', './ieaiaio.py', './setup.py']
        """
        
        
        ext = "*.{}".format(ext) if ext is not None else "*"
        
        splits = [path,ext] 
        
        if recursive:
            splits.insert(1,"**")
        
        pregex = glob.os.path.join(*splits)
        
        for p in sorted(glob.iglob(pregex)):
            yield p
    
    @staticmethod
    def iuglob(path,ext,recursive = False):
        """
        Iterator yielding the UNORDERED paths matching a pathname pattern.
        
        args:
            path (str) : system path
            ext (str) : file extension
            recursive (bool) : check subfolder
        """
        
        ext = "*.{}".format(ext) if ext is not None else "*"
        
        splits = [path,ext] 
        
        if recursive:
            splits.insert(1,"**")
            
        pregex = glob.os.path.join(*splits)
        
        for p in glob.iglob(pregex):
            yield p 
        
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()


