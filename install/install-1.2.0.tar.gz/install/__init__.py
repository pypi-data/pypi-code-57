#!/usr/bin/python
import subprocess
import sys
import shlex
import os
import tempfile
import urllib.request

def _get_pip():
    fd, path = tempfile.mkstemp('_get-pip.py')
    urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", path)
    subprocess.check_call([sys.executable, path])

def _check_pip():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip'], stdout=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError as exc:
        return False

def install(pkg, use_pep517=None, requirements=None, options=None):
    """Install packages dynamically in your code

    Args:
        pkg: Name of the package as a string, you can also use version specifiers like requests==1.2.3
        use_pep517: Optionally set to True or False to force --use-pep517/--no-use-pep517
        options: Arbitary list of options to pass to pip for installation
    """
    if not _check_pip(): _get_pip()

    cmd = [sys.executable, '-m', 'pip', 'install']
    
    if options and isinstance(options, list):
        cmd.extend(options)

    if use_pep517 is True:
        cmd.append('--use-pep517')
    elif use_pep517 is False:
        cmd.append('--no-use-pep517')

    pkg = shlex.quote(pkg)
    cmd.append(pkg)

    subprocess.check_call(cmd)

