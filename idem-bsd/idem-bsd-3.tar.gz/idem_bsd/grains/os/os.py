import logging
import shutil

log = logging.getLogger(__name__)


async def _load_osrelease_freebsd(hub) -> str:
    version = shutil.which("freebsd-version")
    if version:
        return (await hub.exec.cmd.run([version, "-u"])).stdout


async def load_osbuild(hub):
    sysctl = shutil.which("sysctl")

    if sysctl:
        hub.grains.GRAINS.osbuild = (
            await hub.exec.cmd.run([sysctl, "-n", "kern.osrevision"])
        ).stdout.strip()
    else:
        hub.grains.GRAINS.osbuild = "unknown"


async def load_oscodename(hub):
    """
    BSD Doesn't have codenames so we'll use the BSD version of the user environment.
    """
    uname = shutil.which("uname")
    if uname:
        hub.grains.GRAINS.oscodename = (
            await hub.exec.cmd.run([uname, "-U"])
        ).stdout.strip()
    else:
        hub.grains.GRAINS.oscodename = "unknown"


async def load_osinfo(hub):
    hub.grains.GRAINS.os = hub.grains.GRAINS.kernel
    full_release = await _load_osrelease_freebsd(hub) or hub.grains.GRAINS.kernelrelease
    hub.grains.GRAINS.osmanufactuer = "unknown"
    hub.grains.GRAINS.osrelease = full_release.split("-", 1)[0]
    hub.grains.GRAINS.osfullname = f"{hub.grains.GRAINS.os}-{full_release}"
    hub.grains.GRAINS.osrelease_info = tuple(
        int(x) if x.isdigit() else x for x in hub.grains.GRAINS.osrelease.split(".")
    )
    hub.grains.GRAINS.osmajorrelease = int(hub.grains.GRAINS.osrelease_info[0])
    hub.grains.GRAINS.osfinger = (
        f"{hub.grains.GRAINS.os}-{hub.grains.GRAINS.osmajorrelease}"
    )
