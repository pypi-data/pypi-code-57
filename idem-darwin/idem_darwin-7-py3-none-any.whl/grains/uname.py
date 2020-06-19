import os


async def load_uname(hub):
    """
    Verify that POP linux is running on linux
    """
    (
        hub.grains.GRAINS.kernel,
        hub.grains.GRAINS.nodename,
        hub.grains.GRAINS.kernelrelease,
        hub.grains.GRAINS.kernelversion,
        _,
    ) = os.uname()

    assert (
        hub.grains.GRAINS.kernel == "Darwin"
    ), "POP-Darwin is only intended for MacOS based systems"

    # Hard-coded grains for mac
    hub.grains.GRAINS.init = "launchd"
    hub.grains.GRAINS.osmanufacturer = hub.grains.GRAINS.manufacturer = "Apple Inc."
    hub.grains.GRAINS.os_family = "MacOS"
    hub.grains.GRAINS.ps = "ps auxwww"
