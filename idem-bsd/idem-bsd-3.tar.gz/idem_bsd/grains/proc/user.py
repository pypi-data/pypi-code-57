import os
import pwd


async def load_user(hub):
    hub.grains.GRAINS.uid = os.geteuid()
    hub.grains.GRAINS.username = pwd.getpwuid(hub.grains.GRAINS.uid).pw_name
