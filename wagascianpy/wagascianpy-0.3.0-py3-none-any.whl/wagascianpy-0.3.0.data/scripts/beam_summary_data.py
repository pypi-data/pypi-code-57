#!python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

# Python modules
import argparse
import textwrap

# user
import wagascianpy.analysis.beam_summary_data


###############################################################################
#                                  arguments                                  #
###############################################################################

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(usage='use "python %(prog)s --help" for more information',
                                     argument_default=None, description=textwrap.dedent('''\
                                     Add BSD info to the WAGASCI decoded file. The decoded file must contain
                                     the fixed_spill_number branch and all other branches created by the
                                     wgSpillNumberFixer program. '''))

    PARSER.add_argument('-f', '--input-file', metavar='<WAGASCI raw file>', dest='input_file', type=str,
                        nargs=1, required=True, help=textwrap.dedent('''\
                        Path to a WAGASCI decoded file *_ecal_dif_X_tree.root or a directory containing those files.
                        If it is a directory all the files ending in *_ecal_dif_X_tree.root inside it will be analyzed.
                        If the "r" option is set the directory is traversed recursively.  
                        '''))

    PARSER.add_argument('-r', '--recursive', dest='recursive', required=False, default=False, action='store_true',
                        help=textwrap.dedent('''\
                        If set the input directory is scanned recursively for _ecal_dif_X_tree.root files.'''))

    PARSER.add_argument('-b', '--bsd-database', metavar='<BSD database>', dest='bsd_database', type=str,
                        nargs=1, required=True, help=textwrap.dedent('''\
                        Path to the Beam Summary Data database file. This file is created by the 
                        Wagasci Database Viewer (wagascidb_viewer.py) program and is usually called bsddb.db.
                        '''))
    PARSER.add_argument('-p', '--bsd-repository', metavar='<BSD repository>', dest='bsd_repository', type=str,
                        nargs=1, required=False, help=textwrap.dedent('''
                        Path to the Beam Summary Data local repository. This repository is just a folder 
                        containing all the BSD files. The repository must contain multiple subfolders each one 
                        named t2kXrun where X is the T2K run number.
                        '''))
    PARSER.add_argument('-t', '--t2krun', metavar='<T2K run>', dest='t2krun', type=int,
                        nargs=1, help='T2K run number (default is 10)', default=10, required=False)

    ARGS = PARSER.parse_args()

    if isinstance(ARGS.input_file, list):
        ARGS.input_file = ARGS.input_file[0]
    INPUT_FILE = ARGS.input_file

    if isinstance(ARGS.bsd_database, list):
        ARGS.bsd_database = ARGS.bsd_database[0]
    BSD_DATABASE = ARGS.bsd_database

    if isinstance(ARGS.bsd_repository, list):
        ARGS.bsd_repository = ARGS.bsd_repository[0]
    BSD_REPOSITORY = ARGS.bsd_repository

    if isinstance(ARGS.t2krun, list):
        ARGS.t2krun = ARGS.t2krun[0]
    T2KRUN = ARGS.t2krun

    RECURSIVE = ARGS.recursive

    wagascianpy.analysis.beam_summary_data.beam_summary_data(INPUT_FILE, BSD_DATABASE, BSD_REPOSITORY, T2KRUN,
                                                             RECURSIVE)
