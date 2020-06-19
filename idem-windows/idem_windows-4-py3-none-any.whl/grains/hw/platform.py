import platform


async def load_cpuarch(hub):
    hub.grains.GRAINS.cpuarch = platform.machine()


async def load_nodename(hub):
    hub.grains.GRAINS.nodename = platform.node()


async def load_kernel_version(hub):
    hub.grains.GRAINS.kernelversion = platform.version()
