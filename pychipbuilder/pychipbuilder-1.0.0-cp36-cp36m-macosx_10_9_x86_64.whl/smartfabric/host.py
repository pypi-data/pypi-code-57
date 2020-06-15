"""
Copyright 2020 zGlue, Inc.

Licensed under zOH License version 1.0 ("the license") that is included in the accompanying repository.  
You may not use this file except in compliance with the License. 
You may obtain a copy of the license at <https://zglue.com/oci/zohl1v>.

SmartFabric Interface Class

Class containing python wrappers for host device
configuration and initalization. This implementation
uses an FTDI host device configured for MPSSE use.
To use a different host device, modify this class accordingly.

TODO:
- Add VCP driver unload for Linux & MacOS environments
- Add functions for updating device drivers
"""

try:
    from chipbuilder.smartfabric import czip

except ImportError:
    import os, _ctypes, platform
    system = platform.system()

    if system == "Darwin":
        _ctypes.dlopen(os.path.join("/System","Library","Frameworks","IOKit.framework","IOKit"), 2)
        from chipbuilder.smartfabric import czip

from chipbuilder.smartfabric.exceptions import FTDIError
from chipbuilder.smartfabric.util import IS_CLI_CMD, OPEN_HOST_ATTR
from chipbuilder.smartfabric.util import SUCCESS, FAIL, FT_CLKDIV_LIST


# FTDI Supported Device Types

FT_DEVICE_2232H = 6
FT_DEVICE_4232H = 7
FT_DEVICE_232H  = 8

FT_SUPPORTED_DEVICES = [
    FT_DEVICE_2232H,
    FT_DEVICE_4232H,
    FT_DEVICE_4232H
]


