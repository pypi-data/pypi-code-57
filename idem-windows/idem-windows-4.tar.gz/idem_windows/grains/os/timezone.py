async def load_timezone(hub):
    # http://msdn.microsoft.com/en-us/library/windows/desktop/aa394498(v=vs.85).aspx
    timeinfo = await hub.exec.wmi.get("Win32_TimeZone", 0)
    hub.grains.GRAINS.timezone = await hub.grains.init.clean_value(
        "timezone", timeinfo.Description
    )
