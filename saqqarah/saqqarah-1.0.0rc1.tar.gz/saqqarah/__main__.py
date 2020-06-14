#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 23:48:15 2020

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

import argparse

from saqqarah import Pyramid,PyramidPrinterTikz, PyramidPrinterImage, Parameters, PrinterCoordinates, version, codename

def main():
    parser = argparse.ArgumentParser(description=f"Calculation pyramid generator, version {version()} {codename()}" )
    parser.add_argument("-s", "--size", type=int, default=5,
                    help="Piramid size (4 or more) (default: 5)")
    parser.add_argument("-d", "--difficulty", type=int, choices=range(1,6), default=2,
                    help="difficlty level (max 3 if size is 4) (default: 2)")
    parser.add_argument("-m", "--min", type=int, default=0,
                    help="minimum number in base (default: 0)")    
    parser.add_argument("-M", "--max", type=int, default=9,
                    help="maximum number in base (default: 9)")    
    parser.add_argument("-z", "--non-zero", dest='exclude_zero', default=False, action='store_true',
                    help="exclude zeros from base numbers (default: False)")
    parser.add_argument("-S", "--seed", type=int,
                    help="Seed number for random generator")
    parser.add_argument("-E", "--empty", dest='empty', default=False, action='store_true',
                    help="Print an empty pyramid")
    parser.add_argument('--version', action='version', version=f'%(prog)s {version()} {codename()}')
    subparsers = parser.add_subparsers(help='choose output mode (without: list the boxes & values)')
    parser_img = subparsers.add_parser('image', help=f'generate image output ("%(prog)s image -h" for help)')
    parser_img.set_defaults(Printer=PyramidPrinterImage)
    parser_img.add_argument("-f", "--filename", type= str, 
                    help="output schema (default: pyramid-TIME.png gives pyramid-TIME-puzzle.png and pyramid-TIME-solution.png)")
    parser_img.add_argument("-r", "--resolution", type=str,
                    help="resolution of the final images.")
    parser_img.add_argument("-d", "--directory", dest="output_directory",  type=str,
                            help="directory where write images")
    parser_img.add_argument("-t", "--no-timestamp", dest='use_timestamp', default=True, action='store_false',
                    help="Don't add timestamp in file name")
    parser_tikz = subparsers.add_parser('tikz', help=f'generate tikz output ("%(prog)s image -h" for help)')
    parser_tikz.set_defaults(Printer=PyramidPrinterTikz)
    parser_tikz.add_argument("-f", "--filename", type= str,
                    help="output name (default: pyramid-TIMESTAMP.tex)")
    parser_tikz.add_argument("-l", "--latex-separator", type=str, default="",
                    help="latex code to insert between puzzle and solution")
    parser_tikz.add_argument("-d", "--directory", dest="output_directory", type=str,
                            help="directory where write images")
    parser_tikz.add_argument("-t", "--no-timestamp", dest='use_timestamp', default=True, action='store_false',
                    help="Don't add timestamp in file name")
    parser_tikz.add_argument("-o", "--onefile", dest='tikz_onefile', default=False, action='store_true',
                    help="Tikz figures in same tex file ")
    
    args = parser.parse_args()

    # print debugging
    # print(args.__dict__)

    pyra = Pyramid(args.size)
    if not args.empty:
        pyra.get_puzzle(args.difficulty,args.min, args.max, seed=args.seed, exclude_zero=args.exclude_zero)

    # defaut directory is "Documents"
    # but in command line, default should be '.'
    if hasattr(args, 'output_directory'):
        args.output_directory = args.output_directory or '.'
    
    if hasattr(args, 'Printer'):
        param = Parameters()
        # initialise param before pass arguments
        pyraPr = args.Printer(pyra, param)

        for k,v in args.__dict__.items():
            setattr(param, k, v)

        pyraPr.print()
    
    else:
        print("""
        Boxes numeroted from top left to bottom.
        Going from left to right in each line.\n
        """)
        
        print(f"Puzzle for pyramid size {args.size} :")
        for box, value in pyra.puzzle.items():
            print(f"     box : {box+1:2d}   value : {value:4d} ")
        print(f"\nSolution :")
        for box, value in enumerate(pyra.solution):
            print(f"     box : {box+1:2d}   value : {int(value):4d} ")
        
    try:
        exit(1)
    except NameError:
        pass


