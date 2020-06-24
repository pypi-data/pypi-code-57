# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import os
import sys
import shutil
import logging
import math
import datetime
import subprocess
import shlex
import portalocker
import multiprocessing
from functools import partial
import numpy as np
import time
from ekit.logger import vprint
from ekit import logger as logger_utils

LOGGER = logger_utils.init_logger(__file__)
TIMEOUT_MESSAGE = 'Maximum number of pending jobs reached, ' \
                  'will sleep for 30 minutes and retry'


def get_logger(filepath):
    """
    Returns a logger with a specific output format

    :param filepath: path of the file using the logger
    :return: logger
    """
    logger_name = '{:>10}'.format(os.path.basename(filepath)[:10])
    logger = logging.getLogger(logger_name)
    log_formatter = logging.Formatter("%(asctime)s %(name)0.10s "
                                      "%(levelname)0.3s   %(message)s ",
                                      "%y-%m-%d %H:%M:%S")
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)
    logger.propagate = False
    logger.setLevel(logging.INFO)
    return logger


def decimal_hours_to_str(dec_hours):
    """Transforms decimal hours into the hh:mm format

    :param dec_hours: decimal hours, float or int
    :return: string in the format hh:mm
    """

    full_hours = math.floor(dec_hours)
    minutes = math.ceil((dec_hours - full_hours) * 60)

    if minutes == 60:
        full_hours += 1
        minutes = 0

    if minutes < 10:
        time_str = '{}:0{}'.format(full_hours, minutes)
    else:
        time_str = '{}:{}'.format(full_hours, minutes)

    return time_str


def make_resource_string(function, main_memory, main_time,
                         main_scratch, watchdog_memory, watchdog_time,
                         watchdog_scratch, merge_memory,
                         merge_time, merge_scratch, system):
    """
    Creates the part of the submission string which handles
    the allocation of ressources

    :param function: The name of the function defined
                     in the executable that will be submitted
    :param main_memory: Memory per core to allocate for the main job
    :param main_time: The Wall time requested for the main job
    :param main_scratch: Scratch per core to allocate for the main job
    :param watchdog_memory: Memory per core to allocate for the watchdog job
    :param watchdog_time: The Wall time requested for the watchdog job
    :param watchdog_scratch: Scratch to allocate for the watchdog job
    :param merge_memory: Memory per core to allocate for the merge job
    :param merge_time: The Wall time requested for the merge job
    :param merge_scratch: Scratch to allocate for the merge job
    :param system: The type of the queing system of the cluster
    :return: A string that is part of the submission string.
    """

    if function == 'main':
        mem = main_memory
        time = main_time
        scratch = main_scratch
    elif function == 'watchdog':
        mem = watchdog_memory
        time = watchdog_time
        scratch = watchdog_scratch
    elif function == 'merge':
        mem = merge_memory
        time = merge_time
        scratch = merge_scratch
    elif function == 'rerun_missing':
        mem = main_memory
        time = main_time
        scratch = main_scratch

    if system == 'bsub':
        resource_string = '-W {} -R rusage[mem={}] ' \
                          '-R rusage[scratch={}]'.format(
                              decimal_hours_to_str(time), mem, scratch)

    return resource_string


def get_log_filenames(log_dir, job_name, function):
    """
    Builds the filenames of the stdout and stderr log files for a
    given job name and a given function to run.

    :param log_dir: directory where the logs are stored
    :param job_name: Name of the job that will write to the log files
    :param function: Function that will be executed
    :return: filenames for stdout and stderr logs
    """
    job_name_ext = job_name + '_' + function
    stdout_log = os.path.join(log_dir, '{}.o'.format(job_name_ext))
    stderr_log = os.path.join(log_dir, '{}.e'.format(job_name_ext))
    return stdout_log, stderr_log


def get_source_cmd(source_file):
    """
    Builds the command to source a given file if the file exists,
    otherwise returns an empty string.

    :param source_file: path to the (possibly non-existing) source file,
                        can be relative and can contain "~"
    :return: command to source the file if it exists or empty string
    """

    source_file_abs = os.path.abspath(os.path.expanduser(source_file))

    if os.path.isfile(source_file_abs):
        source_cmd = 'source {}; '.format(source_file_abs)
    else:
        vprint('Source file {} not found, skipping'.format(source_file),
               logger=LOGGER, verbose=True)
        source_cmd = ''

    return source_cmd


