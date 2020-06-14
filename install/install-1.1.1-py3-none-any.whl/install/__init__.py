#!/usr/bin/python
import subprocess
import sys
import shlex

def install(pkg, use_pep517=None):
    cmd = [sys.executable, '-m', 'pip', 'install']
    
    if use_pep517 is True:
        cmd.append('--use-pep517')
    elif use_pep517 is False:
        cmd.append('--no-use-pep517')
    
    pkg = shlex.quote(pkg)
    cmd.append(pkg)

    subprocess.check_call(cmd)

