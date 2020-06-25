import os
import sys
import psutil
import shutil
import socket
import getpass

from os.path import *

WINDOWS = os.name == 'nt'
OSX = os.name == 'posix'

def runcommand(command = ''):
    if WINDOWS:
        return not bool(os.system(command))
    elif OSX:
        return bool(os.system(command))

def startfile(filename = '', option = None):
    if WINDOWS and option:
        return os.startfile(filename, option)
    elif WINDOWS:
        return os.startfile(filename)
    elif OSX and option:
        return runcommand(f'open {filename} {option}')
    elif OSX:
        return runcommand(f'open {filename}')

def getcwd():
    return os.getcwd()

def setcwd(nwd):
    return os.chdir(nwd)

def copyfile(src, dst):
    return os.link(src, dst)

def copydir(src, dist):
    return shutil.copytree(src, dst)

def killpid(pid, signal = 0):
    try:
        out = sys.stdout
        err = sys.stderr
        sys.stdout = None
        sys.stderr = None
        os.kill(pid, signal)
        sys.stdout = out
        sys.stderr = err
        return True
    except:
        return False

def getpid():
    return os.getpid()

def getpids():
    return psutil.pids()

def getpidobjs():
    return list(psutil.process_iter())

def getip():
    return socket.gethostbyname(socket.gethostname())

def getuser():
    return getpass.getuser()

def cleanpids():
    nodelete = [getpid()]
    delete = []
    for pidobj in getpidobjs():
        if pidobj.name() in ('python.exe', 'pythonw.exe'):
            nodelete.append(pidobj.pid)
            
    for pidobj in getpidobjs():
        if pidobj.pid in nodelete:
            9
