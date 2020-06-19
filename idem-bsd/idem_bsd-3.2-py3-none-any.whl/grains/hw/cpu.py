import aiofiles
import os
import re
import shutil
from typing import List


async def _load_sysctl_cpus(hub) -> int:
    sysctl = shutil.which("sysctl")
    if sysctl:
        ret = await hub.exec.cmd.run([sysctl, "-n", "hw.ncpu"])
        if not ret.retcode:
            return int(ret.stdout)


async def _load_sysctl_arch(hub) -> str:
    sysctl = shutil.which("sysctl")
    if sysctl:
        ret = await hub.exec.cmd.run([sysctl, "-n", "hw.machine"])
        if not ret.retcode:
            return ret.stdout.strip()


async def _load_sysctl_model(hub) -> str:
    sysctl = shutil.which("sysctl")
    if sysctl:
        ret = await hub.exec.cmd.run([sysctl, "-n", "hw.model"])
        if not ret.retcode:
            return ret["stdout"].strip()


async def _load_sysctl_flags(hub) -> str:
    sysctl = shutil.which("sysctl")
    if sysctl:
        ret = await hub.exec.cmd.run([sysctl, "-n", "machdep.cpu.features"])
        if not ret.retcode:
            return ret.stdout.strip().split(" ")


async def _load_arch(hub) -> str:
    arch = shutil.which("arch")
    if arch:
        ret = await hub.exec.cmd.run([arch, "-s"])
        if not ret.retcode:
            return ret.stdout.strip()


async def _load_cpuctl_flags(hub) -> List[str]:
    cpu_flags = []
    cputil = shutil.which("cputil")
    if cputil:
        ret = await hub.exec.cmd.run([cputil, "identify", "0"])
        for line in ret.stdout.splitlines():
            cpu_match = re.match(r"cpu[0-9]: features[0-9]? .+<(.+)>", line)
            if cpu_match:
                flag = cpu_match.group(1).split(",")
                cpu_flags.extend(flag)

    return cpu_flags


async def _load_dmesg_boot_flags(hub) -> List[str]:
    cpu_flags = []
    dmesg_boot = "/var/run/dmesg.boot"

    if os.path.exists(dmesg_boot):
        async with aiofiles.open(dmesg_boot, "r") as _fp:
            cpu_here = False
            async for line in _fp:
                if line.startswith("CPU: "):
                    cpu_here = True  # starts CPU descr
                    continue
                if cpu_here:
                    if not line.startswith(" "):
                        break  # game over
                    if "Features" in line:
                        start = line.find("<")
                        end = line.find(">")
                        if start > 0 and end > 0:
                            flag = line[start + 1 : end].split(",")
                            cpu_flags.extend(flag)
    return cpu_flags


async def load_cpu_arch(hub):
    hub.grains.GRAINS.cpuarch = (
        await _load_sysctl_arch(hub)
        or await _load_arch(hub)
        or hub.grains.GRAINS.get("osarch")
    )


async def load_cpu_flags(hub):
    hub.grains.GRAINS.cpu_flags = sorted(
        map(
            str.lower,
            set(await _load_cpuctl_flags(hub) or await _load_dmesg_boot_flags(hub)),
        )
    )

    # Report if hardware virtualization is available under amd or intel
    hub.grains.GRAINS.hardware_virtualization = any(
        f in hub.grains.GRAINS.cpu_flags for f in ("svm", "vmx")
    )


async def load_cpu_model(hub):
    hub.grains.GRAINS.cpu_model = await _load_sysctl_model(hub)


async def load_num_cpus(hub):
    hub.grains.GRAINS.num_cpus = await _load_sysctl_cpus(hub) or 1
