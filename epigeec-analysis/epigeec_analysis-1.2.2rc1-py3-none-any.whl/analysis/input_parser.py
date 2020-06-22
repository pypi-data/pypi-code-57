from __future__ import absolute_import, division, print_function

import argparse

from .config import VERSION, NAME, DESCRIPTION
from .annotate.parser import AnnotateParser
from .ari.parser import EvaluateParser
from .slice.parser import SliceFilenameParser, SliceClusterParser
from .util.parser import CatParser, GrepParser

class InputParser(object):
    @staticmethod
    def parse_args(args):
        parser = argparse.ArgumentParser(prog=NAME, description = DESCRIPTION)
        parser.add_argument('-v', '--version', action='version', version='%(prog)s {0}'.format(VERSION))
        subparsers = parser.add_subparsers(help = "Sub-command help.")

        AnnotateParser.add_parser(subparsers)
        EvaluateParser.add_parser(subparsers)
        SliceFilenameParser.add_parser(subparsers)
        SliceClusterParser.add_parser(subparsers)
        CatParser.add_parser(subparsers)
        GrepParser.add_parser(subparsers)
        
        return parser.parse_args(args)
