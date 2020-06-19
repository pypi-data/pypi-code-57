import win32net
import win32netcon

status = {
    win32netcon.NetSetupUnknown: "Unknown",
    win32netcon.NetSetupUnjoined: "Unjoined",
    win32netcon.NetSetupWorkgroupName: "Workgroup",
    win32netcon.NetSetupDomainName: "Domain",
}


async def load_windows_domain(hub):
    """
    Gets information about the domain/workgroup. This will tell you if the
    system is joined to a domain or a workgroup
    """
    info = win32net.NetGetJoinInformation()

    hub.grains.GRAINS.windowsdomain = info[0]
    hub.grains.GRAINS.windowsdomaintype = status[info[1]]
