# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Joerg Herbel

import os
import shutil
import shlex
import subprocess
import pytest


def run_exec_example(test_dir, mode='run', tasks_string=None,
                     extra_esub_args=''):

    # path to example file
    path_example = 'example/exec_example.py'

    # build command
    cmd = 'esub {} --mode={} --output_directory={} {}'.format(path_example,
                                                              mode, test_dir,
                                                              extra_esub_args)
    if tasks_string is not None:
        cmd += ' --tasks={}'.format(tasks_string)

    # main function
    subprocess.call(shlex.split(cmd))
    subprocess.call(shlex.split(cmd + ' --function=main'))

    # rerun_missing
    subprocess.call(shlex.split(cmd + ' --function=rerun_missing'))

    # watchdog
    subprocess.call(shlex.split(cmd + ' --function=watchdog'))

    # merge
    subprocess.call(shlex.split(cmd + ' --function=merge'))

    # all functions
    subprocess.call(shlex.split(cmd + ' --function=all'))


def test_esub_run():

    # create directory for test output
    path_testdir = 'esub_test_dir'
    if not os.path.isdir(path_testdir):
        os.mkdir(path_testdir)

    # test with no tasks provided
    run_exec_example(path_testdir)

    # test with single task
    run_exec_example(path_testdir, tasks_string='99')

    # test with list of tasks
    run_exec_example(path_testdir, tasks_string='10,2,4')

    # test with range
    run_exec_example(path_testdir, tasks_string='"1 > 3"')

    # test run-tasks
    run_exec_example(path_testdir, mode='run-tasks',
                     tasks_string='"0 > 4"', extra_esub_args='--n_cores=2')

    # remove directory for test output
    shutil.rmtree(path_testdir)

    # test another example,
    # this time with renamed main function and missing merge function
    # works because main is renamed
    subprocess.call(shlex.split(
        'esub example/executable_test.py --function=main'))
    # works because main is renamed
    subprocess.call(shlex.split(
        'esub example/executable_test.py --function=all'))

    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_call(shlex.split(
            'esub example/executable_test.py --function=main \
            --main_name=main_renamed'))

    # check that log directory was created and remove it then
    log_dir = 'esub_logs'
    assert os.path.isdir(log_dir)
    shutil.rmtree(log_dir)


def test_esub_jobarray():

    # create directory for test output
    path_testdir = 'esub_test_dir_submit'
    if not os.path.isdir(path_testdir):
        os.mkdir(path_testdir)

    extra = '--test --main_memory=50000 --main_time_per_index=100 '\
            '--main_scratch=100000 --watchdog_memory=2400 --watchdog_time=50 '\
            '--watchdog_scratch=90000 --merge_time=30 --merge_memory=98000 '\
            '--merge_scratch=100000 --n_cores=100'
    # test with no tasks provided
    run_exec_example(path_testdir, mode='jobarray', extra_esub_args=extra,
                     tasks_string='"1 > 3"')

    # check if the submission strings are correct
    check_cmd_strings('check_strings.txt')

    # remove directory for test output
    shutil.rmtree(path_testdir)

    # check that log directory was created and remove it then
    log_dir = 'esub_logs'
    assert os.path.isdir(log_dir)
    shutil.rmtree(log_dir)


def test_esub_mpi():

    # create directory for test output
    path_testdir = 'esub_test_dir_mpi'
    if not os.path.isdir(path_testdir):
        os.mkdir(path_testdir)

    extra = '--test --main_memory=50000 --main_time=50 '\
            '--main_scratch=100000 --watchdog_memory=2400 --watchdog_time=50 '\
            '--watchdog_scratch=90000 --merge_time=30 --merge_memory=98000 '\
            '--merge_scratch=100000 --n_cores=100'
    # test with no tasks provided
    run_exec_example(path_testdir, mode='mpi', extra_esub_args=extra,
                     tasks_string='"1 > 3"')

    # check if the submission strings are correct
    check_cmd_strings('check_strings_mpi.txt')

    # remove directory for test output
    shutil.rmtree(path_testdir)

    # check that log directory was created and remove it then
    log_dir = 'esub_logs'
    assert os.path.isdir(log_dir)
    shutil.rmtree(log_dir)


def check_cmd_strings(file):
    cwd = os.getcwd()

    sub_strings = []
    with open('esub_logs/job.log', 'r') as f:
        content = f.readlines()
    for line in content:
        if 'bsub' in line:
            sub_strings.append('bsub' + line.split('bsub')[1])
    with open('tests/{}'.format(file), 'r') as f:
        check_strings_ = f.read().splitlines()
    check_strings = []
    for s in check_strings_:
        if len(s) > 0:
            check_strings.append(s.format(cwd, cwd, cwd, cwd))
    for ii, cmd_string in enumerate(sub_strings):
        if (ii < 2) | (ii == 5):
            continue
        assert cmd_string == check_strings[ii]
