import sys


async def load_kernel(hub):
    """
    Verify that POP linux is running on windows
    """
    if sys.platform.startswith("win"):
        hub.grains.GRAINS.kernel = "Windows"
    else:
        raise OSError("POP-Windows is only intended for Windows systems")

    # Hard coded grainss for windows systems
    hub.grains.GRAINS.init = "Windows"
    hub.grains.GRAINS.os_family = "Windows"
    hub.grains.GRAINS.ps = "tasklist.exe"
