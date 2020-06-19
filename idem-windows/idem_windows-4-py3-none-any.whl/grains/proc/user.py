async def load_user(hub):
    hub.grains.GRAINS.username = hub.exec.user.current()
    # The relative ID is always the last number in the SID it is a unique identifier for a user or group.
    hub.grains.GRAINS.uid = int(
        hub.exec.user.sid_from_name(hub.grains.GRAINS.username).split("-")[-1]
    )

    groups = hub.exec.user.groups(hub.grains.GRAINS.username)
    admin = "Administrators"
    hub.grains.GRAINS.groupname = admin if admin in groups else groups.pop()
    hub.grains.GRAINS.gid = int(
        hub.exec.user.sid_from_name(hub.grains.GRAINS.groupname).split("-")[-1]
    )


async def load_console_user(hub):
    systeminfo = await hub.exec.wmi.get("Win32_ComputerSystem", 0)
    hub.grains.GRAINS.console_username = systeminfo.UserName
    hub.grains.GRAINS.console_user = int(
        hub.exec.user.sid_from_name(hub.grains.GRAINS.console_username).split("-")[-1]
    )
