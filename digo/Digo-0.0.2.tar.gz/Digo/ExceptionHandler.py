import sys, traceback
import atexit
from Digo import DigoCore

isCrash = False

def check_crash(exc_type, exc_value, exc_traceback):
	global isCrash
	isCrash = True
	traceback.print_exception(exc_type, exc_value, exc_traceback)

def exit_process():
	if isCrash is True:
		DigoCore.Core.instance()
		print("Digo Exit(1)")
	else:
		print("Digo Exit(0)")


atexit.register(exit_process)
sys.excepthook = check_crash
