import os
import shutil


async def get_osarch(hub):
    # Build the osarch grain. This grain will be used for platform-specific
    # considerations such as package management. Fall back to the CPU architecture.
    if shutil.which("uname"):
        ret = await hub.exec.cmd.run(["uname", "-m"])
        hub.grains.GRAINS.osarch = ret.stdout.strip()
    elif shutil.which("rpm") and os.environ.get("_host_cpu"):
        ret = await hub.exec.cmd.run(
            ["rpm", "--eval", os.environ["_host_cpu"]], shell=True
        )
        hub.grains.GRAINS.osarch = ret.stdout.strip() or "unknown"
    elif shutil.which("opkg"):
        archinfo = {}
        for line in (
            (await hub.exec.cmd.run(["opkg", "print-architecture"])).stdout
        ).splitlines():
            if line.startswith("arch"):
                _, arch, priority = line.split()
                archinfo[arch.strip()] = int(priority.strip())
        # Return osarch in priority order (higher to lower)
        hub.grains.GRAINS.osarch = sorted(archinfo, key=archinfo.get, reverse=True)[0]
    elif shutil.which("dpkg"):
        hub.grains.GRAINS.osarch = (
            await hub.exec.cmd.run("dpkg --print-architecture")
        )["stdout"].strip()
    else:
        # WOW64 processes mask the native architecture
        if "PROCESSOR_ARCHITEW6432" in os.environ:
            hub.grains.GRAINS.osarch = os.environ.get("PROCESSOR_ARCHITEW6432", "")
        else:
            hub.grains.GRAINS.osarch = os.environ.get("PROCESSOR_ARCHITECTURE", "")
