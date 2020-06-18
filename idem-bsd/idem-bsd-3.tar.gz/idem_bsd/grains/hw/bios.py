"""
Get system specific hardware data from dmidecode

Provides
    biosversion
    productname
    manufacturer
    serialnumber
    biosreleasedate
    uuid

.. versionadded:: 0.9.5
"""
import shutil
from typing import Dict


async def _load_kenv(hub) -> Dict[str, str]:
    # For FreeBSD
    kenv = shutil.which("kenv")
    if kenv:
        return {
            "biosversion": (
                await hub.exec.cmd.run([kenv, "smbios.bios.version"])
            ).stdout.strip(),
            "manufacturer": (
                await hub.exec.cmd.run([kenv, "smbios.system.maker"])
            ).stdout.strip(),
            "serialnumber": (
                await hub.exec.cmd.run([kenv, "smbios.system.serial"])
            ).stdout.strip(),
            "productname": (
                await hub.exec.cmd.run([kenv, "smbios.system.product"])
            ).stdout.strip(),
            "biosreleasedate": (
                await hub.exec.cmd.run([kenv, "smbios.bios.reldate"])
            ).stdout.strip(),
            "uuid": (
                await hub.exec.cmd.run([kenv, "smbios.system.uuid"])
            ).stdout.strip(),
        }


async def _load_sysctl(hub) -> Dict[str, str]:
    # For OpenBSD and NetBSD
    sysctl = shutil.which("sysctl")
    if sysctl:
        return {
            "biosversion": (
                await hub.exec.cmd.run([sysctl, "hw.version"])
            ).stdout.strip()
            or (
                await hub.exec.cmd.run([sysctl, "machdep.dmi.board-version"])
            ).stdout.strip(),
            "manufacturer": (
                await hub.exec.cmd.run([sysctl, "hw.vendor"])
            ).stdout.strip()
            or (
                await hub.exec.cmd.run([sysctl, "machdep.dmi.system-vendor"])
            ).stdout.strip(),
            "serialnumber": (
                await hub.exec.cmd.run([sysctl, "hw.serialno"])
            ).stdout.strip()
            or (
                await hub.exec.cmd.run([sysctl, "machdep.dmi.system-serial"])
            ).stdout.strip(),
            "productname": (
                await hub.exec.cmd.run([sysctl, "hw.product"])
            ).stdout.strip()
            or (
                await hub.exec.cmd.run([sysctl, "machdep.dmi.system-product"])
            ).stdout.strip(),
            "biosreleasedate": (
                await hub.exec.cmd.run([sysctl, "machdep.dmi.bios-date"])
            ).stdout.strip(),
            "uuid": (await hub.exec.cmd.run([sysctl, "hw.uuid"])).stdout.strip()
            or (
                await hub.exec.cmd.run([sysctl, "machdem.dmi.system-uuid"])
            ).stdout.strip(),
        }


async def load_bios_data(hub):
    data = await _load_kenv(hub) or await _load_sysctl(hub) or ("unknown" * 6)

    for key, val in data.items():
        hub.grains.GRAINS[key] = await hub.grains.init.clean_value(key, val)
