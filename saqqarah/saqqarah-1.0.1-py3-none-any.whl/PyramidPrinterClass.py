#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 23:33:40 2020

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

from . import Parameters, ensure_attr
        
class PyramidPrinter:
    """
        base class for printing pyramid
        
        mask in subclass:
            - PrinterCM: contextmanager for all printing
            - PyramidCM: context manager for one pyramid printing
    """
    def __init__(self, pyramid, param):
        self.pyramid = pyramid
        self.param = param

    class PrinterCM:
        def __init__(self, printer):
            """
            Initialisation code for the printer itself
            **kwargs are passer from self.printer
            Implement in subclass
            """
            raise NotImplementedError("Don't use directly this class !")

        def __enter__(self):
            """
            Enter code for the printer
            Implement in subclass
            """
            raise NotImplementedError("Don't use directly this class !")

        def __exit__(self, *args):
            """
            finalization code for the printer
            Implement in subclass
            """

            raise NotImplementedError("Don't use directly this class !")

    class PyramidCM:
        def __init__(self, printer):
            """
            Initialisation code for the pyramid printing
            **kwargs are passer from self.printer
            Implement in subclass
            """
            raise NotImplementedError("Don't use directly this class !")

        def __enter__(self):
            """
            Enter code for the pyramid printing
            Implement in subclass
            """
            raise NotImplementedError("Don't use directly this class !")

        def __exit__(self, *args):
            """
            Enter code for the printer printing
            Implement in subclass
            """
            raise NotImplementedError("Don't use directly this class !")
            

    def print(self):
        # check unit is ok
        if hasattr(self, 'unit'):
            self.param.unit = self.unit

        # TODO: UGLY ! CLEAN THAT
        self.param.pyramid_puzzle = self.pyramid.puzzle
        self.param.pyramid_solution  = self.pyramid.solution
        self.param.log = self.pyramid.log

        # puzzle and solution are boolean to know
        # what must be printed
        # TODO clean that (print_puzzle e.g.)        
        puzzle = self.param.puzzle if hasattr(self.param, 'puzzle') else True
        solution = self.param.solution if hasattr(self.param, 'solution') else True
        
        if puzzle and not self.param.pyramid_puzzle:
            puzzle = False
        if solution and self.param.pyramid_solution == []:
            solution = False

        self.param.streams = ['NoPuzzle'] if not puzzle and not solution else []
        self.param.streams += ['Puzzle'] if puzzle else []
        self.param.streams += [ 'Solution' ] if solution else []
        
        with self.PrinterCM(self) as printer:
            for index, stream in enumerate(self.param.streams):
                self.param.values = self.__set_values__(stream)
                self.param.index = index
                self.param.stream = stream
                self.param.printer = printer

                with self.PyramidCM(self) as pyramid_printer:
                    self.param.pyramid_printer = pyramid_printer
                    self.print_pyramid(self.param)

    def __set_values__(self, stream):
        """
        prepare list of values to print in cases for output
        """
        if stream == 'Puzzle':
            values = []
            for k in range(self.param.n_values()):
                values.append(
                        self.param.pyramid_puzzle[k] 
                        if k in self.param.pyramid_puzzle 
                        else '_'
                        )
        elif stream == 'Solution':  
            values = [ int(n) for n in self.param.pyramid_solution ]
            # change type if case is in puzzle
            # str will be type of puzzle values
            # used to change color in solution
            for k in self.param.pyramid_puzzle:
                values[k] = str(values[k])
        else:
            values = ['_'] * self.param.n_values()
        return values
                        
    def print_pyramid(self):
        """
        Implement in the subclass
        self.values as values to print, or '_'
        self.size as size of the pyramid
        self.current_stream is 'puzzle' or 'solution'
        """
        raise NotImplementedError("Don't use directly this class !")
           
            
        