def get_dependency_string(function, jobids, ext_dependencies, system):
    """
    Constructs the dependency string which handles which other jobs
    this job is dependent on.

    :param function: The type o function to submit
    :param jobids: Dictionary of the jobids for each job already submitted
    :param ext_dependencies: If external dependencies are given they get
                             added to the dependency string
                             (this happens if epipe is used)
    :param system: The type of the queing system of the cluster
    :return: A sting which is used as a substring for the submission string
             and it handles the dependencies of the job
    """
    if system == 'bsub':
        dep_string = '-w "'
        # no dependencies for main
        if function == 'main':
            if ext_dependencies != '':
                dep_string = '"-w' + ext_dependencies + '"'
            else:
                dep_string = ''
            return dep_string
        # watchdog starts along with main
        elif function == 'watchdog':
            if 'main' in jobids.keys():
                dep_string += '{}({})'.format('started', jobids['main'])
            else:
                vprint("Function {} has not been submitted -> Skipping "
                       "in dependencies for {}".format('main', function),
                       logger=LOGGER, verbose=True)
        # rerun missing starts after main
        elif function == 'rerun_missing':
            if 'main' in jobids.keys():
                dep_string += '{}({})'.format('ended', jobids['main'])
            else:
                vprint("Function {} has not been submitted -> Skipping "
                       "in dependencies for {}".format('main', function),
                       logger=LOGGER, verbose=True)
        # merge starts after all the others
        elif function == 'merge':
            if 'main' in jobids.keys():
                dep_string += '{}({}) && '.format('ended', jobids['main'])
            else:
                vprint("Function {} has not been submitted -> Skipping "
                       "in dependencies for {}".format('main', function),
                       logger=LOGGER, verbose=True)
            if 'watchdog' in jobids.keys():
                dep_string += '{}({}) && '.format('ended', jobids['watchdog'])
            else:
                vprint("Function {} has not been submitted -> Skipping "
                       "in dependencies for {}".format('watchdog',
                                                       function),
                       logger=LOGGER, verbose=True)
            if 'rerun_missing' in jobids.keys():
                dep_string += '{}({}) && '.format('ended',
                                                  jobids['rerun_missing'])
            else:
                vprint("Function {} has not been submitted -> Skipping "
                       "in dependencies for {}".format('rerun_missing',
                                                       function),
                       logger=LOGGER, verbose=True)
            if len(dep_string) > 4:
                dep_string = dep_string[:-4]
        else:
            raise ValueError("Dependencies for function {} "
                             "not defined".format(function))
        if ext_dependencies != '':
            dep_string = dep_string + " && " + ext_dependencies
        dep_string += '"'
    return dep_string


def make_cmd_string(function, source_file, n_cores, tasks, mode, job_name,
                    function_args, exe, main_memory, main_time,
                    main_scratch, watchdog_time, watchdog_memory,
                    watchdog_scratch, merge_memory, merge_time,
                    merge_scratch, log_dir, dependency,
                    system, main_name='main'):
    """
    Creates the submission string which gets submitted to the queing system

    :param function: The name of the function defined in the
                     executable that will be submitted
    :param source_file: A file which gets executed
                        before running the actual function(s)
    :param n_cores: The number of cores that will be requested for the job
    :param tasks: The task string, which will get parsed into the job indices
    :param mode: The mode in which the job will be
                 ran (MPI-job or as a jobarray)
    :param job_name: The name of the job
    :param function_args: The remaining arguments that
                          will be forwarded to the executable
    :param exe: The path of the executable
    :param main_memory: Memory per core to allocate for the main job
    :param main_time: The Wall time requested for the main job
    :param main_scratch: Scratch per core to allocate for the main job
    :param watchdog_memory: Memory per core to allocate for the watchdog job
    :param watchdog_time: The Wall time requested for the watchdog job
    :param watchdog_scratch: Scratch to allocate for the watchdog job
    :param merge_memory: Memory per core to allocate for the merge job
    :param merge_time: The Wall time requested for the merge job
    :param log_dir: log_dir: The path to the log directory
    :param merge_scratch: Scratch to allocate for the merge job
    :param dependency: The dependency string
    :param system: The type of the queing system of the cluster
    :param main_name: name of the main function
    :return: The submission string that wil get submitted to the cluster
    """

    # allocate computing resources
    resource_string = make_resource_string(function, main_memory, main_time,
                                           main_scratch, watchdog_memory,
                                           watchdog_time, watchdog_scratch,
                                           merge_memory, merge_time,
                                           merge_scratch, system)

    # get the job name for the submission system and the log files
    job_name_ext = job_name + '_' + function
    stdout_log, stderr_log = get_log_filenames(log_dir, job_name, function)

    # construct the string of arguments passed to the executable
    args_string = ''
    for arg in function_args:
        args_string += arg + ' '

    # make submission string
    source_cmd = get_source_cmd(source_file)

    if system == 'bsub':
        if (mode == 'mpi') & (function == 'main'):
            cmd_string = 'bsub -o {} -e {} -J {} -n {} {} {} \"{} mpirun ' \
                'python -m esub.submit_mpi --log_dir={} ' \
                         '--job_name={} --executable={} --tasks=\'{}\' ' \
                         '--main_name={} {}\"'. \
                format(stdout_log, stderr_log, job_name_ext, n_cores,
                       resource_string, dependency, source_cmd, log_dir,
                       job_name, exe, tasks, main_name, args_string)
        else:
            cmd_string = 'bsub -o {} -e {} -J {}[1-{}] {} {} \"{} python ' \
                         '-m esub.submit_jobarray --job_name={} ' \
                         '--source_file={} --main_memory={} --main_time={} ' \
                         '--main_scratch={} --function={} ' \
                         '--executable={} --tasks=\'{}\' --n_cores={} ' \
                         '--log_dir={} --system={} --main_name={} {}\"'. \
                format(stdout_log, stderr_log, job_name_ext, n_cores,
                       resource_string, dependency, source_cmd, job_name,
                       source_file, main_memory, main_time, main_scratch,
                       function, exe, tasks, n_cores, log_dir,
                       system, main_name, args_string)

    return cmd_string


