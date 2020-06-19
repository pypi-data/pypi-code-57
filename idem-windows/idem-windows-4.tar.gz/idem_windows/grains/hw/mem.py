import win32api


async def load_memdata(hub):
    """
    Return the memory information for Windows systems
    """
    # get the Total Physical memory as reported by msinfo32
    tot_bytes = win32api.GlobalMemoryStatusEx()["TotalPhys"]
    # return memory info in gigabytes
    hub.grains.GRAINS.mem_total = int(tot_bytes / (1024 ** 2))


async def load_swapdata(hub):
    page_file_usage = await hub.exec.wmi.get("Win32_PageFileUsage", 0)
    hub.grains.GRAINS.swap_total = int(page_file_usage.AllocatedBaseSize)
