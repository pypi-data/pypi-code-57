############################################################################
#*** Magic DAQ Python Module ***
# This is the entry point for all easy daq functions
############################################################################

###############################################
#*** General Imports ***
###############################################

from magicdaq_client_64bit import MagicDAQClient64Bit

###############################################################################
# *** MagicDAQ Class and Methods ***
###############################################################################

#MagicDAQDevice inherits all methods from MagicDAQClient64Bit
class MagicDAQDevice(MagicDAQClient64Bit):
    def __init__(self):
        import magicdaq_client_64bit
        magicdaq_client_64bit.MagicDAQClient64Bit.__init__(self)