class SF_Host(czip.zip):


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.isOpen = False


    def print_dev_info(self, devInfo):
        """
        Pretty print a list of FTDI device info.
        """

        for devId in devInfo.keys():
            print("Dev %d" % devId)
            print("    Flags=0x%x" % devInfo[devId]["Flags"])
            print("    Type=0x%x" % devInfo[devId]["Type"])
            print("    vnpId=0x%x" % devInfo[devId]["vnpId"])
            print("    LocId=0x%x" % devInfo[devId]["LocId"])
            print("    SerialNumber=%s" % devInfo[devId]["SerialNumber"])
            print("    Description=%s" % devInfo[devId]["Description"])


    def get_devs(self, prntDevs:int = 0):
        """
        Get description of connected FTDI devices.
        This function is supported on the CLI script.
        
        Args:
            prntDevs (int, optional): Flag to print device information on console.

        Returns:
            dict. Dictionary of devices and their descriptors::

                {
                    devId:{
                        'Flags':val,
                        'Type':val,
                        'Id':val,
                        'LocId':val,
                        'SerialNumber':val,
                        'Description':val,
                    }
                }
        """

        devInfo = self._get_devices()

        if prntDevs:
            self.print_dev_info(devInfo)
        
        return devInfo


    def get_numdevs(self):
        """
        Get number of connected FTDI devices.
        This function is supported on the CLI script.

        Returns:
            int. Number of connected FTDI devices.
        """
        numDevs = self._get_num_devices()
        print("Number of FTDI Devices: %s" % numDevs)
        
        return numDevs


    def select_device(self, sn:str, vnpId:int = None, devType:int = None, locId:int = None, desc:str = None):
        """
        Select an FTDI device given a set of descriptors. 
        The sn, devType, locId, and vendor and product Id
        are the most useful identifiers to select a device.
        The function will try to match all provided arguments agains
        the current ftDevId.

        Returns:
            int. ftDevId for the matched device; returns FTDIError otherwise.
        """

        if devType != None and devType not in FT_SUPPORTED_DEVICES:
            raise ValueError("Type 0x%x is not supported" % devType)

        devInfo = self.get_devs()
        matched = True

        for devId in devInfo.keys():

            if sn != devInfo[devId]["SerialNumber"]:
                matched = False

            if vnpId != None and vnpId != devInfo[devId]["vnpId"]:
                matched = False

            if devType != None and devType != devInfo[devId]["Type"]:
                matched = False

            if locId != None and locId != devInfo[devId]["LocId"]:
                matched = False

            if desc != None and desc != devInfo[devId]["Description"]:
                matched = False

            if matched:
                print("FTDI ID %d selected" % devId)
                self.set_ftdev_id(devId)
                return devId

            matched = True

        raise FTDIError("No FTDI device matched")


    def connect(self, ftDevId:int = None, latencyMs:int = None):
        """
        Connect to FTDI device.

        Args:
            ftDevId (int, optional): FTDI device ID (default=None). See _get_devices() for device list.
            latencyMs (int, optional): MPSSE read buffer timout latency for filling buffer.
        
        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """

        ret = 0

        if not self.isOpen:

            if ftDevId != None and latencyMs != None:
                ret = self._zip_connect(ftDevId, latencyMs)

            elif ftDevId != None and latencyMs == None:
                ret = self._zip_connect(ftDevId=ftDevId)

            elif ftDevId == None and latencyMs != None:
                ret = self._zip_connect(latencyMs=latencyMs)

            else:
                ret = self._zip_connect()

            self.isOpen = True
        
        else:
            print("FTDI Device %d already open" % self.ftDevId)

        return ret


    def configure(self, clkDiv:int = None):
        """
        Configure host device for JTAG communication.

        Args:
            clkDiv (int, optional): Divisor for MPSSE clock.

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """


        if clkDiv != None:
            ret = self._zip_configure(clkDiv)

        else:
            ret = self._zip_configure()

        return ret


    def close(self):
        """
        Close FTDI device.

        Returns:
            int. A status code::

                Success = 0
                Failure > 0
        """

        if self.isOpen:
            ret = self._zip_close()
        else:
            ret = 0
            print("FTDI Device %d already closed" % self.ftDevId)

        self.isOpen = False

        return ret


    def idle(self, sync:bool = True):
        """
        Set JTAG TAP state machine to IDLE state.

        Args:
            sync (bool, optional): Force JTAG transaction.

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """

        ret = self._zip_idle(sync)

        return ret


    def open(self, ftDevId:int = None, latencyMs:int = None, freq:float = None):
        """
        Open Host Device. This function uses ``connect()``, ``configure``, and
        ``idle()`` to correctly initialize the selected device.

        Args:
            ftDevId (int, optional): FTDI device ID (default=None). See _get_devices() for device list.
            latencyMs (int, optional): MPSSE read buffer timout latency for filling buffer.
            freq (float, optinoal): JTAG clock frequency in Hz as float.

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """
        
        ret = 0

        if ftDevId != None:
            ret |= self.set_ftdev_id(ftDevId)

        if latencyMs != None:
            ret |= self.set_latency(latencyMs)
        
        if freq != None:
            ret |= self.set_jtag_freq(freq)

        if ret == -1:
            raise ValueError("open - failed to set class attributes")

        ret |= self.connect()
        ret |= self.configure()
        ret |= self.idle()

        return ret


    ##################################################
    ###             ATTRIBUTES GET-SET             ###
    ##################################################

    def get_ftdev_id(self):
        """Get the FTDI device index to open."""

        return self.ftDevId


    def set_ftdev_id(self, idx):
        """Set the FTDI device index to open.

        Args:
            idx -- FTDI device index
        """

        if type(idx) != type(int()):
            print("ftDevId - int required, got %s" % type(numCycles))
            return -1

        numDevs = self._get_num_devices()

        if idx in [i for i in range(0, numDevs)]:
            self.ftDevId = idx    
        
        else:
            print("Invalid FTDI device ID")
            return -1

        return SUCCESS


    def get_latency(self):
        """Get the MPSSE read buffer timeout latency."""

        return self.latencyMs


    def set_latency(self, latencyMs):
        """Set the MPSSE read buffer timeout latency.

        Args:
            latencyMs -- latency for read buffer timout in milliseconds
        """

        if type(latencyMs) != type(int()):
            print("latencyMs - int required, got %s" % type(numCycles))
            return -1

        if latencyMs > 1 or latencyMs < 256:
            self.latencyMs = latencyMs    
        
        else:
            print("Invalid read latency. Possible range is 1 < latency < 256")
            return -1

        return SUCCESS


    def get_jtag_freq(self):
        """Get the JTAG clock frequency."""

        return self.freq


    def set_jtag_freq(self, freq):
        """Set the JTAG clock frequency.

        Args:
            freq -- JTAG clock frequency in Hz as float
        """

        if type(freq) != type(float()):
            print("freq - float required, got %s" % type(freq))
            return -1

        try:
            self.clkDiv = FT_CLKDIV_LIST.index(freq)

        except ValueError:
            print("%0.1fHz not supported" % freq)
            print("Use print_frequencies functions to see available options.")
            return -1

        self.freq = freq

        return SUCCESS


    def get_stall_cycles(self):
        """Set the number of stall cycles for OTP programming."""

        return self.stallCycles


    def set_stall_cycles(self, numCycles):
        """Set the number of stall cycles for OTP programming. This attribute has been
        set to 300 cycles by default. This value works for 1MHz JTAG clock; however, changing
        the JTAG clock frequency means that the stall time scales inversly proportional. Modify this attribute
        at your own risk.

        Args:
            numCycles -- number of cycles for OTP programming
        """

        if type(numCycles) != type(int()):
            print("stallCycles - int required, got %s" % type(numCycles))
            return -1

        if numCycles > 8 or numCycles > 524280:
            self.stallCycles = numCycles    
        
        else:
            print("Invalid number of cycles")
            return -1

        return SUCCESS


    setattr(get_devs, IS_CLI_CMD, True)
    setattr(get_numdevs, IS_CLI_CMD, True)
    # setattr(connect, IS_CLI_CMD, False)
    # setattr(configure, IS_CLI_CMD, False)
    # setattr(close, IS_CLI_CMD, False)
    # setattr(idle, IS_CLI_CMD, False)
    # setattr(open, IS_CLI_CMD, False)

    # setattr(get_devs, OPEN_HOST_ATTR, False)
    # setattr(get_numdevs, OPEN_HOST_ATTR, False)
    setattr(connect, OPEN_HOST_ATTR, True)
    setattr(configure, OPEN_HOST_ATTR, True)
    setattr(close, OPEN_HOST_ATTR, True)
    setattr(idle, OPEN_HOST_ATTR, True)
    setattr(open, OPEN_HOST_ATTR, True)

