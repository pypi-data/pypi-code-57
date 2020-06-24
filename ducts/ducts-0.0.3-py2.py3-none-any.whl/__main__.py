#!/usr/bin/env python3
# coding: utf-8

import os
import sys
from importlib import import_module
import psutil
from pathlib import Path
import functools
import argparse

from daemon.pidfile import TimeoutPIDLockFile, DaemonContext

from ifconf import configure_module, config_callback, configure_main

def start(pidfile, run):
    if pidfile.is_locked():
        raise Exception('Process is already started.')
    current_dir = os.getcwd()
    with DaemonContext(
            pidfile=pidfile
            , stdout = sys.stdout
            , stderr = sys.stderr):
        os.chdir(current_dir)
        run()
    
def stop(pidfile, run):
    if not pidfile.is_locked():
        return
    pid = pidfile.read_pid()
    print('Terminating PID={}...'.format(pid))
    p = psutil.Process(pid)
    p.terminate()  #or p.kill()

def main():
    module_names = [py.stem for py in Path(__file__).parent.joinpath('main').glob('*.py')]
    parser = argparse.ArgumentParser()
    parser.add_argument('module', help='module_name to run command. '.join(module_names))
    parser.add_argument('command', help='[start|stop]')
    parser.add_argument('--service', dest='service', default='run', help='service to run')
    config = configure_main(argparser = parser)
    run = getattr(import_module('{}.{}.{}'.format('ducts', 'main', config.args.module)), config.args.service)
    command = getattr(import_module(main.__module__), config.args.command)
    
    import ducts.common as c
    pidfile = TimeoutPIDLockFile(c.get_pidfile(config.args.module, config.args.service))

    command(pidfile, run)
    
if __name__ == '__main__':
    main()
    
