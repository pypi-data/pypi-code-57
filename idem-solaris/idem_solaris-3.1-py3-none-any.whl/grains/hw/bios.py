import re
import shutil


async def load_bios_data(hub):
    # A simple value cleaner for regex matches
    clean = lambda x: x.strip().replace("'", "")

    # Run the commands that generate data for bios info
    prtconf = (
        await hub.exec.cmd.run([shutil.which("prtconf") or "/usr/sbin/prtconf", "-vp"])
    ).stdout
    prtdiag = (
        await hub.exec.cmd.run([shutil.which("prtdiag") or "/usr/sbin/prtdiag", "-v"])
    ).stdout
    virtinfo = (
        await hub.exec.cmd.run([shutil.which("virtinfo") or "/usr/sbin/virtinfo", "-a"])
    ).stdout

    # Load biosversion and biosreleasedate
    match = re.search(r"(?im)version:\s*\'OBP\s+(\S+)\s+(\S+)", prtconf) or re.search(
        r"(?im)System\s+PROM\s+revisions.*\n(?:Version\n)?-+\nOBP\s+(\S+)\s+(\S+)",
        prtdiag,
    )
    hub.grains.GRAINS.biosversion = (
        clean(match.group(1))
        if match
        else await hub.exec.smbios.get("bios-version") or "unknown"
    )
    hub.grains.GRAINS.biosreleasedate = (
        clean(match.group(2))
        if match
        else await hub.exec.smbios.get("bios-release-date") or "unknown"
    )

    # Load manufacturer
    match = re.search(r"(?im)^\s*System\s+Configuration:\s*(.*)(?=sun)", prtdiag)
    hub.grains.GRAINS.manufacturer = (
        clean(match.group(1))
        if match
        else await hub.exec.smbios.get("system-manufacturer") or "unknown"
    )

    # load productname
    match = re.search(
        r"(?im)^[^\S\r\n]*(?:banner|product)-name:[^\S\r\n]*(.*)", prtconf
    ) or re.search(
        r"(?im)^\s*System\s+Configuration:\s*.*?sun\d\S+[^\S\r\n]*(.*)", prtdiag
    )
    hub.grains.GRAINS.productname = (
        clean(match.group(1))
        if match
        else await hub.exec.smbios.get("system-product-name") or "unknown"
    )

    # Load serial number
    match = (
        re.search(r"(?i)chassis-sn:\s*(\S+)", prtconf)
        or re.search(r"(?im)Chassis\s+Serial\s+Number\n-+\n(\S+)", prtdiag)
        or re.search(r"(?i)Chassis\s+Serial#:\s*(\S+)", virtinfo)
    )
    hub.grains.GRAINS.serialnumber = (
        clean(match.group(1))
        if match
        else (
            await hub.exec.smbios.get("baseboard-serial-number")
            or await hub.exec.smbios.get("chassis-serial-number")
            or await hub.exec.smbios.get("system-serial-number")
        )
        or "unkown"
    )

    # Load system firmware
    match = re.search(r"(?i)Sun\s+System\s+Firmware\s+(\S+)\s+(\S+)", prtdiag)
    if match:
        hub.grains.GRAINS.systemfirmware = match.group(1)
        hub.grains.GRAINS.systemfirmwaredate = match.group(2)

    # Load uuid
    match = re.search(r"(?i)Domain\s+UUID:\s+(\S+)", virtinfo)
    hub.grains.GRAINS.uuid = (
        clean(match.group(1))
        if match
        else await hub.exec.smbios.get("system-uuid") or "unknown"
    )