def submit_job(tasks, mode, exe, log_dir, function_args, function='main',
               source_file='', n_cores=1, job_name='job', main_memory=100,
               main_time=1, main_scratch=1000, watchdog_memory=100,
               watchdog_time=1, watchdog_scratch=1000, merge_memory=100,
               merge_time=1, merge_scratch=1000, dependency='', system='bsub',
               main_name='main', test=False):
    """
    Based on arguments gets the submission string and submits it to the cluster

    :param tasks: The task string, which will get parsed into the job indices
    :param mode: The mode in which the job will be ran
                 (MPI-job or as a jobarray)
    :param exe: The path of the executable
    :param log_dir: The path to the log directory
    :param function_args: The remaining arguments that will
                          be forwarded to the executable
    :param function: The name of the function defined in the
                     executable that will be submitted
    :param source_file: A file which gets executed before
                        running the actual function(s)
    :param n_cores: The number of cores that will be requested for the job
    :param job_name: The name of the job
    :param main_memory: Memory per core to allocate for the main job
    :param main_time: The Wall time requested for the main job
    :param main_scratch: Scratch per core to allocate for the main job
    :param watchdog_memory: Memory per core to allocate for the watchdog job
    :param watchdog_time: The Wall time requested for the watchdog job
    :param watchdog_scratch: Scratch to allocate for the watchdog job
    :param merge_memory: Memory per core to allocate for the merge job
    :param merge_time: The Wall time requested for the merge job
    :param merge_scratch: Scratch to allocate for the merge job
    :param dependency: The jobids of the jobs on which this job depends on
    :param system: The type of the queing system of the cluster
    :param main_name: name of the main function
    :param test: If True no submission but just printing submission string to
                 log
    :return: The jobid of the submitted job
    """

    # get submission string
    cmd_string = make_cmd_string(function, source_file, n_cores, tasks, mode,
                                 job_name, function_args, exe,
                                 main_memory, main_time, main_scratch,
                                 watchdog_time, watchdog_memory,
                                 watchdog_scratch,
                                 merge_memory, merge_time, merge_scratch,
                                 log_dir, dependency, system, main_name)

    vprint(
        "####################### Submitting command to queing system "
        "#######################",
        logger=LOGGER, verbose=True)
    vprint(cmd_string,
           logger=LOGGER, verbose=True)

    if test:
        path_log = get_path_log(log_dir, job_name)
        write_to_log(path_log, cmd_string)
        return

    # message the system sends if the
    # maximum number of pendings jobs is reached
    if system == 'bsub':
        msg_limit_reached = 'Pending job threshold reached.'
        pipe_limit_reached = 'stderr'

    # submit
    while True:

        output = dict(stdout=[], stderr=[])

        with subprocess.Popen(shlex.split(cmd_string),
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              bufsize=1,
                              universal_newlines=True) as proc:

            # check for limit concerning maximum number of pending jobs
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
                           format(cmd_string, proc.returncode,
                                  '\n'.join(output['stderr'])))

    # get id of submitted job (bsub-only up to now)
    jobid = output['stdout'][-1].split('<')[1]
    jobid = jobid.split('>')[0]
    jobid = int(jobid)

    vprint("Submitted job and got jobid: {}".format(jobid),
           logger=LOGGER, verbose=True)

    return jobid


