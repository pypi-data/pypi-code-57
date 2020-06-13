#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio
#

import argparse
import textwrap
from typing import List


def parse_args(args):
    # type: (List[str]) -> argparse.Namespace
    parser = argparse.ArgumentParser(usage='use "python %(prog)s --help" for more information',
                                     argument_default=None, description=textwrap.dedent('''\
                                     WAGASCI run database and BSD database viewer and manager. If you wish to use the
                                     script arguments from shell, please run in batch mode (option -x). Be carefull 
                                     that all the arguments accept no more than one value and any additional value is 
                                     discarded.'''))

    parser.add_argument('-x', '--batch-mode', dest='batch_mode', required=False,
                        default=False, action='store_true', help=textwrap.dedent('''\
                        Do not run the graphical interface. (default: %(default)s)'''))

    parser.add_argument('-wr', '--wagasci-repository', metavar='<WAGASCI repository location>',
                        dest='wagasci_repository', type=str, nargs=1, required=False, help=textwrap.dedent('''\
                        Path to a WAGASCI run repository location. Can be a simple repository or a borg repository.
                        The path can be also a remote path of the form <SSH alias>:/path/to/repository where the SSH
                        alias is the one defined in the .ssh/config file. (default: %(default)s)'''))

    parser.add_argument('-s', '--simple-wagasci-repository', dest='simple_wagasci_repository', required=False,
                        default=False, action='store_true', help=textwrap.dedent('''\
                        If set the WAGASCI run repository is assumed to be a simple repository (no encription) 
                        (default: %(default)s)'''))

    parser.add_argument('-b', '--borg-wagasci-repository', dest='borg_wagasci_repository', required=False,
                        default=False, action='store_true', help=textwrap.dedent('''\
                        If set the WAGASCI run repository is assumed to be a borg repository (default: %(default)s)'''))

    parser.add_argument('-wup', '--update-wagasci-database', dest='update_wagasci_database', required=False,
                        default=False, action='store_true', help=textwrap.dedent('''\
                        If set the WAGASCI database is updated (new runs are added but existing runs are not 
                        modified) (default: %(default)s)'''))

    parser.add_argument('-wrb', '--rebuild-wagasci-database', dest='rebuild_wagasci_database', required=False,
                        default=False, action='store_true', help=textwrap.dedent('''\
                        If set the WAGASCI database is rebuilt (all runs are overwritten) (default: %(default)s)'''))

    parser.add_argument('-wd', '--wagasci-database', metavar='<WAGASCI database location>', dest='wagasci_database',
                        type=str, nargs=1, required=False, help=textwrap.dedent('''\
                        Path to the Beam Summary Data database file. This file is created by the 
                        Wagasci Database Viewer (wagascidb_viewer.py) program and is usually called bsddb.db.
                        The path can be also a remote path of the form <SSH alias>:/path/to/database where the SSH
                        alias is the one defined in the .ssh/config file. (default: %(default)s)
                        '''))

    parser.add_argument('-wl', '--wagasci-libdir', metavar='<WAGASCI library location>', dest='wagasci_libdir',
                        type=str, nargs=1, required=False, help=textwrap.dedent('''\
                        Path to the WAGASCI library directory. Only local paths are supported. 
                        (default: %(default)s)'''))

    parser.add_argument('-br', '--bsd-repository', metavar='<BSD repository location>', dest='bsd_repository', type=str,
                        nargs=1, required=False, help=textwrap.dedent('''
                        Path to the Beam Summary Data local repository. This repository is just a folder 
                        containing all the BSD files. The repository must contain multiple subfolders each one 
                        named t2kXrun where X is the T2K run number. The path can be also a remote path of the form 
                        <SSH alias>:/path/to/repository where the SSH alias is the one defined in the .ssh/config file.
                         (default: %(default)s)'''))

    parser.add_argument('-bd', '--bsd-database', metavar='<BSD database location>', dest='bsd_database', type=str,
                        nargs=1, required=False, help=textwrap.dedent('''\
                        Path to the Beam Summary Data database file. This file is created by the 
                        Wagasci Database Viewer (wagascidb_viewer.py) program and is usually called bsddb.db.
                        The path can be also a remote path of the form <SSH alias>:/path/to/database where the SSH
                        alias is the one defined in the .ssh/config file. (default: %(default)s)
                        '''))

    parser.add_argument('-bf', '--bsd-download-location', metavar='<BSD database download location>',
                        dest='bsd_download_location', type=str, nargs=1, required=False,
                        help=textwrap.dedent('''\
                        Folder where to download BSD files when updating or rebuilding the BSD database
                         (default: %(default)s)
                        '''))

    parser.add_argument('-bup', '--update-bsd-database', dest='update_bsd_database', required=False,
                        default=False, action='store_true', help=textwrap.dedent('''\
                        If set the BSD database is updated (new runs are added but existing runs are not 
                        modified) (default: %(default)s)'''))

    parser.add_argument('-brb', '--rebuild-bsd-database', dest='rebuild_bsd_database', required=False,
                        default=False, action='store_true', help=textwrap.dedent('''\
                        If set the BSD database is rebuilt (all runs are overwritten) (default: %(default)s)'''))

    parser.add_argument('-d', '--wagasci-download-location', metavar='<WAGASCI runs download location>',
                        dest='wagasci_download_location', type=str, nargs=1, required=False, help=textwrap.dedent('''
                        Local directory where the WAGASCI runs are downloaded. (default: %(default)s)'''))

    parser.add_argument('-sf', '--wagasci-decoded-location', metavar='<WAGASCI decoded save location>',
                        dest='wagasci_decoded_location', type=str, nargs=1, required=False, help=textwrap.dedent('''
                        Local directory where the decoded data is stored. (default: %(default)s)'''))

    parser.add_argument('-tsd', '--temperature-sqlite-database', metavar='<temperature SQLite database>',
                        dest='temperature_sqlite_database', type=str, nargs=1, required=False, help=textwrap.dedent('''
                        Local SQLite3 database where all the temperature and humidity readings are stored.
                         (default: %(default)s)'''))

    parser.add_argument('-dql', '--data-quality-folder', metavar='<data quality location>',
                        dest='data_quality_location', type=str, nargs=1, required=False, help=textwrap.dedent('''
                        Local folder where to store output of wgDataQuality program.(default: %(default)s)'''))

    parser.add_argument('-t', '--t2krun', metavar='<T2K run>', dest='t2krun', type=int,
                        nargs=1, help='T2K run number (default: %(default)s)', default=10, required=False)

    parser.add_argument('-at', '--start-time', metavar='<start time>', dest='start_time', type=str,
                        nargs=1, required=False, help=textwrap.dedent('''
                        Start date and time in the form YYYY/MM/DD HH:MM:SS
                        '''))

    parser.add_argument('-ot', '--stop-time', metavar='<stop time>', dest='stop_time', type=str,
                        nargs=1, required=False, help=textwrap.dedent('''
                        Stop date and time in the form YYYY/MM/DD HH:MM:SS
                        '''))

    parser.add_argument('-ar', '--start-run', metavar='<start run>', dest='start_run', type=int,
                        nargs=1, default=0, required=False, help=textwrap.dedent('''Start run number'''))

    parser.add_argument('-or', '--stop-run', metavar='<stop run>', dest='stop_run', type=int,
                        nargs=1, default=0, required=False, help=textwrap.dedent('''Stop run number'''))

    parser.add_argument('-g', '--only-good-runs', dest='only_good_runs', required=False,
                        default=False, action='store_true', help=textwrap.dedent('''\
                        If set select only good runs (default: %(default)s)'''))

    parser.add_argument('-i', '--include-overlapping', dest='include_overlapping', required=False,
                        default=False, action='store_true', help=textwrap.dedent('''\
                        If set include the runs that overlap within the interval (default: %(default)s)'''))

    parser.add_argument('-do', '--download', dest='download', required=False,
                        default=False, action='store_true', help=textwrap.dedent('''\
                        Download the runs selected by the --get-all and --get-interval arguments'''))

    parser.add_argument('-dcd', '--decoder', dest='decoder', required=False,
                        default=False, action='store_true', help=textwrap.dedent('''\
                        Decode the runs selected by the --get-all and --get-interval arguments'''))

    parser.add_argument('-snf', '--spill-number-fixer', dest='spill_number_fixer', required=False,
                        default=False, action='store_true', help=textwrap.dedent('''\
                        Fix the spill number for the runs selected by the --get-all and --get-interval arguments'''))

    parser.add_argument('-bsd', '--beam-summary-data', dest='beam_summary_data', required=False,
                        default=False, action='store_true', help=textwrap.dedent('''\
                        Integrate Beam Summary Data into the runs selected by the --get-all and
                         --get-interval arguments'''))

    parser.add_argument('-dq', '--data-quality', dest='data_quality', required=False,
                        default=False, action='store_true', help=textwrap.dedent('''\
                        Run data quality program for the runs selected by the --get-all and
                         --get-interval arguments. Recommended to use for a total period of roughly one week.'''))

    parser.add_argument('-temp', '--temperature', dest='temperature', required=False,
                        default=False, action='store_true', help=textwrap.dedent('''\
                        Merge the temperature and humidity for the runs selected by the --get-all and
                         --get-interval arguments. This analyzer must be run after the beam-summary-data analyzer.'''))

    parser.add_argument('-aa', '--all-analyzers', dest='all_analyzers', required=False,
                        default=False, action='store_true', help=textwrap.dedent('''\
                        Apply all analyzers to the runs selected by the --get-all and --get-interval arguments'''))

    parser.add_argument('-ov', '--overwrite-flag', dest='overwrite_flag', required=False,
                        default=False, action='store_true', help=textwrap.dedent('''\
                        When applying analyzers use the overwrite_flag flag if present'''))

    # Flatten all arguments
    parsed_args = parser.parse_args(args=args)
    for name, value in vars(parsed_args).items():
        if isinstance(value, list):
            setattr(parsed_args, name, value[0])

    return parsed_args
