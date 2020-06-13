#!python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

# Python modules
import argparse
import textwrap

# user
import wagascianpy.analysis.mhistory2sqlite


###############################################################################
#                                  arguments                                  #
###############################################################################

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(usage='use "python %(prog)s --help" for more information',
                                     argument_default=None, description=textwrap.dedent('''\
                                     Convert MIDAS history files .hst to SQLite format .sqlite3'''))

    PARSER.add_argument('-f', '--input-folder', metavar='<input folder>', dest='input_folder', type=str,
                        nargs=1, required=True, help=textwrap.dedent('''\
                        Path to a folder containing all the .hst files. If you want to convert a single file
                        please use the mh2sql utility bundled with MIDAS.'''))

    PARSER.add_argument('-r', '--recursive', dest='recursive', required=False, default=False, action='store_true',
                        help=textwrap.dedent('''\
                        If set the input directory is scanned recursively for .hst files.'''))

    PARSER.add_argument('-o', '--output-folder', metavar='<output folder>', dest='output_folder', type=str,
                        nargs=1, required=False, default=None, help=textwrap.dedent('''\
                        Output folder where the .sqlite3 files are saved (default is same as input)
                        '''))

    PARSER.add_argument('-a', '--start-time', metavar='<start time>', dest='start_time', type=str,
                        nargs=1, help='Start date and time in the format "%%Y/%%m/%%d %%H:%%M:%%S"', default=None,
                        required=False)

    PARSER.add_argument('-z', '--stop-time', metavar='<stop time>', dest='stop_time', type=str,
                        nargs=1, help='Stop date and time in the format "%%Y/%%m/%%d %%H:%%M:%%S"', default=None,
                        required=False)

    ARGS = PARSER.parse_args()

    if isinstance(ARGS.input_folder, list):
        ARGS.input_folder = ARGS.input_folder[0]
    INPUT_FOLDER = ARGS.input_folder
    if isinstance(ARGS.output_folder, list):
        ARGS.output_folder = ARGS.output_folder[0]
    OUTPUT_FOLDER = ARGS.output_folder
    if isinstance(ARGS.start_time, list):
        ARGS.start_time = ARGS.start_time[0]
    START_TIME = ARGS.start_time
    if isinstance(ARGS.stop_time, list):
        ARGS.stop_time = ARGS.stop_time[0]
    STOP_TIME = ARGS.stop_time
    RECURSIVE = ARGS.recursive

    wagascianpy.analysis.mhistory2sqlite.mhistory2sqlite(input_path=INPUT_FOLDER, output_folder=OUTPUT_FOLDER,
                                                         start_time=START_TIME, stop_time=STOP_TIME, recursive=RECURSIVE)
