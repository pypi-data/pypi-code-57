import shutil


async def _load_swapctl(hub) -> int:
    swapctl = shutil.which("swapctl")

    if swapctl:
        swap_data = (await hub.exec.cmd.run([swapctl, "-sk"])).stdout.strip()
        if swap_data != "no swap devices configured":
            return int(swap_data.split()[1]) // 1024


async def _load_sysctl_swap(hub) -> int:
    sysctl = shutil.which("sysctl")
    if sysctl:
        return (
            int((await hub.exec.cmd.run([sysctl, "-n", "vm.swap_total"])).stdout)
            // 1024
            // 1024
        )


async def load_swap(hub):
    """
    Return the swap information for BSD-like systems
    """
    hub.grains.GRAINS.swap_total = (
        await _load_swapctl(hub) or await _load_sysctl_swap(hub) or 0
    )


async def load_meminfo(hub):
    """
    Return the memory information for BSD-like systems
    """
    hub.grains.GRAINS.mem_total = 0

    sysctl = shutil.which("sysctl")

    if sysctl:
        mem = int((await hub.exec.cmd.run([sysctl, "-n", "hw.physmem"])).stdout)
        if mem < 0:
            mem = int((await hub.exec.cmd.run([sysctl, "-n", "hw.physmem64"])).stdout)
        hub.grains.GRAINS.mem_total = mem // 1024 // 1024
