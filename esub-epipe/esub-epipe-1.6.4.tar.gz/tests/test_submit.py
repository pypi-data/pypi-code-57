# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import shutil
import shlex
import os
import subprocess


def test_submit_jobarray():
    # setup mock esub_logs directory with log files
    path_testdir = 'esub_logs_submit_jobarray'
    if not os.path.isdir(path_testdir):
        os.mkdir(path_testdir)

    # main job
    cmd = "python esub/submit_jobarray.py --job_name=job --main_memory=100 " \
          "--main_time=2 --main_scratch=1000 --function=main " \
          "--executable=example/exec_example.py --tasks='0 > 10' " \
          "--n_cores=10 --log_dir={} --system=bsub " \
          "--main_name=main " \
        "--source_file=example/source_file_example.sh".format(path_testdir)
    subprocess.call(shlex.split(cmd))

    # watchdog job
    cmd = "python esub/submit_jobarray.py --job_name=job --main_memory=100 " \
          "--main_time=2 --main_scratch=1000 --function=watchdog " \
          "--executable=example/exec_example.py --tasks='0 > 10' " \
          "--n_cores=10 --log_dir={} --system=bsub " \
          "--main_name=main " \
        "--source_file=example/source_file_example.sh".format(path_testdir)
    subprocess.call(shlex.split(cmd))

    # merge job
    cmd = "python esub/submit_jobarray.py --job_name=job --main_memory=100 " \
          "--main_time=2 --main_scratch=1000 --function=merge " \
          "--executable=example/exec_example.py --tasks='0 > 10' " \
          "--n_cores=10 --log_dir={} --system=bsub " \
          "--main_name=main " \
          "--source_file=example/source_file_example.sh".format(path_testdir)
    subprocess.call(shlex.split(cmd))

    # rerun missing job (will not find all output files)
    cmd = "python esub/submit_jobarray.py --job_name=job --main_memory=100 " \
        "--main_time=2 --main_scratch=1000 --function=rerun_missing " \
          "--executable=example/exec_example.py --tasks='0 > 10' " \
        "--n_cores=10 --log_dir={} --system=bsub " \
        "--main_name=main " \
        "--source_file=example/source_file_example.sh".format(path_testdir)

    out = subprocess.call(shlex.split(cmd))
    assert out == 1

    shutil.rmtree(path_testdir)
    subprocess.call(['rm randoms_1.npy'], shell=1)
    subprocess.call(['rm all_randoms.npy'], shell=1)


def test_submit_mpi():

    # setup mock esub_logs directory with log files
    path_testdir = 'esub_logs_submit_mpi'
    if not os.path.isdir(path_testdir):
        os.mkdir(path_testdir)

    # main job
    cmd = "python esub/submit_mpi.py --log_dir={} " \
          "--job_name=job " \
          "--executable=example/exec_example.py --tasks=0 " \
          "--main_name=main --test".format(path_testdir)

    subprocess.call(shlex.split(cmd))
    shutil.rmtree(path_testdir)
    subprocess.call(['rm randoms_0.npy'], shell=1)
