#!/usr/bin/env python
# -*- encoding: utf8 -*-
"""\033[1;3;32m
    CMS Crawler for Novogene
\033[0m"""
import os
import sys
import getpass
import argparse

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
PKG_PATH = os.path.dirname(os.path.dirname(BASE_DIR))
sys.path.insert(0, PKG_PATH)

from cms.util.lims.lims import parser_add_lims
from cms.util.report.report import parser_add_report
from cms.util.cms.project import parser_add_cms
from cms.util.settlement.settlement import parser_add_settlement


__author__ = 'suqingdong'
__author_email__ = 'suqingdong@novogene.com'

__version__ = '1.0.15'


def check_update():
    pass


def main():

    parser = argparse.ArgumentParser(
        prog='cms',
        description=__doc__,
        usage='%(prog)s [OPTIONS]',
        epilog='contact: {__author__} <{__author_email__}>'.format(
            **globals()),
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-v', '--version', action='version', version=__version__)
    parser.add_argument('-u', '--username', help='the username to login CMS')
    parser.add_argument('-p', '--password', help='the password to login CMS')

    parser.add_argument(
        '-c',
        '--configfile',
        help='the config file to login CMS[default: %(default)s]',
        default=os.path.join(os.path.expanduser('~'), '.cms.ini'))

    parser.add_argument(
        '-debug',
        '--verbose',
        action='store_true',
        help='logging in debug mode')

    parser.add_argument(
        '-log',
        '--logfile',
        help='output logging to a file [stdout]')


    # 子命令
    subparser = parser.add_subparsers(
        title='sub-commands',
        dest='subparser_name',
        metavar='')

    parser_cms = subparser.add_parser(
        'project',
        formatter_class=argparse.RawTextHelpFormatter,
        help='show project informations')
    parser_add_cms(parser_cms)

    parser_report = subparser.add_parser(
        'report',
        formatter_class=argparse.RawTextHelpFormatter,
        help='get the report excel')
    parser_add_report(parser_report)

    parser_lims = subparser.add_parser(
        'lims',
        formatter_class=argparse.RawTextHelpFormatter,
        help='get lims data')
    parser_add_lims(parser_lims)

    parser_settlement = subparser.add_parser(
        'settlement',
        formatter_class=argparse.RawTextHelpFormatter,
        help='parse settlement report')
    parser_add_settlement(parser_settlement)

    if not sys.argv[1:]:
        parser.print_help()
        exit()

    args = parser.parse_args()

    args.func(**vars(args))


if __name__ == '__main__':
    main()
