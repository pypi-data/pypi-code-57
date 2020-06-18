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
import aiofiles
import errno

import os
import shutil


async def load_arm_linux(hub):
    fw_printenv = shutil.which("fw_printenv")
    if fw_printenv:
        # ARM Linux devices expose UBOOT env variables via fw_printenv
        hwdata = {
            "manufacturer": "manufacturer",
            "productname": "DeviceDesc",
            "serialnumber": "serial#",
        }
        for grain_name, cmd_key in hwdata.items():
            result = await hub.exec.cmd.run([fw_printenv, cmd_key])
            if result.retcode == 0:
                uboot_keyval = result.stdout.split("=")[1]
                hub.grains.GRAINS[grain_name] = await hub.grains.init.clean_value(
                    grain_name, uboot_keyval
                )


async def load_dmi(hub):
    name = "/sys/class/dmi/id"
    if os.path.exists(name):
        # On many Linux distributions basic firmware information is available via sysfs
        # requires CONFIG_DMIID to be enabled in the Linux kernel configuration
        sysfs_firmware_info = {
            "biosreleasedate": "bios_date",
            "biosversion": "bios_version",
            "manufacturer": "sys_vendor",
            "productname": "product_name",
            "serialnumber": "product_serial",
            "uuid": "product_uuid",
        }
        for key, fw_file in sysfs_firmware_info.items():
            contents_file = os.path.join("/sys/class/dmi/id", fw_file)
            if not hub.grains.GRAINS.get(key) and os.path.exists(contents_file):
                try:
                    async with aiofiles.open(contents_file, "r") as ifile:
                        hub.grains.GRAINS[key] = (await ifile.read()).strip()
                        if key == "uuid":
                            hub.grains.GRAINS.uuid = hub.grains.GRAINS.uuid.lower()
                except (IOError, OSError) as err:
                    # PermissionError is new to Python 3, but corresponds to the EACESS and
                    # EPERM error numbers. Use those instead here for PY2 compatibility.
                    if err.errno == errno.EACCES or err.errno == errno.EPERM:
                        # Skip the grain if non-root user has no access to the file.
                        pass


async def load_smbios(hub):
    smbios_info = {
        "biosreleasedate": "bios-release-date",
        "biosversion": "bios-version",
        "manufacturer": "system-manufacturer",
        "productname": "system-product-name",
        "serialnumber": "uuid",
        "uuid": "system-uuid",
    }
    if shutil.which("smbios"):
        for key, value in smbios_info.items():
            if not hub.grains.GRAINS.get(key):
                hub.grains.GRAINS[key] = await hub.exec.smbios.get(value)


async def load_serialnumber(hub):
    if shutil.which("smbios"):
        for serial in (
            "baseboard-serial-number",
            "chassis-serial-number",
            "system-serial-number",
        ):
            serial = await hub.exec.smbios.get(serial)
            if serial is not None:
                hub.grains.GRAINS.serialnumber = serial
                break
