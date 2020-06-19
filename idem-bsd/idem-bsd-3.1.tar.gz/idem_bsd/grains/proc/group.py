import os
import grp


async def load_group(hub):
    hub.grains.GRAINS.gid = os.getegid()
    try:
        hub.grains.GRAINS.groupname = grp.getgrgid(hub.grains.GRAINS.gid).gr_name
    except KeyError:
        hub.grains.GRAINS.groupname = None
