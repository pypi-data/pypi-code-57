import logging as log
import os
from pathlib import Path
from runpy import run_path
from shutil import copyfile

##########################################################
#################### User settings #######################
##########################################################
try:
    home = Path.home()  # In Bash for Windows this does not work
    config_path = home / ".nqontrol.py"

    if os.path.isfile(config_path):
        user_config = run_path(str(config_path))
        log.info("Successfully imported user configuration.")
    else:
        # Copy sample file to user path
        nqontrol_path = os.path.dirname(os.path.abspath(__file__))
        src = "{}/settings_local.sample.py".format(nqontrol_path)
        copyfile(src, config_path)
        log.info("Created a user configuration template at {}".format(config_path))
        user_config = {}
except (IOError, OSError, AttributeError) as e:
    log.warning(e)
    user_config = {}

##########################################################
#################### Default settings ####################
##########################################################
# Local configuration
HOST = user_config.get("HOST", "127.0.0.1")
PORT = user_config.get("PORT", 8000)
DEVICE_NUM = user_config.get("DEVICE_NUM", 1)
SETTINGS_FILE = user_config.get("SETTINGS_FILE", None)
CREATE_SETTINGS_BACKUP = user_config.get("CREATE_SETTINGS_BACKUP", False)
BACKUP_SUBSTRING = user_config.get("BACKUP_SUBSTRING", "%Y-%m-%d_%H-%M-%S")

LOG_LEVEL = user_config.get("LOG_LEVEL", "WARNING")
LOG_FORMAT = user_config.get("LOG_FORMAT", "%(levelname)s: %(module)s: %(message)s")
DEBUG = user_config.get("DEBUG", False)

NUMBER_OF_SERVOS = user_config.get("NUMBER_OF_SERVOS", 8)
NUMBER_OF_MONITORS = user_config.get("NUMBER_OF_MONITORS", 8)

# Temperature feedback
DEFAULT_TEMP_HOST = user_config.get("DEFAULT_TEMP_HOST", "127.0.0.1")
DEFAULT_TEMP_PORT = user_config.get("DEFAULT_TEMP_PORT", 5917)

# Ramp frequency limits
# leave it at 1, should be reasonable
RAMP_FREQUENCY_MIN = user_config.get("RAMP_FREQUENCY_MIN", 1)
# for high frequencies the autolock accuracy will go down
RAMP_FREQUENCY_MAX = user_config.get("RAMP_FREQUENCY_MAX", 100)

LOCK_THRESHOLD = user_config.get("LOCK_THRESHOLD", 0.8)
LOCK_THRESHOLD_BREAK = user_config.get("LOCK_THRESHOLD_BREAK", 0.6)

# ADwin variables
SAMPLING_RATE = 200e3
FIFO_BUFFER_SIZE = 30003  # Buffer size that is choosen on the adwin system.
FIFO_MAXLEN = 3000
NUMBER_OF_FILTERS = 5
NUMBER_OF_SOS = 5

###########################################################################################
# ADwin parameter index assignments (don't change, these are mostly for better readability)
###########################################################################################
PAR_TIMER = 1
PAR_RELOADBIT = 2
PAR_ACTIVE_CHANNEL = 4
PAR_FIFOSTEPSIZE = 6
PAR_TIMEDIFF = 7
PAR_SENSITIVITY = 8
# Filter Control Register, used as `10 + servo_channel`, so PAR 11-18 are also occupied
PAR_FCR = 10
# Lock control register 1: contains search bits, locked bits and relock bits
PAR_LCR = 19
# Second lock control register: contains greater bits and rampmode bits
PAR_GCR = 20

DATA_FILTERCOEFFS = 1
DATA_OFFSETGAIN = 2
DATA_FIFO = 3
DATA_LAST_OUTPUT = 4
DATA_MONITORS = 6
DATA_LOCK = 8
DATA_LOCK_ITER = 9
DATA_LOCK_OUTPUT = 10
DATA_LOCK_STEPSIZE = 11

##########################################################
################# local settings import ##################
##########################################################
# This is a selfmade alternative to dotenv that does not have the problems with different types.
# It will overwrite default settings with the custom settings that are set.
try:
    from .settings_local import *  # pylint: disable=import-error,unused-wildcard-import,wildcard-import

    log.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
    log.info("Successfully imported custom settings.")
except ModuleNotFoundError:
    log.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
    log.info("Not importing settings_local.")
    # If the import fails use the default options
