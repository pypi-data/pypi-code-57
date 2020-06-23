"""
This module includes wrapper classes for Tool connection parameters
"""

#pylint: disable=too-few-public-methods
class ToolConnection(object):
    """
    Base class for ToolConnection classes used to wrap configuration parameters for tool connections
    """

#pylint: disable=too-few-public-methods
class ToolUsbHidConnection(ToolConnection):
    """
    Helper class wrapping configuration parameters for a connection to a USB HID tool
    """
    serial_number = None
    tool_name = None

    def __init__(self, serial_number=None, tool_name=None):
        """
        :param tool_name: Tool name as given in USB Product string.  Some shortnames are also supported
            as defined in pyedbglib.hidtransport.toolinfo.py.  Set to None if don't care
        :param serial_number: USB serial number string.  Set to None if don't care
        """
        self.serial_number = serial_number
        self.tool_name = tool_name

#pylint: disable=too-few-public-methods
class ToolSerialConnection(ToolConnection):
    """
    Helper class wrapping configuration parameters for a connection to a serial port
    """
    serialport = None

    def __init__(self, serialport="COM1"):
        self.serialport = serialport
