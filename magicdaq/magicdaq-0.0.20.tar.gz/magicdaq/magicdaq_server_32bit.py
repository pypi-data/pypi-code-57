###############################################
#*** 32 Bit Magic DAQ Server ***
#Server is used with a 64 bit client to allow 64 bit python to use the 32 bit MagicDAQ Python API
###############################################

###############################################
#*** Imports ***
###############################################

from loadlib import Server32

# This is used if you want the easydaq code to be run locally by the 32bit server
# Commented out as we want the easydaq code contained within the 32bit server
#import easydaq

###############################################
#*** How to Re-Freeze Server ***
###############################################

#Use the API as described:
#https://msl-loadlib.readthedocs.io/en/latest/refreeze.html

#I have written a script to re-freeze:
#python32 freezeserver.py

###############################################
#*** Server Class ***
###############################################

# If you want the easydaq code run locally by the 32bit server, do this:
# class MagicDAQServer32Bit(Server32, easydaq.DAQDevice):
# If you want to run locally, be sure you remove easydaq.Device from server32.py

# Server32 class has all easydaq methods as sub class. Go see Server32
class MagicDAQServer32Bit(Server32):

    def __init__(self, host, port, quiet, **kwargs):
        # This line taken directly from example server
        # https://msl-loadlib.readthedocs.io/en/latest/interprocess_communication.html
        super(MagicDAQServer32Bit, self).__init__('magicdaq.dll', 'cdll', host, port, quiet)

        # If you want the easydaq code run locally by the 32bit server, do this:
        # easydaq.DAQDevice.__init__(self)
        # If you want to run locally, be sure you removed the easydaq.DAQDevice.__init__(self) from
        # server32.py __init__() method

    #*** All DAQDevice Methods ***
    #Are inherited. See MagicDAQServer32Bit definition

