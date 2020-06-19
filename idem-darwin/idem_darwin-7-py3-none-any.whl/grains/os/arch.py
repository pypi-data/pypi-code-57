import os


async def load_osarch(hub):
    hub.grains.GRAINS.osarch = os.uname().machine
