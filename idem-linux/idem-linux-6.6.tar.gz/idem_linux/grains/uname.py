import os


async def load_uname(hub):
    """
    Verify that idem-linux is running on linux
    """
    (
        hub.grains.GRAINS.kernel,
        hub.grains.GRAINS.nodename,
        hub.grains.GRAINS.kernelrelease,
        hub.grains.GRAINS.kernelversion,
        hub.grains.GRAINS.cpuarch,
    ) = os.uname()

    assert (
        hub.grains.GRAINS.kernel == "Linux"
    ), "idem-Linux is only intended for Linux systems"


async def load_ps(hub):
    """
    Let anyone else try to set this grain first, then fallback to a default
    """
    if not await hub.grains.init.wait_for("ps"):
        hub.log.info("Using default Linux 'ps' grain")
        hub.grains.GRAINS.ps = "ps -efHww"
