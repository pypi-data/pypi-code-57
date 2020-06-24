#! /usr/bin/env python

# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

# System imports
from __future__ import (print_function, division, absolute_import,
                        unicode_literals)

# package import
import argparse
import math
import os
import sys
import collections
from esub import utils
from ekit.logger import vprint
from ekit import logger as logger_utils


LOGGER = logger_utils.init_logger(__file__)
TIMEOUT_MESSAGE = 'Maximum number of pending jobs reached, ' \
                  'will sleep for 30 minutes and retry'


def starter_message():
    print()
    print(' ______   _______   _    _   _______ ')
    print('|  ____| |  _____| | |  | | |  _    |')
    print('| |___   | |_____  | |  | | | |_|  _|')
    print('|  ___|  |_____  | | |  | | |  _  |_ ')
    print('| |____   _____| | | |__| | | |_|   |')
    print('|______| |_______| \\______/ |_______|')
    print()


def main(args=None):
    """
    Main function of esub.

    :param args: Command line arguments are parsed
    """

    if args is None:
        args = sys.argv[1:]

    # Make log directory if non existing
    log_dir = os.path.join(os.getcwd(), 'esub_logs')
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)
        vprint('Created directory {}'.format(log_dir),
               logger=LOGGER, verbose=True)

    # initializing parser
    description = "This is esub an user friendly and flexible tool to " \
                  "submit jobs to a cluster or run them locally"
    parser = argparse.ArgumentParser(description=description, add_help=True)

    resources = dict(main_memory=1000,
                     main_time=4,
                     main_time_per_index=None,
                     main_scratch=2000,
                     watchdog_memory=1000,
                     watchdog_time=4,
                     watchdog_scratch=2000,
                     merge_memory=1000,
                     merge_time=4,
                     merge_scratch=2000)

    # parse all the submitter arguments
    parser.add_argument(
        'exec', type=str, help='path to the executable (python file '
                               'containing functions main, watchdog, merge)')
    parser.add_argument('--mode', type=str, default='run',
                        choices=('run', 'jobarray', 'mpi',
                                 'run-mpi', 'run-tasks'),
                        help='The mode in which to operate. '
                        'Choices: run, jobarray, mpi, run-mpi, '
                        'run-tasks')
    parser.add_argument('--job_name', type=str, default='job',
                        help='Individual name for this job. CAUTION: '
                             'Multiple jobs with same name'
                             'can confuse system!')
    parser.add_argument('--source_file', type=str, default='source_esub.sh',
                        help='Optionally provide a source file which '
                        'gets executed first (loading modules, '
                        'declaring environemental variables and so on')
    parser.add_argument('--main_memory', type=float,
                        default=resources['main_memory'],
                        help='Memory allocated per core for main job in MB')
    parser.add_argument('--main_time', type=float,
                        default=resources['main_time'],
                        help='Job run time limit in hours for main job')
    parser.add_argument('--main_time_per_index', type=float,
                        default=resources['main_time_per_index'],
                        help='Job run time limit in hours for main '
                             'job per index, overwrites main_time if set')
    parser.add_argument('--main_scratch', type=float,
                        default=resources['main_scratch'],
                        help='Local scratch for allocated for main job')
    parser.add_argument('--watchdog_memory', type=float,
                        default=resources['watchdog_memory'],
                        help='Memory allocated per core '
                             'for watchdog job in MB')
    parser.add_argument('--watchdog_time', type=float,
                        default=resources['watchdog_time'],
                        help='Job run time limit in hours for watchdog job')
    parser.add_argument('--watchdog_scratch', type=float,
                        default=resources['watchdog_scratch'],
                        help='Local scratch for allocated for watchdog job')
    parser.add_argument('--merge_memory', type=float,
                        default=resources['merge_memory'],
                        help='Memory allocated per core for merge job in MB')
    parser.add_argument('--merge_time', type=float,
                        default=resources['merge_time'],
                        help='Job run time limit in hours for merge job')
    parser.add_argument('--merge_scratch', type=float,
                        default=resources['merge_scratch'],
                        help='Local scratch for allocated for merge job')
    parser.add_argument('--function', type=str, default=['main'], nargs='+',
                        choices=('main', 'watchdog', 'merge', 'rerun_missing',
                                 'all'),
                        help='The functions that should be executed. '
                        'Choices: main, watchdog, merge, rerun_missing, all')
    parser.add_argument('--main_name', type=str, default='main',
                        help='Name of the main function in the executable')
    parser.add_argument('--tasks', type=str, default='0',
                        help='Task string from which the indices are parsed. '
                             'Either single index, list of indices or range '
                             'looking like int1 > int2')
    parser.add_argument('--n_cores', type=int, default=1,
                        help='The number of cores to request')
    parser.add_argument('--dependency', type=str, default='',
                        help='A dependency string that gets added to the '
                             'dependencies (meant for pipelining)')
    parser.add_argument('--system', type=str, default='bsub',
                        choices=('bsub',),
                        help='Type of the queing system '
                             '(so far only know bsub)')
    parser.add_argument('--test', action='store_true',
                        default=False, help='Test mode')

    args, function_args = parser.parse_known_args(args)

    mode = args.mode
    main_name = args.main_name
    job_name = args.job_name
    source_file = args.source_file
    tasks = args.tasks
    exe = args.exec
    n_cores = args.n_cores
    function = args.function
    system = args.system
    ext_dependencies = args.dependency

    if len(function) == 1 and function[0] == 'all':
        function = 'all'

    # Make sure that executable exits
    if os.path.isfile(exe):
        if not os.path.isabs(exe):
            exe = os.path.join(os.getcwd(), exe)
    else:
        raise FileNotFoundError(
            'Did not find {}. Please specify a valid path for '
            'executable'.format(exe))

    starter_message()

    # Set path to log file and to file storing finished main job ids
    path_log = utils.get_path_log(log_dir, job_name)
    path_finished = utils.get_path_finished_indices(log_dir, job_name)
    vprint("Using log file {}".format(path_log),
           logger=LOGGER, verbose=True)
    vprint("Storing finished indices in file {}".format(path_finished),
           logger=LOGGER, verbose=True)
    vprint("Running in mode {}".format(mode),
           logger=LOGGER, verbose=True)

    # importing the functions from the executable
    executable = utils.import_executable(exe)

    # check if required function exists. Otherwise skip it
    if function == 'all':
        function = ['main', 'rerun_missing', 'watchdog', 'merge']
    for func in function:
        if func == 'rerun_missing':
            continue
        elif func == 'main':
            if not hasattr(executable, main_name):
                vprint(
                    "Did not find main function {} in the executable. "
                    "Skipping it...".format(main_name),
                    logger=LOGGER, verbose=True)
                function.remove(func)
        else:
            if not hasattr(executable, func):
                vprint(
                    "Did not find function {} in the executable. "
                    "Skipping it...".format(func),
                    logger=LOGGER, verbose=True)
                function.remove(func)
    if len(function) == 0:
        vprint("No function to run found. Exiting...",
               logger=LOGGER, verbose=True)
        sys.exit(0)

    # run setup if implemented
    if hasattr(executable, 'setup'):
        vprint('Running setup from executable',
               logger=LOGGER, verbose=True)
        getattr(executable, 'setup')(function_args)

    # get resources from executable if implemented
    res_update = dict()
    if hasattr(executable, 'resources'):
        vprint('Getting cluster resources from executable',
               logger=LOGGER, verbose=True)
        res_update = getattr(executable, 'resources')(function_args)

    # overwrite with non-default command-line input
    for res_name, res_default_val in resources.items():
        res_cmd_line = getattr(args, res_name)
        if res_cmd_line != res_default_val:
            res_update[res_name] = res_cmd_line

    resources.update(res_update)

    if resources['main_time_per_index'] is not None:
        n_indices = len(utils.get_indices(tasks))
        resources['main_time'] = resources['main_time_per_index'] * \
            math.ceil(n_indices / n_cores)

    del resources['main_time_per_index']

    # check if log files should be overwritten
    overwrite_log = function == 'all'

    # CASE 1 : run locally
    if (mode == 'run') | (mode == 'run-mpi') | (mode == 'run-tasks'):
        # adding function and tasks arguments
        if function == 'all':
            vprint("Running all functions specified in executable",
                   logger=LOGGER, verbose=True)
        else:
            vprint("Running the function(s) {} "
                   "specified in executable".format(
                       ', '.join(function)),
                   logger=LOGGER, verbose=True)

        # getting index list
        indices = utils.get_indices(tasks)
        vprint("Running on tasks: {}".format(indices),
               logger=LOGGER, verbose=True)

        # loop over functions
        for f in function:

            indices_use = indices

            # check if function is specified
            if f == 'main' or f == 'rerun_missing':
                function_found = hasattr(executable, main_name)
            else:
                function_found = hasattr(executable, f)

            if not function_found:
                vprint(
                    "The requested function {} is missing in the executable. "
                    "Skipping...".format(f),
                    logger=LOGGER, verbose=True)
                continue

            if f == 'main':
                # resetting missing file
                vprint("Resetting file holding finished indices",
                       logger=LOGGER, verbose=True)
                utils.robust_remove(path_finished)

            if f == 'rerun_missing':
                indices_use = utils.check_indices(
                    indices, path_finished, executable, function_args, LOGGER)
                if len(indices_use) > 0:
                    vprint("Rerunning tasks: {}".format(indices_use),
                           logger=LOGGER, verbose=True)
                    f = 'main'
                else:
                    vprint('All indices are finished, nothing to re-run.',
                           logger=LOGGER, verbose=True)
                    continue

            if f == 'main':

                if mode == 'run':
                    for index in getattr(executable, main_name)(indices,
                                                                function_args):
                        utils.write_index(index, path_finished)
                        vprint(
                            "##################### Finished Task {} "
                            "#####################".format(index),
                            logger=LOGGER, verbose=True)

                elif mode == 'run-mpi':
                    utils.run_local_mpi_job(
                        exe, n_cores, function_args, LOGGER, main_name)
                    vprint(
                        "##################### Finished "
                        "#####################",
                        logger=LOGGER, verbose=True)

                elif mode == 'run-tasks':
                    dones = utils.run_local_mpi_tasks(
                        executable, n_cores, function_args, tasks, main_name,
                        LOGGER)
                    for index in dones:
                        utils.write_index(index, path_finished)
                        vprint(
                            "##################### Finished Task {} "
                            "#####################".format(index),
                            logger=LOGGER, verbose=True)

            else:
                getattr(executable, f)(indices_use, function_args)

    # CASE 2 and 3 : running jobs on cluster (MPI or jobarray)
    elif (mode == 'jobarray') | (mode == 'mpi'):
        # Add dependencies to functions
        if (function == 'all') & (mode == 'jobarray'):
            function = ['main', 'watchdog', 'rerun_missing', 'merge']
            vprint("Submitting all functions specified in executable "
                   "to queuing system. Watchdog running along "
                   "main. Trying to rerun jobs after main finished. "
                   "Merge running at the end.",
                   logger=LOGGER, verbose=True)
        elif (function == 'all') & (mode == 'mpi'):
            function = ['main', 'watchdog', 'merge']
            vprint("Submitting all functions specified in executable "
                   "to queuing system. Watchdog running along "
                   "main. Merge running at the end.",
                   logger=LOGGER, verbose=True)
        else:
            vprint("Submitting the function(s) {} specified in "
                   "executable to queuing system".
                   format(', '.join(function)),
                   logger=LOGGER, verbose=True)

        jobids = collections.OrderedDict()
        for ii, f in enumerate(function):

            if f == 'main' or f == 'rerun_missing':
                function_found = hasattr(executable, main_name)
            else:
                function_found = hasattr(executable, f)

            if not function_found:
                vprint(
                    "The requested function {} is missing in the executable. "
                    "Skipping...".format(f),
                    logger=LOGGER, verbose=True)
                continue

            if f == 'main':
                # resetting missing file
                vprint("Resetting file holding finished indices",
                       logger=LOGGER, verbose=True)
                utils.robust_remove(path_finished)
                n_cores_use = n_cores
            else:
                n_cores_use = 1

            vprint(
                "Submitting {} job to {} core(s)".format(f, n_cores_use),
                logger=LOGGER, verbose=True)

            # reset logs
            vprint('Resetting log files',
                   logger=LOGGER, verbose=True)
            stdout_log, stderr_log = utils.get_log_filenames(
                log_dir, job_name, f)
            utils.robust_remove(stdout_log)
            utils.robust_remove(stderr_log)

            # the current job depends at most on the previous one
            # (e.g., rerun_missing does not need to wait for the
            # watchdog to finish)
            dependency = utils.get_dependency_string(
                f, jobids, ext_dependencies, system)

            jobid = utils.submit_job(tasks, mode, exe, log_dir, function_args,
                                     function=f,
                                     source_file=source_file,
                                     n_cores=n_cores_use,
                                     job_name=job_name,
                                     dependency=dependency,
                                     system=system,
                                     main_name=main_name,
                                     test=args.test,
                                     **resources)
            jobids[f] = jobid
            vprint(
                "Submitted job for function {} as jobid {}".format(f, jobid),
                logger=LOGGER, verbose=True)

        vprint("Submitted jobids: {}".format(
            ' '.join([str(jobid) for jobid in jobids.values()])),
            logger=LOGGER, verbose=True)

        # write to log
        if overwrite_log:
            utils.write_to_log(
                path_log, 'esub arguments: \n{}'.format(args), mode='w')
            utils.write_to_log(
                path_log, 'function arguments: \n{}'.format(function_args))

        for fun, jobid in jobids.items():
            utils.write_to_log(path_log, 'Job id {}: {}'.format(fun, jobid))


if __name__ == '__main__':
    main()
