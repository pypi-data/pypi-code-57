# -*- coding: utf-8 -*-
# @author: leesoar
# @email: secure@tom.com
# @email2: employ@aliyun.com

import argparse

from crack import __version__

parser = argparse.ArgumentParser(description=f"Crack everything.", prog="crack", add_help=False)
parser.add_argument('-v', '--version', action='version', version=__version__, help='Get version of anole')
parser.add_argument('-h', '--help', action='help', help='Show help message')
parser.parse_args()


def run():
    return "Powered by leesoar.com"
