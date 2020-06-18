import aiofiles
import logging
import os
import shutil

log = logging.getLogger(__name__)


async def load_init(hub):
    log.debug("Adding init grain")
    hub.grains.GRAINS.init = "init"

    system = "/run/systemd/system"
    cmdline = "/proc/1/cmdline"

    if shutil.which("rc"):
        # The first choice for most BSD systems
        hub.grains.GRAINS.init = "rc"
    elif os.path.exists(system) and os.stat(system):
        hub.grains.GRAINS.init = "systemd"
    elif os.path.exists(cmdline):
        async with aiofiles.open("/proc/1/cmdline") as fhr:
            init_cmdline = (await fhr.read()).replace("\x00", " ").split()
            if len(init_cmdline) >= 1:
                init_bin = shutil.which(init_cmdline[0])
                if init_bin.endswith("bin/init"):
                    supported_inits = (b"upstart", b"sysvinit", b"systemd")
                    edge_len = max(len(x) for x in supported_inits) - 1
                    buf_size = hub.OPT.get("file_buffer_size", 262144)
                    try:
                        async with aiofiles.open(init_bin, "rb") as fp_:
                            edge = b""
                            buf = (await fp_.read(buf_size)).lower()
                            while buf:
                                if isinstance(buf, str):
                                    # This makes testing easier
                                    buf = buf.encode()
                                buf = edge + buf
                                for item in supported_inits:
                                    if item in buf:
                                        item = item.decode("utf-8")
                                        hub.grains.GRAINS.init = item
                                        buf = b""
                                        break
                                edge = buf[-edge_len:]
                                buf = (await fp_.read(buf_size)).lower()
                    except (IOError, OSError) as exc:
                        log.error(
                            "Unable to read from init_bin (%s): %s", init_bin, exc
                        )
                elif shutil.which("supervisord") in init_cmdline:
                    hub.grains.GRAINS.init = "supervisord"
                elif shutil.which("dumb-init") in init_cmdline:
                    # https://github.com/Yelp/dumb-init
                    hub.grains.GRAINS.init = "dumb-init"
                elif shutil.which("tini") in init_cmdline:
                    # https://github.com/krallin/tini
                    hub.grains.GRAINS.init = "tini"
                elif "runit" in init_cmdline:
                    hub.grains.GRAINS.init = "runit"
                elif "/sbin/my_init" in init_cmdline:
                    # Phusion Base docker container use runit for srv mgmt, but
                    # my_init as pid1
                    hub.grains.GRAINS.init = "runit"
                else:
                    log.debug(
                        "Could not determine init system from command line: (%s)",
                        " ".join(init_cmdline),
                    )
            else:
                # Emtpy init_cmdline
                log.warning("Unable to fetch data from /proc/1/cmdline")
