import shutil


async def load_iqn(hub):
    """
    Return iSCSI IQN from an AIX host.
    """
    iscsi_iqn = []
    lsattr = shutil.which("lsattr")

    if lsattr:
        ret = await hub.exec.cmd.run([lsattr, "-E", "-l", "iscsi0"])
        for line in ret.stdout.splitlines():
            line = line.strip()
            if "initiator_name" in line and line[0].isalpha():
                iqns = line.split()
                if len(iqns) > 1:
                    iscsi_iqn.append(iqns[1].rstrip())
    if iscsi_iqn:
        hub.grains.GRAINS.iscsi_iqn = iscsi_iqn
