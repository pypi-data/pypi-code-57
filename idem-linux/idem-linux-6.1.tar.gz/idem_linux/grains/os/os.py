import aiofiles
import distro

import os
import re


_REPLACE_LINUX_RE = re.compile(r"\W(?:gnu/)?linux", re.IGNORECASE)

_OS_NAME_MAP = {
    "redhatente": "RedHat",
    "gentoobase": "Gentoo",
    "archarm": "Arch ARM",
    "arch": "Arch",
    "debian": "Debian",
    "raspbian": "Raspbian",
    "fedoraremi": "Fedora",
    "chapeau": "Chapeau",
    "korora": "Korora",
    "amazonami": "Amazon",
    "alt": "ALT",
    "enterprise": "OEL",
    "oracleserv": "OEL",
    "cloudserve": "CloudLinux",
    "cloudlinux": "CloudLinux",
    "pidora": "Fedora",
    "scientific": "ScientificLinux",
    "synology": "Synology",
    "nilrt": "NILinuxRT",
    "poky": "Poky",
    "manjaro": "Manjaro",
    "manjarolin": "Manjaro",
    "univention": "Univention",
    "antergos": "Antergos",
    "sles": "SUSE",
    "void": "Void",
    "slesexpand": "RES",
    "linuxmint": "Mint",
    "neon": "KDE neon",
}

_OS_FAMILY_MAP = {
    "Ubuntu": "Debian",
    "Fedora": "RedHat",
    "Chapeau": "RedHat",
    "Korora": "RedHat",
    "FedBerry": "RedHat",
    "CentOS": "RedHat",
    "GoOSe": "RedHat",
    "Scientific": "RedHat",
    "Amazon": "RedHat",
    "CloudLinux": "RedHat",
    "OVS": "RedHat",
    "OEL": "RedHat",
    "XCP": "RedHat",
    "XCP-ng": "RedHat",
    "XenServer": "RedHat",
    "RES": "RedHat",
    "Sangoma": "RedHat",
    "Mandrake": "Mandriva",
    "ESXi": "VMware",
    "Mint": "Debian",
    "VMwareESX": "VMware",
    "Bluewhite64": "Bluewhite",
    "Slamd64": "Slackware",
    "SLES": "Suse",
    "SUSE Enterprise Server": "Suse",
    "SUSE  Enterprise Server": "Suse",
    "SLED": "Suse",
    "openSUSE": "Suse",
    "SUSE": "Suse",
    "openSUSE Leap": "Suse",
    "openSUSE Tumbleweed": "Suse",
    "SLES_SAP": "Suse",
    "Arch ARM": "Arch",
    "Manjaro": "Arch",
    "Antergos": "Arch",
    "ALT": "RedHat",
    "Trisquel": "Debian",
    "GCEL": "Debian",
    "Linaro": "Debian",
    "elementary OS": "Debian",
    "elementary": "Debian",
    "Univention": "Debian",
    "ScientificLinux": "RedHat",
    "Raspbian": "Debian",
    "Devuan": "Debian",
    "antiX": "Debian",
    "Kali": "Debian",
    "neon": "Debian",
    "Cumulus": "Debian",
    "Deepin": "Debian",
    "NILinuxRT": "NILinuxRT",
    "KDE neon": "Debian",
    "Void": "Void",
    "IDMS": "Debian",
    "Funtoo": "Gentoo",
    "TurnKey": "Debian",
}


async def _get_synology_osrelease(hub) -> str:
    # Get os from synology
    version = "/etc.defaults/VERSION"
    if os.path.isfile(version) and os.path.isfile("/etc.defaults/synoinfo.conf"):
        hub.log.debug("Parsing Synology distrib info from /etc/.defaults/VERSION")
        async with aiofiles.open(version, "r") as fp_:
            synoinfo = {}
            async for line in fp_:
                try:
                    key, val = line.rstrip("\n").split("=")
                except ValueError:
                    continue
                if key in ("majorversion", "minorversion", "buildnumber"):
                    synoinfo[key] = val.strip('"')
            if len(synoinfo) != 3:
                hub.log.warning(
                    "Unable to determine Synology version info. "
                    "Please report this, as it is likely a bug."
                )
            else:
                return f'{synoinfo["majorversion"]}.{synoinfo["minorversion"]}-{synoinfo["buildnumber"]}'


async def _get_os(osfullname: str) -> str:
    distroname = _REPLACE_LINUX_RE.sub("", osfullname).strip()

    # return the first ten characters with no spaces, lowercased
    shortname = distroname.replace(" ", "").lower()[:10]

    # this maps the long names from the /etc/DISTRO-release files to the
    # traditional short names that Salt has used.
    return _OS_NAME_MAP.get(shortname, distroname)


async def load_manufacturer(hub):
    # TODO There has got to be a way to programmatically determine this
    # For example, ubuntu is manufactuerd by Canonical, etc...
    hub.grains.GRAINS.osmanufacturer = "unknown"


async def load_linux_distribution(hub):
    release_info = lambda osrelease: tuple(
        int(x) if x.strip().isdigit() else x for x in osrelease.split(".")
    )

    info = distro.LinuxDistribution()
    hub.grains.GRAINS.osbuild = info.build_number()
    hub.grains.GRAINS.oscodename = info.codename().strip("\"'")

    hub.grains.GRAINS.osfullname = info.name().strip("\"'")
    hub.grains.GRAINS.osrelease = info.version().strip("\"'")

    if not (hub.grains.GRAINS.get("osfullname") or hub.grains.GRAINS.get("osrelease")):
        hub.grains.GRAINS.osrelease = await _get_synology_osrelease(hub)
        if hub.grains.GRAINS.get("osrelease"):
            hub.grains.GRAINS.osfullname = "Synology"
        else:
            hub.grains.GRAINS.osrelease = ""
            hub.grains.GRAINS.osfullname = ""

    hub.grains.GRAINS.os = await _get_os(hub.grains.GRAINS.osfullname)

    hub.grains.GRAINS.os_family = _OS_FAMILY_MAP.get(
        hub.grains.GRAINS.os, hub.grains.GRAINS.os
    )
    if hub.grains.GRAINS.os_family == "NILinuxRT":
        # This will likely have been defined elsewhere, dereference and redefine
        del hub.grains.GRAINS.ps
        hub.grains.GRAINS.ps = "ps -o user,pid,ppid,tty,time,comm"
    hub.grains.GRAINS.osrelease_info = release_info(hub.grains.GRAINS.osrelease)

    major_version = info.major_version().strip("\"'")
    hub.grains.GRAINS.osmajorrelease = (
        int(major_version) if major_version else hub.grains.GRAINS.osrelease_info[0]
    )

    # load osfinger
    os_name = hub.grains.GRAINS[
        "os" if hub.grains.GRAINS.os in ("Debian", "Raspbian") else "osfullname"
    ]
    finger = (
        hub.grains.GRAINS.osrelease
        if os_name in ("Ubuntu",)
        else hub.grains.GRAINS.osrelease_info[0]
    )
    if os_name and finger:
        hub.grains.GRAINS.osfinger = f"{os_name}-{finger}"
