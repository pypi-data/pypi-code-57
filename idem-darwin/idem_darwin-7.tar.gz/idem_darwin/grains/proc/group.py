import os
import grp


async def load_group(hub):
    hub.grains.GRAINS.gid = os.getegid()
    hub.grains.GRAINS.groupname = grp.getgrgid(hub.grains.GRAINS.gid).gr_name
