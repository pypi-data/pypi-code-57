import platform
import psutil
import os


def get_memory_state(pid=None):
    """
    Get memory usage stats for the host or a single process
    """
    assert pid == None or isinstance(pid, int)

    if pid:
        p = psutil.Process(pid)
        mem = p.memory_info()

        rss = float(mem.rss) / 1024 / 1024 / 1024
        return rss
    else:
        mem = psutil.virtual_memory()
        total = float(mem.total) / 1024 / 1024 / 1024
        used = float(mem.used) / 1024 / 1024 / 1024
        free = float(mem.free) / 1024 / 1024 / 1024

        return total, used, free


def get_cpu_state(pid=None, interval=1):
    assert pid == None or isinstance(pid, int)

    if pid:
        p = psutil.Process(pid)
        return p.cpu_percent(interval=interval)
    else:
        return psutil.cpu_percent(interval)