def robust_remove(path):
    """
    Remove a file or directory if existing

    :param path: path to possible non-existing file or directory
    """
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)
    # recreate
    open(path, 'a').close()


def get_path_log(log_dir, job_name):
    """
    Construct the path of the esub log file

    :param log_dir: directory where log files are stored
    :param job_name: name of the job that will be logged
    :return: path of the log file
    """
    path_log = os.path.join(log_dir, job_name + '.log')
    return path_log


def get_path_finished_indices(log_dir, job_name):
    """
    Construct the path of the file containing the finished indices

    :param log_dir: directory where log files are stored
    :param job_name: name of the job for which the indices will be store
    :return: path of the file for the finished indices
    """
    path_finished = os.path.join(log_dir, job_name + '_done.dat')
    return path_finished


def import_executable(exe, verbose=True):
    """
    Imports the functions defined in the executable file.

    :param exe: path of the executable
    :param verbose: whether to give out a logging statement about the import
    :return: executable imported as python module
    """
    sys.path.insert(0, os.path.dirname(exe))
    to_import = os.path.basename(exe).replace('.py', '')
    executable = __import__(to_import)
    if verbose:
        vprint('Imported {}'.format(exe),
               logger=LOGGER, verbose=True)
    return executable


def save_write(path, str_to_write, mode='a'):
    """
    Write a string to a file, with the file being locked in the meantime.

    :param path: path of file
    :param str_to_write: string to be written
    :param mode: mode in which file is opened
    """
    with portalocker.Lock(path, mode=mode, timeout=math.inf) as f:
        # write
        f.write(str_to_write)
        # flush and sync to filesystem
        f.flush()
        os.fsync(f.fileno())


def write_index(index, finished_file):
    """
    Writes the index number on a new line of the
    file containing the finished indices

    :param index: A job index
    :param finished_file: The file to which the
                          jobs will write that they are done
    """
    save_write(finished_file, '{}\n'.format(index))


def check_indices(indices, finished_file, exe, function_args, LOGGER):
    """
    Checks which of the indices are missing in
    the file containing the finished indices

    :param indices: Job indices that should be checked
    :param finished_file: The file from which the jobs will be read
    :param exe: Path to executable
    :return: Returns the indices that are missing
    """
    # wait for the indices file to be written
    if os.path.exists(finished_file):
        # first get the indices missing in the log file (crashed jobs)
        done = []
        with open(finished_file, 'r') as f:
            for line in f:
                # Ignore empty lines
                if line != '\n':
                    done.append(int(line.replace('\n', '')))
        failed = list(set(indices) - set(done))
    else:
        vprint("Did not find File {} -> None of the main functions "
               "recorded its indices. "
               "Not rerunning any jobs".format(finished_file),
               logger=LOGGER, verbose=True)
        failed = []

    # if provided use check_missing function
    # (finished jobs but created corrupted output)
    if hasattr(exe, 'check_missing'):
        vprint("Found check_missing function in executable.",
               logger=LOGGER, verbose=True)
        corrupted = getattr(exe, 'check_missing')(indices, function_args)
    else:
        corrupted = []

    missing = failed + corrupted
    missing = np.unique(np.asarray(missing))
    return missing


def write_to_log(path, line, mode='a'):
    """
    Write a line to a esub log file

    :param path: path of the log file
    :param line: line (string) to write
    :param mode: mode in which the log file will be opened
    """
    extended_line = "{}    {}\n".format(datetime.datetime.now(), line)
    save_write(path, extended_line, mode=mode)


def cd_local_scratch(verbose=True):
    """
    Change to current working directory to the local scratch if set.

    :param verbose: whether to give out a logging
                    statement about the new working directory.
    """
    if 'ESUB_LOCAL_SCRATCH' in os.environ:

        if os.path.isdir(os.environ['ESUB_LOCAL_SCRATCH']):
            submit_dir = os.getcwd()
            os.chdir(os.environ['ESUB_LOCAL_SCRATCH'])
            os.environ['SUBMIT_DIR'] = submit_dir

            if verbose:
                vprint('Changed current working directory to {} and '
                       'set $SUBMIT_DIR to {}'.
                       format(os.getcwd(), os.environ['SUBMIT_DIR']),
                       logger=LOGGER, verbose=True)
        else:
            LOGGER.error('$ESUB_LOCAL_SCRATCH is set to non-existing '
                         'directory {}, skipping...'.
                         format(os.environ['ESUB_LOCAL_SCRATCH']))


