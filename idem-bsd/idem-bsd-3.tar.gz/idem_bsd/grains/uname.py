import os


async def load_uname(hub):
    """
    Verify that idem-BSD is running on BSD
    """
    (
        hub.grains.GRAINS.kernel,
        hub.grains.GRAINS.nodename,
        hub.grains.GRAINS.kernelrelease,
        hub.grains.GRAINS.kernelversion,
        hub.grains.GRAINS.osarch,
    ) = os.uname()

    assert hub.grains.GRAINS.kernel.upper().endswith(
        "BSD"
    ), "idem-bsd is only intended for BSD systems"

    # Hard coded grains for BSD
    hub.grains.GRAINS.os_family = "BSD"
    hub.grains.GRAINS.ps = "ps auxwww"
