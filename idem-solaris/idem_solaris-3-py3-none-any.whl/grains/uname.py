import os
import sys


async def load_uname(hub):
    """
    Verify that idem-solaris is running on SunOS
    """
    (
        hub.grains.GRAINS.kernel,
        hub.grains.GRAINS.nodename,
        hub.grains.GRAINS.kernelrelease,
        hub.grains.GRAINS.kernelversion,
        hub.grains.GRAINS.osarch,
    ) = os.uname()

    assert (
        hub.grains.GRAINS.kernel == "SunOS"
    ), "idem-solaris is only intended for SunOs systems"

    # Determine if host is SmartOS (Illumos) or not
    hub.grains.GRAINS.smartos = sys.platform.startswith(
        "sunos"
    ) and hub.grains.GRAINS.kernelversion.startswith("joyent_")

    # Hard coded grains for SunOs go here:
