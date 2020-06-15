"""
Copyright 2020 zGlue, Inc.

Licensed under zOH License version 1.0 ("the license") that is included in the accompanying repository.  
You may not use this file except in compliance with the License. 
You may obtain a copy of the license at <https://zglue.com/oci/zohl1v>.

SmartFabric Python Package

Author (s): Jorge L. Rojas

Description: 
    Python package for zGlue's Smart Fabric active interposer.
    This package works as a wrapper around FTDI's ftd2xx DLL, which 
    provides an API to issue MPSSE commands over USB.
"""

import os
import math
import time
import faulthandler

from chipbuilder.smartfabric.util import SUCCESS

try:
    from chipbuilder.smartfabric.debug import SF_Internal

except ImportError:
    from chipbuilder.smartfabric.host import SF_Host

    # class SF_Internal:
    class SF_Internal(SF_Host):
        pass

from chipbuilder.smartfabric.led  import SF_LED
from chipbuilder.smartfabric.otp  import SF_OTP
from chipbuilder.smartfabric.pmic import SF_PMIC
from chipbuilder.smartfabric.tgrid   import SF_TileGrid


faulthandler.enable()


class SmartFabric(
    SF_Internal, 
    SF_TileGrid, 
    SF_OTP, 
    SF_PMIC, 
    SF_LED
):
    """
    Class for zGlue's SmartFabric active interposer.
    """

    def __init__(self, devid = 0, latency = 2, freq = 1.0E6, scycles = 300):

        self.isOpen = False
        rc = self.set_jtag_freq(freq)

        if rc == SUCCESS:
            super().__init__(
                ftDevId = devid, 
                latencyMs = latency, 
                clkDiv = self.clkDiv, 
                stallCycles = scycles
            )
        else:
            super().__init__(
                ftDevId = devid, 
                latencyMs = latency, 
                stallCycles = scycles
            )


