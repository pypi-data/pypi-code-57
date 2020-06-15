"""
Copyright 2020 zGlue, Inc.

Licensed under zOH License version 1.0 ("the license") that is included in the accompanying repository.  
You may not use this file except in compliance with the License. 
You may obtain a copy of the license at <https://zglue.com/oci/zohl1v>.

Exceptions module for chipbuilder.smartfabric
"""

class ChipBuilerError(Exception):
    """Base class for ChipBuilder errors"""
    pass



class HostError(Exception):
    """Base class for Host device errors"""
    pass



class FTDIError(HostError):
    """Base class for FTDI host device errors"""
    pass