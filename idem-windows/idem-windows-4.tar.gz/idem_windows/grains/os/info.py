# Provides:
#    osversion
#    osmanufacturer
#    osfullname

import platform
import re


def _windows_os_release_grain(caption: str, product_type: int) -> str:
    """
    helper function for getting the osrelease grain
    :return:
    """
    # This creates the osrelease grain based on the Windows Operating
    # System Product Name. As long as Microsoft maintains a similar format
    # this should be future proof
    version = "Unknown"
    release = ""
    if "Server" in caption:
        for item in caption.split(" "):
            # If it's all digits, then it's version
            if re.match(r"\d+", item):
                version = item
            # If it starts with R and then numbers, it's the release ie: R2
            if re.match(r"^R\d+$", item):
                release = item
        os_release = "{0}Server{1}".format(version, release)
    else:
        for item in caption.split(" "):
            # If it's a number, decimal number, Thin or Vista, then it's the version
            if re.match(r"^(\d+(\.\d+)?)|Thin|Vista|XP$", item):
                version = item
        os_release = version

    # If the version is still Unknown, revert back to the old way of getting the os_release
    # https://github.com/saltstack/salt/issues/52339
    if os_release in ["Unknown"]:
        os_release = platform.release()
        server = {
            "Vista": "2008Server",
            "7": "2008ServerR2",
            "8": "2012Server",
            "8.1": "2012ServerR2",
            "10": "2016Server",
        }

        # Starting with Python 2.7.12 and 3.5.2 the `platform.uname()`
        # function started reporting the Desktop version instead of the
        # Server version on # Server versions of Windows, so we need to look
        # those up. So, if you find a Server Platform that's a key in the
        # server dictionary, then lookup the actual Server Release.
        # (Product Type 1 is Desktop, Everything else is Server)
        if product_type > 1 and os_release in server:
            os_release = server[os_release]

    return os_release


async def load_build(hub):
    major = int(
        hub.exec.reg.read_value(
            hive="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
            vname="CurrentBuildNumber",
        ).get("vdata")
    )
    minor = int(
        hub.exec.reg.read_value(
            hive="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
            vname="UBR",
        ).get("vdata")
    )

    hub.grains.GRAINS.osbuild = f"{major}.{minor}"


async def load_build_version(hub):
    hub.grains.GRAINS.osbuildversion = int(
        hub.exec.reg.read_value(
            hive="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
            vname="ReleaseId",
        ).get("vdata")
    )


async def load_codename(hub):
    hub.grains.GRAINS.oscodename = hub.exec.reg.read_value(
        hive="HKEY_LOCAL_MACHINE",
        key="SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
        vname="BuildBranch",
    ).get("vdata")


async def load_osinfo(hub):
    hub.grains.GRAINS.os = "Windows"
    # https://msdn.microsoft.com/en-us/library/aa394239(v=vs.85).aspx
    osinfo = await hub.exec.wmi.get("Win32_OperatingSystem", 0)

    hub.grains.GRAINS.osmanufacturer = await hub.grains.init.clean_value(
        "osmanufacturer", osinfo.Manufacturer
    )
    hub.grains.GRAINS.osfullname = await hub.grains.init.clean_value(
        "osfullname", osinfo.Caption
    )
    hub.grains.GRAINS.kernelrelease = await hub.grains.init.clean_value(
        "kernelrelease", osinfo.Version
    )

    hub.grains.GRAINS.osversion = await hub.grains.init.clean_value(
        "osversion", osinfo.Version
    )

    hub.grains.GRAINS.osrelease = _windows_os_release_grain(
        caption=osinfo.Caption, product_type=osinfo.ProductType
    )

    hub.grains.GRAINS.osfinger = f"{hub.grains.GRAINS.os}-{hub.grains.GRAINS.osrelease}"

    hub.grains.GRAINS.osrelease_info = (
        int(x) for x in hub.grains.GRAINS.osversion.split(".")
    )

    hub.grains.GRAINS.osservicepack = await hub.grains.init.clean_value(
        "osservicepack", osinfo.CSDVersion
    ) or platform.win32_ver()[2].replace("SP", "Service Pack ")

    hub.grains.GRAINS.osarch = await hub.grains.init.clean_value(
        "osarch", osinfo.OSArchitecture
    )


async def load_osmajorrelease(hub):
    hub.grains.GRAINS.osmajorrelease = int(
        hub.exec.reg.read_value(
            hive="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
            vname="CurrentMajorVersionNumber",
        ).get("vdata")
    )
