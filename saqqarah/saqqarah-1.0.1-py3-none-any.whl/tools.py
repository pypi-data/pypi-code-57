#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 22:36:13 2020

@author: yves
"""

import os
from pathlib import Path
   
def filename_prepare(name, extensions, defaut_extension):
    """ 
    return basename, extension tuple
    keeping extension given if it's in extensions list
    add default_extension if not
    """
    
    if type(defaut_extension) is str:
        defaut_extension = defaut_extension.lower()
        
    if not defaut_extension in extensions:
        extensions.insert(0, defaut_extension)
    
    # replace spaces by _ and then split by '.'
    name = '_'.join(name.split())
    
    # check if name contains directory
    # os.path.dirname returns '' is there is no dirname
    # None if no dirname
    dirname = os.path.dirname(name) or None
    
    if dirname and not Path(dirname).is_dir():
            dirname = None
    
    pname = Path(name)
    # in pathlib, suffix contains the '.'
    ext = pname.suffix[1:].lower()
    basename = pname.stem
    
    # extension is in extensions_list ?
    if not ext in [ extension.lower() for extension in extensions]:
        # basenme is full name
        # extension is default_extension
        basename = pname.name
        ext = defaut_extension
        
    return basename, ext, dirname

def ensure_attr(obj, key, default):
    """
    put a default attribute if it does not exists or is None
    """
    if hasattr(obj, key):
        if getattr(obj,key) is None:
            setattr(obj,key, default)
    else:
        setattr(obj,key, default)
