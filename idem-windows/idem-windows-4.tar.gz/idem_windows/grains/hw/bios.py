import datetime


async def load_bios_info(hub):
    biosinfo = await hub.exec.wmi.get("Win32_BIOS", 0)

    # bios name had a bunch of whitespace appended to it in my testing
    # 'PhoenixBIOS 4.0 Release 6.0     '
    hub.grains.GRAINS.biosversion = await hub.grains.init.clean_value(
        "biosversion", biosinfo.Name.strip()
    )

    date = datetime.datetime.strptime(
        biosinfo.ReleaseDate.split(".")[0], "%Y%m%d%H%M%S"
    )
    hub.grains.GRAINS.biosreleasedate = f"{date.month}/{date.day}/{date.year}"
    hub.grains.GRAINS.serialnumber = await hub.grains.init.clean_value(
        "serialnumber", biosinfo.SerialNumber
    )
