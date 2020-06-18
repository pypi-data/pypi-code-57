import shutil


async def load_init(hub):
    if shutil.which("rc"):
        hub.grains.GRAINS.init = "rc"
    else:
        hub.grains.GRAINS.init = "unknown"
