import os


async def load_uname(hub):
    """
    Verify that idem-aix is running on AIX
    """
    (
        hub.grains.GRAINS.kernel,
        hub.grains.GRAINS.nodename,
        hub.grains.GRAINS.kernelrelease,
        hub.grains.GRAINS.kernelversion,
        _,
    ) = os.uname()
    assert (
        hub.grains.GRAINS.kernel == "AIX"
    ), "idem-AIX is only intended for AIX systems"

    # Hard coded grains for AIX systems
    hub.grains.GRAINS.os_family = hub.grains.GRAINS.os = "AIX"
    hub.grains.GRAINS.osmanufacturer = "International Business Machines Corporation"
    hub.grains.GRAINS.virtual = "physical"
    hub.grains.GRAINS.ps = "/usr/bin/ps auxww"
