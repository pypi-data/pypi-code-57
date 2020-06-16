import sys

stderr = sys.stderr
stdout = sys.stdout

def off():
    sys.stderr = None
    sys.stdout = None

def on():
    sys.stderr = stderr
    sys.stdout = stdout
