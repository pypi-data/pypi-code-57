#!/usr/bin/python
import subprocess
import sys

def install(pkg):
	subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])
