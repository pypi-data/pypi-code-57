#! /usr/bin/env python

# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

# System imports
from __future__ import (print_function, division, absolute_import,
                        unicode_literals)
# package imports
import argparse
from esub import utils
from ekit.logger import vprint
from ekit import logger as logger_utils

LOGGER = logger_utils.init_logger(__file__)

# parse from arguments
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('--log_dir', type=str, default='')
parser.add_argument('--test', action='store_true', default=False)
parser.add_argument('--job_name', type=str, default='')
parser.add_argument('--executable', type=str, required=True)
parser.add_argument('--main_name', type=str, required=True)
parser.add_argument('--tasks', type=str, required=True,
                    help='has to be a single task!')
args, function_args = parser.parse_known_args()

try:
    from mpi4py import MPI
    is_master = MPI.COMM_WORLD.rank == 0
except ImportError:
    if args.test:
        is_master = False
    else:
        raise ImportError(
            "You are attempting to run a MPI job. This requires a local "
            "MPI environement as well as the mpi4py package")


job_name = args.job_name
main_name = args.main_name
log_dir = args.log_dir
exe = args.executable
tasks = int(args.tasks)

# get path of log file
if log_dir != '':
    path_log = utils.get_path_log(log_dir, job_name)

executable = utils.import_executable(exe, verbose=is_master)
utils.cd_local_scratch(verbose=is_master)  # Change to local scratch if set

if is_master:
    vprint(
        "##################### Running main function in MPI\
         environment #####################",
        logger=LOGGER, verbose=True)
    if log_dir != '':
        utils.write_to_log(path_log, 'Running {}'.format(main_name))

getattr(executable, main_name)([tasks], function_args).__next__()

if is_master:
    if log_dir != '':
        utils.write_to_log(path_log, 'Finished running {}'.format(main_name))
