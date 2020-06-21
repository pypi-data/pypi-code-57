#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 21:25:09 2020

@author: yves

    This file is part of Saqqarah.

    Saqqarah is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Saqqarah is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Saqqarah.  If not, see <https://www.gnu.org/licenses/>
"""

from PySide2.QtCore import QStandardPaths as sp
from time import strftime
from pathlib import Path

from . import filename_prepare

class Parameters:
    # output parameter
    basename = 'pyramid'
    __extension = None
    default_extension = None
    extensions_list = []
    
    use_timestamp = True
    
    # Pyramid parameter
    size = 5
    size_min = 4
    size_max = 12
    difficulty = 2
    difficulty_min = 1
    difficulty_max = 5
    seed = None
    value_min = 0
    value_max = 9
    exclude_zero = False
    
    # Printing parameter

    # unit cm
    boxw = 2
    outw = 0
    boxh = 1
    outh = 0
    # pt
    line_width = 1
    
    # ppp
    __resolution = 300
    
    # Tikz
    latex_separator = ''
    tikz_onefile = False

    units = {
            'cm' : 1,
            'mm':  1/10,
            'inch': 2.54,
            'pt': 2.54/72.27,
            # change it changing resolution
            'px': 2.54/__resolution
            }
    
    scale = 1
    unit = 'cm'
    
    def __init__(self, **kwargs):
        self.__output_directory = sp.writableLocation(sp.DocumentsLocation) or '.'
        for k, v in kwargs:
            setattr(self,k,v)
    
    def u(self, length, *, to_unit = None, scale = None):
        """
        change value cm to unit
        and scale by self.scale
        """
        to_unit = to_unit or self.unit
        scale = scale or self.scale
        return length*scale/self.units[to_unit]
    
    def pt(self,val):
        """
        change from pt to unit
        used for text size and line width
        """
        return round(self.u(val*2.54/72.27))
    
    def n_values(self):
        """ 
        return the numbers of values in the pyramid
        """
        return self.size*(self.size+1)//2

    @property
    def resolution(self):
        return self.__resolution

    @resolution.setter
    def resolution(self, r):
        # ignore if none
        try:
            r = int(r)
        except:
            return
        if r:
            self.__resolution = r
            self.units['px'] = 2.54/r
    @property
    def extension(self):
        return self.__extension if self.__extension else self.default_extension
    
    @extension.setter
    def extension(self, ext):
        self.__extension = ext
    
    @property
    def filename(self):
        pext = f".{self.ext}" if self.ext else ''
        if self.use_timestamp:
            timestamp = strftime('-%Y%m%dT%H%M%S')
            return str(Path(self.output_directory, f"{self.basename}{timestamp}{pext}"))
        
    @filename.setter
    def filename(self, name):
        if name:
            self.basename, self.extension, dirname = filename_prepare(name, self.extensions_list, self.default_extension)
            self.output_directory = dirname if dirname else self.output_directory
        
    def get_filename(self, complement = None):
        ext = self.extension or self.default_extension
        pcomplement = f"-{complement}" if complement else ''
        if self.use_timestamp:
            timestamp = strftime('-%Y%m%dT%H%M%S')
        else:
            timestamp = ''
        return str(Path(self.output_directory, f"{self.basename}{timestamp}{pcomplement}.{ext}"))
    @property
    def output_directory(self):
        return self.__output_directory
    
    @output_directory.setter
    def output_directory(self, dirname):
        if dirname:
            pdir = Path(dirname)
            if pdir.is_dir():
                self.__output_directory = dirname
            
class PrinterCoordinates:
    """
    Automagicly change x et y properties to
    unit given by parameters class
    """
    def __init__(self, parameters):
        self.param = parameters
        self.shift = self.param.outw or self.param.outh

    def __str__(self):
        return f" {self.__x}, {self.__y} "

    def __iter__(self):
        yield self.__x
        yield self.__y
        
    __x = None
    __y = None
    __shift = False
    __shift_x = 0
    __shift_y = 0


    def __round__(self):
        return round(self.__x), round(self.__y)

    @property
    def shift(self):
        return self.__shift
    
    @shift.setter
    def shift(self, bool):
        self.__shift = bool
        if bool:
            self.__shift_x = self.param.u(self.param.outw)
            self.__shift_y = self.param.u(self.param.outh)
        else:
            self.__shift_x = 0
            self.__shift_y = 0
            

    @property
    def xy(self):
        return self.__x+self.__shift_x, self.__y + self.__shift_y
    
    @xy.setter
    def xy(self, coord):
        self.x = coord[0]
        self.y = coord[1]
        
    @property
    def x(self):
        return self.__x+self.__shift_x
    
    @x.setter
    def x(self, val):
        self.__x = self.param.u(val)
        
    @property
    def y(self):
        return self.__y+self.__shift_y

    @y.setter
    def y(self, val):
        self.__y = self.param.u(val)
        
