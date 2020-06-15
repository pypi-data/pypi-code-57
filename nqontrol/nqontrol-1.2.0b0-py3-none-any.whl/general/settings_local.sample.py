## To use custom settings copy this sample to settings_local.py or customize it at ~/.nqontrol.py
## The settings_local.py will overwrite the user config file.
## Find a more detailed list of possible settings in the settings.py file.

#################### Local configuration ####################
## Use 0 to enable a dummy device. Otherwise use the channel number
DEVICE_NUM = 0  # The 0 is reserved to mock device for testing!

## Host and port of the local webserver
# HOST = "127.0.0.1"
# PORT = 8000

## Specify a file to store the servo configuration, but choose an absolute file name.
## On each saving event an automatic backup in the directory of the settings file can be created.
# SETTINGS_FILE = 'test.json'
# CREATE_SETTINGS_BACKUP = False
# BACKUP_SUBSTRING = "%Y-%m-%d_%H-%M-%S"

## Set the logging level if you want more verbose output.
# LOG_LEVEL = 'INFO'  # Default 'WARNING'

## The DEBUG is for Dash debugging.
# DEBUG = True

## Reducing these numbers can increase the performance (especially the load time).
# NUMBER_OF_SERVOS = 8
# NUMBER_OF_MONITORS = 8

## These frequencies should work fine with the autolock,
## but there might be cases where you want to change it.
# RAMP_FREQUENCY_MAX = 100
# RAMP_FREQUENCY_MIN = 1

## Change the relative threshold values for the autolock (and relock)
## 1 is the extremum of the peak, 0 the median
# LOCK_THRESHOLD = 0.8
# LOCK_THRESHOLD_BREAK = 0.6
