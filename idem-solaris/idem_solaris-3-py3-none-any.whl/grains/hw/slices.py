import shutil


async def load_disks(hub):
    # partitions are called "slices" on SunOS, find out about the underlying hardware
    disks = []
    ssds = []

    iostat = shutil.which("iostat") or "/usr/bin/iostat"
    ret = await hub.exec.cmd.run([iostat, "-x"])
    # extended device statistics
    # device    r/s    w/s   kr/s   kw/s wait actv wsvc_t asvc_t  %w  %b
    # cmdk0     1.5   21.7   68.5  214.2  0.0  0.0    0.4    0.3   0   0

    # Skip the first two lines
    for line in ret.stdout.splitlines()[2:]:
        disks.append(line.split()[0])

    if disks:
        hub.grains.GRAINS.disks = sorted(disks)

    # TODO how to distinguish between SSDs and HDDs?
    if ssds:
        hub.grains.GRAINS.SSDs = sorted(ssds)
