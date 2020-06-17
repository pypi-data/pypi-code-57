import aiofiles
import glob


async def load_disks(hub):
    """
    Return list of disk devices and work out if they are SSD or HDD.
    """
    SSDs = []
    disks = []
    for entry in glob.glob("/sys/block/*/queue/rotational"):
        async with aiofiles.open(entry, "r") as entry_fp:
            device = entry.split("/")[3]
            flag = await entry_fp.read(1)
            if flag == "0":
                SSDs.append(device)
                hub.log.debug(f"Device {device} reports itself as an SSD")
            elif flag == "1":
                disks.append(device)
                hub.log.debug(f"Device {device} reports itself as an HDD")
            else:
                hub.log.error(
                    f"Unable to identify device {device} as an SSD or HDD. It does not report 0 or 1"
                )
    if SSDs:
        hub.grains.GRAINS.SSDs = sorted(SSDs)
    if disks:
        hub.grains.GRAINS.disks = sorted(disks)
