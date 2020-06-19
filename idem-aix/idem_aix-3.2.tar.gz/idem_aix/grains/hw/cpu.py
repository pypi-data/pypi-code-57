# Provides:
#   cpuarch
#   num_cpus
#   cpu_model
#   cpu_flags
import re
import shutil


async def load_cpuinfo(hub):
    """
    Return CPU information for AIX systems
    """
    clean = lambda x: x.strip().replace("'", "")

    prtconf = shutil.which("prtconf")
    if prtconf:
        ret = await hub.exec.cmd.run(prtconf)

        # Load cpuarch
        match = re.search(r"(?im)^\s*Processor\s+Type:\s+(\S+)", ret.stdout)
        if match:
            hub.grains.GRAINS.osarch = hub.grains.GRAINS.cpuarch = clean(match.group(1))

        # Load cpu_model
        match = re.search(
            r"(?im)^\s*Processor\s+Implementation\s+Mode:\s+(.*)", ret.stdout
        )
        if match:
            hub.grains.GRAINS.cpu_model = clean(match.group(1))

        # Load num_cpus
        match = re.search(r"(?im)^\s*Number\s+Of\s+Processors:\s+(\S+)", ret.stdout)
        if match:
            hub.grains.GRAINS.num_cpus = int(clean(match.group(1)))


async def load_cpu_flags(hub):
    cpu_flags = []

    lsattr = shutil.which("lsattr")
    if lsattr:
        ret = await hub.exec.cmd.run([lsattr, "-El", "sys0"])
        for line in ret.stdout.strip().splitlines():
            vals = line.split()
            if vals[-1] == "True":
                cpu_flags.append(vals[0].split()[0])

    hub.grains.GRAINS.cpu_flags = sorted(cpu_flags)


async def load_hardware_virtualization(hub):
    hub.grains.GRAINS.hardware_virtualization = False

    #  Specifies whether the machine hardware is MP-capable
    #  (capable of running the multi-processor kernel and supporting more than one processor).
    bootinfo = shutil.which("bootinfo")
    if bootinfo:
        ret = await hub.exec.cmd.run([bootinfo, "-z"])
        hub.grains.GRAINS.hardware_virtualization = ret.stdout.startswith("1")
