import io
import plistlib as plist
import shutil


async def load_disks(hub):
    """
    Return list of disk devices and work out if they are SSD or HDD.
    """
    diskutil = shutil.which("diskutil")
    if diskutil:
        plist_data = (
            await hub.exec.cmd.run([diskutil, "list", "-plist"])
        ).stdout.strip()
        disk_info = plist.load(io.BytesIO(plist_data.encode()))
        hub.grains.GRAINS.disks = disk_info["WholeDisks"]

        ssds = []
        for disk in hub.grains.GRAINS.disks:
            plist_data = (
                await hub.exec.cmd.run([diskutil, "info", "-plist", disk])
            ).stdout.strip()
            disk_info = plist.load(io.BytesIO(plist_data.encode()))
            if disk_info.get("SolidState", False):
                ssds.append(disk)

        if ssds:
            hub.grains.GRAINS.SSDs = ssds
