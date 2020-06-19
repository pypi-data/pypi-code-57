import aiofiles
import os


async def load_meminfo(hub):
    """
    Return the memory information for Linux-like systems
    """
    hub.grains.GRAINS.mem_total = 0
    hub.grains.GRAINS.swap_total = 0

    meminfo = "/proc/meminfo"
    if os.path.isfile(meminfo):
        async with aiofiles.open(meminfo, "r") as ifile:
            async for line in ifile:
                comps = line.rstrip("\n").split(":")
                if not len(comps) > 1:
                    continue
                if comps[0].strip() == "MemTotal":
                    # Use floor division to force output to be an integer
                    hub.grains.GRAINS.mem_total = int(comps[1].split()[0]) // 1024
                if comps[0].strip() == "SwapTotal":
                    # Use floor division to force output to be an integer
                    hub.grains.GRAINS.swap_total = int(comps[1].split()[0]) // 1024
