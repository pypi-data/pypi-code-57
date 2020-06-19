"""
Return the memory information for SunOS-like systems
"""
import asyncio
import os
import shutil


async def load_meminfo(hub):
    hub.grains.GRAINS.mem_total = 0
    prtconf = shutil.which("prtconf") or "/usr/sbin/prtconf"

    if os.path.exists(prtconf):
        ret = await hub.exec.cmd.run(prtconf, stderr=asyncio.subprocess.DEVNULL)
        for line in ret.stdout.splitlines():
            comps = line.split(" ")
            if comps[0].strip() == "Memory" and comps[1].strip() == "size:":
                hub.grains.GRAINS.mem_total = int(comps[2].strip())
                break


async def load_swap(hub):
    hub.grains.GRAINS.swap_total = 0

    swap_cmd = shutil.which("swap")
    if swap_cmd:
        # total: 605092k bytes allocated + 401380k reserved = 1006472k used, 4116500k available
        ret = await hub.exec.cmd.run([swap_cmd, "-s"])
        swap_data = ret.stdout.strip().split()
        try:
            swap_avail = int(swap_data[-2][:-1])
            swap_used = int(swap_data[-4][:-1])
            hub.grains.GRAINS.swap_total = (swap_avail + swap_used) // 1024
        except ValueError:
            pass
