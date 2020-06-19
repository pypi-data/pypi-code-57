import shutil
import subprocess


async def load_disks(hub):
    namespace = r"\\root\microsoft\windows\storage"
    path = "MSFT_PhysicalDisk"
    get = "DeviceID,MediaType"

    disks = []
    ssds = []

    stdout = hub.exec.wmic.get(namespace, path, get)
    for line in stdout.strip().splitlines():
        info = line.split()
        if len(info) != 2 or not info[0].isdigit() or not info[1].isdigit():
            continue
        device = r"\\.\PhysicalDrive{0}".format(info[0])
        mediatype = info[1]
        if mediatype == "3":
            hub.log.debug(f"Device {device} reports itself as an HDD")
            disks.append(device)
        elif mediatype == "4":
            hub.log.debug(f"Device {device} reports itself as an SSD")
            ssds.append(device)
            disks.append(device)
        elif mediatype == "5":
            hub.log.debug(f"Device {device} reports itself as an SCM")
            disks.append(device)
        else:
            hub.log.debug(f"Device {device} reports itself as Unspecified")
            disks.append(device)

    if disks:
        hub.grains.GRAINS.disks = sorted(disks)
    if ssds:
        hub.grains.GRAINS.SSDs = sorted(ssds)


async def load_iqn(hub):
    """
    Return iSCSI IQN from a Windows host.
    """
    namespace = r"\\root\WMI"
    path = "MSiSCSIInitiator_MethodClass"
    get = "iSCSINodeName"

    iqns = []

    stdout = hub.exec.wmic.get(namespace, path, get)
    for line in stdout.split():
        if line.startswith("iqn."):
            line = line.rstrip()
            iqns.append(line.rstrip())

    if iqns:
        hub.grains.GRAINS.iscsi_iqn = iqns


async def load_fibre_channel(hub):
    """
    Return Fibre Channel port WWNs from a Windows host.
    """
    return  # TODO The powershell command needs to be fleshed out
    ps_cmd = (
        r"Get-WmiObject -ErrorAction Stop "
        r"-class MSFC_FibrePortHBAAttributes "
        r'-namespace "root\WMI" | '
        r"Select -Expandproperty Attributes | "
        r'%{($_.PortWWN | % {"{0:x2}" -f $_}) -join ""}'
    )
    ret = []
    cmd_ret = await hub.exec.cmd.powershell(ps_cmd)
    for line in cmd_ret:
        ret.append(line.rstrip())
    hub.grains.GRAINS.fc_wwn = ret
