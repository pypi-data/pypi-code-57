import shutil


async def load_mem(hub):
    """
    Return the memory information for BSD-like systems
    """
    sysctl = shutil.which("sysctl")
    if sysctl:
        hub.grains.GRAINS.mem_total = (
            int((await hub.exec.cmd.run([sysctl, "-n", "hw.memsize"])).stdout.strip())
            // 1024
            // 1024
        )


async def load_swap(hub):
    sysctl = shutil.which("sysctl")
    if sysctl:
        swap_total = (
            (await hub.exec.cmd.run([sysctl, "-n", "vm.swapusage"]))
            .stdout.strip()
            .split()[2]
            .replace(",", ".")
        )
        if swap_total.endswith("K"):
            _power = 2 ** 10
        elif swap_total.endswith("M"):
            _power = 2 ** 20
        elif swap_total.endswith("G"):
            _power = 2 ** 30
        swap_total = float(swap_total[:-1]) * _power

        hub.grains.GRAINS.swap_total = int(swap_total) // 1024 // 1024
