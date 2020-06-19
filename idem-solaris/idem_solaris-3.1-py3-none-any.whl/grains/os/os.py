import aiofiles

import os
import re
import shutil
from typing import Tuple


_OS_FAMILY_MAP = {
    "Solaris": "Solaris",
    "SmartOS": "Solaris",
    "OmniOS": "Solaris",
    "OpenIndiana Development": "Solaris",
    "OpenIndiana": "Solaris",
    "OpenSolaris Development": "Solaris",
    "OpenSolaris": "Solaris",
    "Oracle Solaris": "Solaris",
}


async def load_osbuild(hub):
    hub.grains.GRAINS.osbuild = "unknown"

    pkg = shutil.which("pkg") or "/usr/bin/pkg"
    if os.path.exists(pkg):
        ret = await hub.exec.cmd.run([pkg, "info", "kernel"])
        hub.grains.GRAINS.osbuild = ret.stdout.strip().split("FMRI")[-1].split(":")[-1]


def _load_oscodename(hub, osname: str, osrelease: float) -> str:
    if ("sunos" in osname and osrelease <= 4.1) or (
        "solaris" in osname and osrelease <= 1.1
    ):
        return "Valkyrie"
    elif ("sunos" in osname and osrelease <= 5) or (
        "solaris" in osname and osrelease <= 2
    ):
        return "Jupiter"
    elif "solaris" in osname:
        if osrelease < 2.5:
            return "Starburst"
        elif osrelease <= 2.6:
            return "Wave3"
        elif osrelease == 7:
            return "StoreEdge N8200"
        elif "64" in hub.grains.GRAINS.get("osarch", ""):
            # For the full x86_64 version of Solaris
            return "Wyoming"
        else:
            # For the current release of Solaris
            return "Nevada"
    else:
        return "unknown"
    # Chrysalis Client if Solaris intel-based NC


async def load_manufacturer(hub):
    hub.grains.GRAINS.osmanufacturer = "unknown"
    prtconf = shutil.which("prtconf") or "/usr/sbin/prtconf"
    if os.path.exists(prtconf):
        ret = await hub.exec.cmd.run(prtconf)
        for line in ret.stdout.splitlines():
            if "System Configuration" in line:
                # remove the system configuration line and os arch
                hub.grains.GRAINS.osmanufacturer = " ".join(line.split()[2:-1])
                break


async def _load_release(hub) -> Tuple[str]:
    release_file = "/etc/release"
    if os.path.isfile(release_file):
        async with aiofiles.open(release_file, "r") as fp_:
            rel_data = await fp_.read()
            try:
                release_re = re.compile(
                    r"((?:(?:Open|Oracle )?Solaris|OpenIndiana|OmniOS)\s*(?:Development)?)"
                    r"\s*(\d+\.?\d*|v\d+)\s?[A-Z]*\s?(r\d+|\d+\/\d+|oi_\S+|snv_\S+)?"
                )
                return release_re.search(rel_data).groups()
            except AttributeError:
                pass


async def load_osinfo(hub):
    hub.grains.init.wait_for("kernelversion")

    # Collect some preliminary information
    (osname, osmajorrelease, osminorrelease) = await _load_release(hub) or [
        "Solaris",
        "0",
        "0",
    ]

    # Load os
    hub.grains.GRAINS.os = "SmartOS" if hub.grains.GRAINS.smartos else osname.strip()
    hub.grains.GRAINS.os_family = _OS_FAMILY_MAP.get(
        hub.grains.GRAINS.os, hub.grains.GRAINS.os
    )

    # Sanitize the osrelease information
    if hub.grains.GRAINS.smartos:
        # See https://github.com/joyent/smartos-live/issues/224
        osrelease_stamp = hub.grains.GRAINS.kernelversion[
            hub.grains.GRAINS.kernelversion.index("_") + 1 :
        ]
        hub.grains.GRAINS.osrelease = ".".join(
            (x or "0")
            for x in (
                osrelease_stamp.split("T")[0][0:4],
                osrelease_stamp.split("T")[0][4:6],
                osrelease_stamp.split("T")[0][6:8],
            )
        )
    elif (
        hub.grains.GRAINS.os == "Oracle Solaris"
        and hub.grains.GRAINS.kernelversion.startswith(osmajorrelease)
    ):
        # Oracla Solars 11 and up have minor version in kernelversion
        hub.grains.GRAINS.osrelease = hub.grains.GRAINS.kernelversion[
            : hub.grains.GRAINS.kernelversion.find(".", 5)
        ]
    elif hub.grains.GRAINS.os == "OmniOS":
        hub.grains.GRAINS.osrelease = (
            f"{osmajorrelease[1:] or 0}.{osminorrelease[1:] or 0}"
        )
    else:
        hub.grains.GRAINS.osrelease = ""

    # Load release info
    hub.grains.GRAINS.osrelease_info = [
        int(x) if x.isdigit() else x or 0
        for x in hub.grains.GRAINS.osrelease.split(".")
    ]
    assert len(hub.grains.GRAINS.osrelease_info)
    hub.grains.GRAINS.osmajorrelease = int(hub.grains.GRAINS.osrelease_info[0])
    hub.grains.GRAINS.osrelease = ".".join(
        str(x or 0) for x in hub.grains.GRAINS.osrelease_info
    )

    # Load other name info
    if len(hub.grains.GRAINS.osrelease_info) > 1:
        hub.grains.GRAINS.oscodename = _load_oscodename(
            hub,
            osname=hub.grains.GRAINS.os.lower(),
            osrelease=hub.grains.GRAINS.osrelease_info[0]
            + (hub.grains.GRAINS.osrelease_info[1] / 10),
        )
    else:
        hub.grains.GRAINS.oscodename = "unknown"

    if hub.grains.GRAINS.osmajorrelease:
        hub.grains.GRAINS.osfinger = (
            f"{hub.grains.GRAINS.os}-{hub.grains.GRAINS.osmajorrelease}"
        )
        # In salt, osfullname was a duplicate of what osfinger should have been and osfinger didn't exist
        # It's set straight now
        hub.grains.GRAINS.osfullname = (
            f"{hub.grains.GRAINS.os}-{hub.grains.GRAINS.osrelease}"
        )
    else:
        hub.grains.GRAINS.osfullname = hub.grains.GRAINS.osfinger = hub.grains.GRAINS.os
