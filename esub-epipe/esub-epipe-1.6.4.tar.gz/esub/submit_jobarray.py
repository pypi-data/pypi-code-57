#! /usr/bin/env python

# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

# System imports
from __future__ import (print_function, division, absolute_import,
                        unicode_literals)

# package imports
import os
import argparse
import time
from esub import utils
import subprocess
import shlex
from ekit.logger import vprint
from ekit import logger as logger_utils

LOGGER = logger_utils.init_logger(__file__)


# parse all the submitter arguments
parser = argparse.ArgumentParser()
parser.add_argument('--job_name', type=str, required=True)
parser.add_argument('--source_file', type=str, required=True)
parser.add_argument('--main_memory', type=float, required=True)
parser.add_argument('--main_time', type=float, required=True)
parser.add_argument('--main_scratch', type=float, required=True)
parser.add_argument('--function', type=str, required=True)
parser.add_argument('--executable', type=str, required=True)
parser.add_argument('--tasks', type=str, required=True)
parser.add_argument('--n_cores', type=int, required=True)
parser.add_argument('--log_dir', type=str, required=True)
parser.add_argument('--system', type=str, required=True)
parser.add_argument('--main_name', type=str, required=True)

args, function_args = parser.parse_known_args()
function = args.function
source_file = args.source_file
job_name = args.job_name
log_dir = args.log_dir
exe = args.executable
tasks = args.tasks
n_cores = args.n_cores
main_memory = args.main_memory
main_time = args.main_time
main_scratch = args.main_scratch
system = args.system
main_name = args.main_name

# get path of log file and of file containing finished indices
path_log = utils.get_path_log(log_dir, job_name)
path_finished = utils.get_path_finished_indices(log_dir, job_name)

TIMEOUT_MESSAGE = 'Maximum number of pending jobs reached, ' \
                  'will sleep for 30 minutes and retry'

# get rank of the processor
if system == 'bsub':
    try:
        msg_limit_reached = 'Pending job threshold reached.'
        pipe_limit_reached = 'stderr'
        rank = int(os.environ['LSB_JOBINDEX'])
        rank -= 1
    except KeyError:
        vprint(
            "Environment variable LSB_JOBINDEX not set. Setting rank to 1. "
            "Are you in a bsub system?", level='warning', verbose=True,
            logger=LOGGER)
        rank = 1

# Import the executable
executable = utils.import_executable(exe)

if function == 'main':
    vprint(
        'Running the function {} specified in executable'.format(main_name),
        logger=LOGGER, verbose=True)
else:
    vprint(
        'Running the function {} specified in executable'.format(function),
        logger=LOGGER, verbose=True)

if function == 'rerun_missing':
    vprint('Checking if all main jobs terminated correctly...',
           logger=LOGGER, verbose=True)
    indices_all = utils.get_indices(tasks)

    indices_missing = utils.check_indices(
        indices_all, path_finished, executable, function_args, LOGGER)

    utils.write_to_log(
        path_log, 'Found {} missing indices'.format(len(indices_missing)))

    if len(indices_missing) == 0:
        vprint('Nothing to resubmit. All jobs ended.',
               logger=LOGGER, verbose=True)
    else:
        if len(indices_missing) > 1:
            tasks = ','.join(map(str, indices_missing[:-1]))
            n_cores = len(indices_missing) - 1
            vprint(
                'Re-Submitting tasks {} to {} cores'.format(tasks, n_cores),
                logger=LOGGER, verbose=True)
            jobid = utils.submit_job(tasks=tasks, mode='jobarray',
                                     exe=args.executable, log_dir=log_dir,
                                     function_args=function_args,
                                     function='main', source_file=source_file,
                                     n_cores=n_cores, job_name=job_name,
                                     main_memory=main_memory,
                                     main_time=main_time,
                                     main_scratch=main_scratch, dependency='',
                                     system=system, main_name=main_name)

            utils.write_to_log(
                path_log, 'Job id rerun_missing extended: {}'.format(jobid))
        else:
            jobid = None

        # Change to local scratch if set; this has to be done after submission,
        # s.t. that the pwd at submission time is
        # the original directory where the submission starts
        utils.cd_local_scratch()

        # run last job locally to not waste any resources
        index = indices_missing[-1]
        vprint(
            '##################### Starting Task {}\
             #####################'.format(index),
            logger=LOGGER, verbose=True)
        for index in getattr(executable, main_name)([index], function_args):
            utils.write_index(index, path_finished)
        vprint(
            '##################### Finished Task {}\
             #####################'.format(index),
            logger=LOGGER, verbose=True)

        if len(indices_missing) == 1:
            utils.write_to_log(path_log, 'First index is done')

        # wait until all jobs are done
        if jobid is not None:
            while True:
                while True:
                    output = dict(stdout=[], stderr=[])
                    with subprocess.Popen(
                            shlex.split('bjobs {}'.format(jobid)),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            bufsize=1,
                            universal_newlines=True) as proc:

                        # check for limit for maximum number of pending jobs
                        for line in getattr(proc, pipe_limit_reached):

                            pending_limit_reached = msg_limit_reached in line
                            if pending_limit_reached:
                                break
                            else:
                                output[pipe_limit_reached].append(line)

                        # if the limit has been reached, kill process and sleep
                        if pending_limit_reached:
                            proc.kill()
                            vprint(TIMEOUT_MESSAGE,
                                   logger=LOGGER, verbose=True)
                            time.sleep(60 * 30)
                            continue

                        # read rest of the output
                        for line in proc.stdout:
                            output['stdout'].append(line)
                        for line in proc.stderr:
                            output['stderr'].append(line)

                        break

                # check if process terminated successfully
                if proc.returncode != 0:
                    raise RuntimeError('Running the command \"{}\" failed with'
                                       'exit code {}. Error: \n{}'.
                                       format('bjobs {}'.format(jobid),
                                              proc.returncode,
                                              '\n'.join(output['stderr'])))

                # check jobstate
                jobstate = output['stdout'][-1].split()[2]
                if (jobstate == 'DONE') | (jobstate == 'EXIT'):
                    break
                time.sleep(60)

        indices_missing = utils.check_indices(
            indices_all, path_finished, executable, function_args, LOGGER)

    if len(indices_missing) == 0:
        vprint('All indices finished',
               logger=LOGGER, verbose=True)
        utils.write_to_log(path_log, 'All indices finished')
    else:
        vprint('Even after rerun not all indices finished sucessfully',
               logger=LOGGER, verbose=True)
        utils.write_to_log(
            path_log, 'Even after rerun not all indices finished sucessfully')
else:
    # Change to local scratch if set
    utils.cd_local_scratch()

    # getting index list based on jobid
    indices = utils.get_indices_splitted(tasks, n_cores, rank)

    if function == 'main':

        vprint('Running on tasks: {}'.format(indices),
               logger=LOGGER, verbose=True)

        is_first = rank == 0

        for index in getattr(executable, main_name)(indices, function_args):
            utils.write_index(index, path_finished)
            vprint(
                '##################### Finished Task {}\
                 #####################'.format(index),
                logger=LOGGER, verbose=True)

            if is_first:
                utils.write_to_log(path_log, 'First index is done')
                is_first = False

    else:
        utils.write_to_log(path_log, 'Running {}'.format(function))
        vprint('Running {}, {} task(s), \
                    first: {}, last: {}'.format(function, len(indices),
                                                indices[0], indices[-1]),
               logger=LOGGER, verbose=True)
        getattr(executable, function)(indices, function_args)
        utils.write_to_log(path_log, 'Finished running {}'.format(function))
