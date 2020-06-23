"""
Tool for generating stub.c files that work with k3stubproxy from implemented stub.c files
"""

import argparse
import os
import logging
import json
import k3logging

from k3stubproxy import __version__, stub_target_generator

__author__ = 'Joachim Kestner <joachim.kestner@khoch3.de>'

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description=__doc__+"\n\nAuthor: {}\nVersion: {}".format(__author__,__version__), formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-o", "--output", help="Ouput file. If not set result will be printed to stdout")
    parser.add_argument("function_definition_json",help="The function definition json file")
    
    k3logging.set_parser_log_arguments(parser)
    
    args = parser.parse_args()
    
    k3logging.eval_parser_log_arguments(args)
    
    if not os.path.isfile(args.function_definition_json):
        raise RuntimeError("function_definition_json is not a file")
    
    with open(args.function_definition_json) as fh:
        data = json.load(fh)
    
    stub_target_generator.generate_target_stub(data, args.output)