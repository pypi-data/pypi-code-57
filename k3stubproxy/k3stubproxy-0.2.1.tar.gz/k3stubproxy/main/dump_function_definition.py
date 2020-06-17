"""
Get function and types list out of stub definition json
"""

import argparse
import os
import logging
import k3logging

from k3stubproxy import __version__
import json

__author__ = 'Joachim Kestner <joachim.kestner@khoch3.de>'

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description=__doc__+"\n\nAuthor: {}\nVersion: {}".format(__author__,__version__), formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("function_definition_json",help="The function definition json file")
    
    k3logging.set_parser_log_arguments(parser)
    
    args = parser.parse_args()
    
    k3logging.eval_parser_log_arguments(args)
    
    if not os.path.isfile(args.function_definition_json):
        raise RuntimeError("function_definition_json is not a file")
    
    with open(args.function_definition_json) as fh:
        data = json.load(fh)
    
    funks = data.keys();  
    print(f"Functions {len(funks)}:")
    print("\n".join((funks)))
    
    print("")    
    typeSet = set()
    inTypeSet = set()
    outTypeSet = set()
    returnTypeSet = set()
    
    for k, funcDict in data.items():
        prmList = funcDict["parameters"]
        returnTypeSet.add(funcDict["return"])
        for prm in prmList:
            (nm, io, typ) = prm
            typeSet.add(typ)
            if io == "in":
                inTypeSet.add(typ)
            else:
                outTypeSet.add(typ)
#     print(f"Types ({len(typeSet)}):")
#     print("\n".join(sorted(list(typeSet))))
    
    print("")
    print(f"Types input ({len(inTypeSet)}):")
    print("\n".join(sorted(list(inTypeSet))))
    
    print("")
    print(f"Types output ({len(outTypeSet)}):")
    print("\n".join(sorted(list(outTypeSet))))
    
    print("")
    print(f"Types return ({len(returnTypeSet)}):")
    print("\n".join(sorted(list(returnTypeSet))))
    
    
    
