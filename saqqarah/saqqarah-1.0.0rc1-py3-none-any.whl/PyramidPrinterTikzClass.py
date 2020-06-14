#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 23:37:07 2020

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

from . import PyramidPrinter
from . import PrinterCoordinates
from . import ensure_attr

import os, sys

class PyramidPrinterTikz(PyramidPrinter):
    """ 
    implements printing in tikz
    """
    def __init__(self, pyramid, param):
        super().__init__(pyramid, param)
        param.default_extension = 'tex'
        self.unit = 'cm'

    def print_pyramid(self, param):
        for i in range(param.size):
            y = param.size - i 
            self.__print_line__(y, i+1, param)

    def __add_line_out__(self, line, param):
        param.printer.put(line, param)

    def __print_line__(self, y, no, param):
        for x in range(param.size-no, param.size+no,2):
            self.__print_box__(x,y, param)
            self.__print_node__(x,y, param)
            
    def __print_box__(self, x, y, param):
        # Python is cool
        c1, c2, c3, c4 = (PrinterCoordinates(param) for c in range(4))
        c1.xy = x, y
        c2.xy = x + param.boxw, y
        c3.xy = x + param.boxw, y - param.boxh
        c4.xy = x, y - param.boxh
        self.__add_line_out__(fr"\draw [line width={param.line_width}pt] ({c1})--({c2})--({c3})--({c4})--cycle;", param)

    def __print_node__(self, x, y, param):
        if not param.values:
            return
        value = param.values.pop()
        if value == "_":
            return

        c = PrinterCoordinates(param)
        c.xy = x + param.boxw/2, y - param.boxh/2

        # puzzle
        if type(value) is str:
            color="[text=red]"
        else:
            color=""
        self.__add_line_out__(f"\\draw ({c}) node{color} \u007b ${value}$ \u007d ;", param)

    class PrinterCM(PyramidPrinter.PrinterCM):
        def  __init__(self, printer):
            # if filename does not open to a file clone sys.stdout
            self.param = printer.param
            self.out = { stream: "" for stream in self.param.streams }
 
        def __enter__(self):
           # dict of out strings for each pyramid
           return self
            
        def __exit__(self, *args):
            if self.param.tikz_onefile:
                filename = self.param.get_filename()
                try:
                    self.file = open(filename, "w")
                except Exception as e:
                    # PermissionError or FileNotFoundError
                    #print(f"Error {e}: {filename}")
                    filename=None
                    self.file = os.fdopen(os.dup(sys.stdout.fileno()),"w")

                with self.file as f:
                    for stream in self.param.streams:
                        f.write(self.out[stream])
                        f.write("\n")
                if filename:
                    self.param.log(f"Tikz code written in {filename}")
                else:
                    self.param.log(f"% Tikz code written in standard output.")
            else:
                # two files: puzzle and solution
                for stream in self.param.streams:
                    filename = self.param.get_filename(stream.lower())
                    try:
                        self.file = open(filename, "w")
                    except Exception as e:
                        # PermissionError or FileNotFoundError
                        #print(f"Error {e}: {filename}")
                        filename=None
                        self.file = os.fdopen(os.dup(sys.stdout.fileno()),"w")
                        
                    with self.file as f:
                        f.write(self.out[stream])
                        f.write("\n")
                        
                    if filename:
                        self.param.log(f"Tikz code written in {filename}")
                    else:
                        self.param.log(f"% Tikz code for {stream} written in standard output.")
                
        def put(self, line, param):
            self.out[param.stream] += line + '\n'

    class PyramidCM(PyramidPrinter.PyramidCM):
        def __init__(self, printer):
            self.param = printer.param
        
        def __enter__(self):
            stream = self.param.stream

            #add eventually a separator before each pyramid but first
            index = self.param.index
            ensure_attr(self.param, 'latex_separator', '')
            if index > 0:
                self.param.printer.put(self.param.latex_separator, self.param)

            # begin tikz image
            self.param.printer.put(f"%% {stream}", self.param)
            self.param.printer.put(r"\begin{tikzpicture}", self.param)

        def __exit__(self, *args):
            # end tikz image
            self.param.printer.put(r"\end{tikzpicture}", self.param)
    
