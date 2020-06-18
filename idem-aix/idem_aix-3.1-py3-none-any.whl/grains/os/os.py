import shutil


async def load_techlevel(hub):
    oslevel = shutil.which("oslevel")
    if oslevel:
        hub.grains.GRAINS.osrelease_techlevel = (
            await hub.exec.cmd.run([oslevel, "-r"])
        ).stdout.strip()


async def load_os(hub):
    release_info = lambda osrelease: tuple(
        int(x) if x.strip().isdigit() else x for x in osrelease.split(".")
    )

    oslevel = shutil.which("oslevel")
    uname = shutil.which("uname")
    if oslevel:
        hub.grains.GRAINS.osrelease = (await hub.exec.cmd.run(oslevel)).stdout.strip()
        hub.grains.GRAINS.osrelease_info = release_info(hub.grains.GRAINS.osrelease)
        hub.grains.GRAINS.osmajorrelease = hub.grains.GRAINS.osrelease_info[0]
        if uname:
            hub.grains.GRAINS.osfullname = (
                await hub.exec.cmd.run(uname)
            ).stdout.strip()
            hub.grains.GRAINS.osfinger = (
                f"{hub.grains.GRAINS.osfullname}-{hub.grains.GRAINS.osmajorrelease}"
            )
    hub.grains.GRAINS.oscodename = "unknown"


async def load_build(hub):
    hub.grains.GRAINS.osbuild = "unknown"
    bootinfo = shutil.which("bootinfo")
    if bootinfo:
        ret = await hub.exec.cmd.run([bootinfo, "-m"])
        hub.grains.GRAINS.osbuild = ret.stdout.strip()
