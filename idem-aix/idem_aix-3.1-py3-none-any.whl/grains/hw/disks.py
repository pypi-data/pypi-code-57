import shutil


async def load_disks(hub):
    """
    Return list of disk devices and work out if they are SSD or HDD.
    """
    SSDs = []
    disks = []

    lsdev = shutil.which("lsdev")
    if lsdev:
        ret = await hub.exec.cmd.run([lsdev, "-c", "disk"])
        for line in ret.stdout.strip().splitlines():
            name, available, disk_type = line.split(maxsplit=2)
            if available == "Available":
                disks.append(name)

    if SSDs:
        # TODO detect which disks are SSDs
        hub.grains.GRAINS.SSDs = sorted(SSDs)
    if disks:
        hub.grains.GRAINS.disks = sorted(disks)
