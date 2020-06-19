import aiofiles
import os
import shutil


async def load_systemd(hub):
    cmd = shutil.which("systemctl")
    if cmd and shutil.which("localectl"):
        hub.log.debug("Adding systemd grains")
        ret = await hub.exec.cmd.run([cmd, "--version"])
        if ret.retcode:
            hub.log.error(ret.stderr)
        else:
            systemd_info = ret.stdout.strip().splitlines()
            hub.grains.GRAINS.systemd.version = systemd_info[0].split()[1]
            hub.grains.GRAINS.systemd.features = systemd_info[1]


async def _load_cgroup(hub) -> str:
    path = "/proc/1/cgroup"
    if os.path.exists(path):
        async with aiofiles.open(path) as fh_:
            data = await fh_.read()
            if "docker" in data:
                return "docker"
            elif "name=" in data:
                name = data.split("name=")[1]
                return name.split(":")[0]


def _load_systemd(hub) -> str:
    system = "/run/systemd/system"
    if os.path.exists(system) and os.stat(system):
        return "systemd"


async def _load_bin(hub, init_bin: str) -> str:
    supported_inits = (b"upstart", b"sysvinit", b"systemd")
    edge_len = max(len(x) for x in supported_inits) - 1
    try:
        async with aiofiles.open(init_bin, "rb") as fp_:
            edge = b""
            buf = (await fp_.read(hub.OPT.grains.file_buffer_size)).lower()
            while buf:
                if isinstance(buf, str):
                    # This makes testing easier
                    buf = buf.encode()
                buf = edge + buf
                for item in supported_inits:
                    if item in buf:
                        return item.decode("utf-8")
                edge = buf[-edge_len:]
                buf = (await fp_.read(hub.OPT.grains.file_buffer_size)).lower()
    except (IOError, OSError) as exc:
        hub.log.error(f"Unable to read from init_bin ({init_bin}): {exc}")


async def _load_cmdline(hub) -> str:
    cmdline = "/proc/1/cmdline"

    if not os.path.exists(cmdline):
        return ""

    async with aiofiles.open(cmdline) as fhr:
        init_cmdline = (await fhr.read()).replace("\x00", " ").strip().split()
        if not init_cmdline:
            # Emtpy init_cmdline
            hub.log.warning("Unable to fetch data from /proc/1/cmdline")
            return ""

    if "runit" in init_cmdline:
        return "runit"
    elif "/sbin/my_init" in init_cmdline:
        # Phusion Base docker container use runit for srv mgmt, but
        # my_init as pid1
        return "runit"
    else:
        for init in (
            "supervisord",
            # https://github.com/Yelp/dumb-init
            "dumb-init",
            # https://github.com/krallin/tini
            "tini",
        ):
            if shutil.which(init) in init_cmdline:
                return init

    init_bin = shutil.which(init_cmdline[0])
    if init_bin.endswith("bin/init"):
        return await _load_bin(hub, init_bin)
    else:
        hub.log.debug(
            f"Could not determine init system from command line: {init_cmdline}"
        )


async def load_init(hub):
    # Add init grain
    # Default to the cgroup
    hub.log.debug("Adding init grain")
    hub.grains.GRAINS.init = (
        await _load_cgroup(hub)
        or _load_systemd(hub)
        or await _load_cmdline(hub)
        or "unknown"
    )
