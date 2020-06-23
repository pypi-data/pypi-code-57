"""
Tool for generating stub.c files that work with k3stubproxy from implemented stub.c files
"""

import argparse
import os
import logging
import k3logging

import k3stubproxy
from k3stubproxy import __version__, stub_generator

__author__ = 'Joachim Kestner <joachim.kestner@khoch3.de>'

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description=__doc__+"\n\nAuthor: {}\nVersion: {}".format(__author__,__version__), formatter_class=argparse.RawDescriptionHelpFormatter)
#     parser.add_argument("-f", "--flag", action="store_true", help="Example argparse of a choice")
#     parser.add_argument("-c", "--choice", default="c1", choices=["c1", "c2", "c3", "c4"], help="Example of an argparse choice argument")
    parser.add_argument("--func_prefix", help="A function prefix that will, if set, only stub functions that match this prefix. Can be a list of comma seperated values.")
    parser.add_argument("--filename_suffix", help="A suffix that is added before the extension for created files")
    parser.add_argument("--file_header", help="Path to a file whose contents will become the initial part of each file. Use for generic includes.")
    parser.add_argument("--stub_function_definition_out", default="stub_function_definition.json", help="File path to which the stub function definition will be written to as json. Default: stub_function_definition.json")
    parser.add_argument("-o", "--output", default=".", help="Output directory. Default is .")
    parser.add_argument("files", nargs='+', help="One or more files to be parsed for stub creation")
    
    k3logging.set_parser_log_arguments(parser)
    
    args = parser.parse_args()
    
    k3logging.eval_parser_log_arguments(args)
    
    if not os.path.isdir(args.output):
        raise RuntimeError("Output is not a directory")
    
    fileHeaderLines = []
    if args.file_header:
        with open(args.file_header) as fh:
            fileHeaderLines = fh.readlines()
    
    functionPrefixes = []
    if args.func_prefix:
        functionPrefixes = args.func_prefix.split(",") 
    
    # call the actual 'business' logic here
    # Note: Having the main logic within a library enables another project to use
    # the implemented functionalities directly through importing the installed library
    stub_generator.generate_stubs(args.files, args.output, fileHeaderLines, functionPrefixes, args.filename_suffix, args.stub_function_definition_out)
