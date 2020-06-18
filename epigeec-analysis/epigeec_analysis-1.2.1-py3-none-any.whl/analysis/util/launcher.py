from __future__ import absolute_import, division, print_function

from .cat import run as run_cat
from .grep import run as run_grep

def select_unique_identifier(arg):
    if arg:
        unique_identifier = 'md5sum'
    else:
        unique_identifier = 'file_name'
    return unique_identifier

class CatLaucher(object):
    @staticmethod
    def run(args):
        run_cat(args.input, select_unique_identifier(args.md5sum))

class GrepLauncher(object):
    @staticmethod
    def run(args):
        run_grep(
            args.inputs,
            args.pattern,
            args.e,
            args.f,
            args.v,
            select_unique_identifier(args.md5sum)
        )
