import re


async def load_motherboard(hub):
    # http://msdn.microsoft.com/en-us/library/windows/desktop/aa394072(v=vs.85).aspx
    try:
        motherboardinfo = await hub.exec.wmi.get("Win32_BaseBoard", 0)
        hub.grains.GRAINS.motherboard.productname = motherboardinfo.Product
        hub.grains.GRAINS.motherboard.serialnumber = motherboardinfo.SerialNumber
    except IndexError:
        hub.log.debug("Motherboard info not available on this system")


async def load_system_info(hub):
    # http://msdn.microsoft.com/en-us/library/windows/desktop/aa394102%28v=vs.85%29.aspx
    systeminfo = await hub.exec.wmi.get("Win32_ComputerSystem", 0)
    hub.grains.GRAINS.manufacturer = await hub.grains.init.clean_value(
        "manufacturer", systeminfo.Manufacturer
    )
    hub.grains.GRAINS.productname = await hub.grains.init.clean_value(
        "productname", systeminfo.Model
    )

    hub.grains.GRAINS.computer_name = await hub.grains.init.clean_value(
        "computer_name", systeminfo.Name
    )
