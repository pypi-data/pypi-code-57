import traceback
import time
import datetime as dt

from math import *

def sleep(seconds):
    """
    Could do a sweet loading animation in console
    """
    time.sleep(seconds)

def error(msg = None):
    traceback.print_stack()
    print("ERROR: {}".format(msg))

    global gui
    if "gui" in globals():
        gui.processContainer.stopAll()

    exit()

def warn(msg):
    print("WARNING: {}".format(msg))

def dictFirstValue(dictionary, iterate = False):
    if not isinstance(dictionary, dict):
        error("not dict")
    if not len(dictionary):
        return None

    if iterate:
        return next(iter(dictionary.values()))
    return dictionary[list(dictionary.keys())[0]]

def strToDynamicType(var):
    if var == "true" or var == "True":
        return True
    if var == "false" or var == "False":
        return False

    try:
        return int(var)
    except:
        pass

    try:
        return float(var)
    except:
        pass

    return var


