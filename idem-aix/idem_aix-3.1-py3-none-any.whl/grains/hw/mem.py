import re
import shutil


async def load_meminfo(hub):
    """
    Return the memory information for AIX systems
    """
    hub.grains.GRAINS.mem_total = 0

    prtconf = shutil.which("prtconf")
    if prtconf:
        ret = await hub.exec.cmd.run([prtconf, "-m"])
        hub.grains.GRAINS.mem_total = int(ret.stdout.strip().split()[2])
    else:
        hub.log.error("Could not find `prtconf` binary in $PATH")


async def load_swapinfo(hub):
    hub.grains.GRAINS.swap_total = 0

    swap = shutil.which("swap")
    if swap:
        # allocated = 688128 blocks used = 2664 blocks free = 685464 blocks
        ret = await hub.exec.cmd.run([swap, "-s"])
        match = re.search(
            "blocks\s+used\s+=\s+(\d+)\s+blocks\s+free\s+=\s+(\d+)\s+blocks",
            ret.stdout.strip(),
        )
        if match:
            hub.grains.GRAINS.swap_total = (
                int(match.group(1)) + int(match.group(2))
            ) * 4
    else:
        hub.log.error("Could not find `swap` binary in $PATH")
