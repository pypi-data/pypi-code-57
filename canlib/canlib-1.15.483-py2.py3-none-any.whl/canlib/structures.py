import ctypes as ct


class CanBusStatistics(ct.Structure):
    """Result from reading bus statistics using `canlib.canlib.Channel.get_bus_statistics`.

    Attributes:
        busLoad (`int`): The bus load, expressed as an integer in the interval
            0 - 10000 representing 0.00% - 100.00% bus load.
        errFrame (`int`): Number of error frames.
        extData (`int`): Number of received extended (29-bit identifiers) data frames.
        extRemote (`int`): Number of received extended (29-bit identifiers) remote frames.
        overruns (`int`): The number of overruns detected by the hardware, firmware or driver.
        stdData (`int`): Number of received standard (11-bit identifiers) data frames.
        stdRemote (`int`): Number of received standard (11-bit identifiers) remote frames.

    """
    _fields_ = [
        ('stdData', ct.c_ulong),
        ('stdRemote', ct.c_ulong),
        ('extData', ct.c_ulong),
        ('extRemote', ct.c_ulong),
        ('errFrame', ct.c_ulong),
        ('busLoad', ct.c_ulong),
        ('overruns', ct.c_ulong),
        ]