def run_local_mpi_job(exe, n_cores, function_args, logger, main_name='main'):
    """
    This function runs an MPI job locally

    :param exe: Path to executable
    :param n_cores: Number of cores
    :param function_args: A list of arguments to be passed to the executable
    :param index: Index number to run
    :param logger: logger instance for logging
    :param main_name:
    """
    # construct the string of arguments passed to the executable
    args_string = ''
    for arg in function_args:
        args_string += arg + ' '

    # make command string
    cmd_string = 'mpirun -np {} python -m esub.submit_mpi' \
                 ' --executable={} --tasks=\'0\' --main_name={} {}'.\
                 format(n_cores, exe, main_name, args_string)
    print(cmd_string)
    sys.exit()
    for line in execute_local_mpi_job(cmd_string):
        line = line.strip()
        if len(line) > 0:
            logger.info(line)


def get_indices(tasks):
    """
    Parses the jobids from the tasks string.

    :param tasks: The task string, which will get parsed into the job indices
    :return: A list of the jobids that should be executed
    """
    # parsing a list of indices from the tasks argument
    if '>' in tasks:
        tasks = tasks.split('>')
        start = tasks[0].replace(' ', '')
        stop = tasks[1].replace(' ', '')
        indices = list(range(int(start), int(stop)))
    elif ',' in tasks:
        indices = tasks.split(',')
        indices = list(map(int, indices))
    elif os.path.exists(tasks):
        with open(tasks, 'r') as f:
            content = f.readline()
        indices = get_indices(content)
    else:
        try:
            indices = [int(tasks)]
        except ValueError:
            raise ValueError("Tasks argument is not in the correct format!")
    return indices


def get_indices_splitted(tasks, n_cores, rank):
    """
    Parses the jobids from the tasks string.
    Performs load-balance splitting of the jobs and returns the indices
    corresponding to rank. This is only used for job array submission.

    :param tasks: The task string, which will get parsed into the job indices
    :param n_cores: The number of cores that will be requested for the job
    :param rank: The rank of the core
    :return: A list of the jobids that should
             be executed by the core with number rank
    """

    # Parse
    indices = get_indices(tasks)

    # Load-balanced splitter
    steps = len(indices)
    size = n_cores
    chunky = int(steps / size)
    rest = steps - chunky * size
    mini = chunky * rank
    maxi = chunky * (rank + 1)
    if rank >= (size - 1) - rest:
        maxi += 2 + rank - size + rest
        mini += rank - size + 1 + rest
    mini = int(mini)
    maxi = int(maxi)

    return indices[mini:maxi]


def function_wrapper(indices, args, func):
    """
    Wrapper that converts a generator to a function.

    :param generator: A generator
    """
    inds = []
    for ii in func(indices, args):
        inds.append(ii)
    return inds


def run_local_mpi_tasks(exe, n_cores, function_args, tasks, function, logger):
    """
    Executes an MPI job locally, running each splitted index list on one core.

    :param exe: The executable from where the main function is imported.
    :param n_cores: The number of cores to allocate.
    :param function_args: The arguments that
                          will get passed to the main function.
    :param tasks: The indices to run on.
    :param function: The function name to run
    :param logger: The logger instance
    """
    # get executable
    func = getattr(exe, function)

    # Fix function arguments for all walkers
    run_func = partial(function_wrapper, args=function_args, func=func)

    # get splitted indices
    nums = []
    for rank in range(n_cores):
        nums.append(get_indices_splitted(tasks, n_cores, rank))

    # Setup mutltiprocessing pool
    pool = multiprocessing.Pool(processes=n_cores)
    if int(multiprocessing.cpu_count()) < n_cores:
        raise Exception(
            "Number of CPUs available is smaller \
             than requested number of CPUs")

    # run and retrive the finished indices
    out = pool.map(run_func, nums)
    out = [item for sublist in out for item in sublist]
    return out


def execute_local_mpi_job(cmd_string):
    """
    Execution of local MPI job

    :param cmd_string: The command string to run
    """
    popen = subprocess.Popen(shlex.split(cmd_string),
                             stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd_string)
