import os


async def load_pid(hub):
    hub.grains.GRAINS.pid = os.getpid()
