import wmi
from typing import Any


def __init__(hub):
    """The WMI constructor can either take a ready-made moniker or as many
    parts of one as are necessary. Eg::

      c = wmi.WMI (moniker="winmgmts:{impersonationLevel=Delegate}//remote")
      # or
      c = wmi.WMI (computer="remote", privileges=["!RemoteShutdown", "Security"])

    I daren't link to a Microsoft URL; they change so often. Try Googling for
    WMI construct moniker and see what it comes back with.

    For complete control, a named argument "wmi" can be supplied, which
    should be a SWbemServices object, which you create yourself. Eg::

      loc = win32com.client.Dispatch("WbemScripting.SWbemLocator")
      svc = loc.ConnectServer(...)
      c = wmi.WMI(wmi=svc)

    This is the only way of connecting to a remote computer with a different
    username, as the moniker syntax does not allow specification of a user
    name.
    """
    # TODO read WMI options from hub.OPTS
    """
    computer = "",
    impersonation_level = "",
    authentication_level = "",
    authority = "",
    privileges = "",
    moniker = "",
    namespace = "",
    suffix = "",
    user = "",
    password = "",
    find_classes = False,
    debug = False
    """
    hub.exec.wmi.WMI = wmi.WMI()


async def get(
    hub, class_: str, index: int = None, property_: str = "", *args, **kwargs
) -> Any:
    """
    Args:
        class_: The wmi object to fetch
        index: The index of the wmi object if multiple objects are available
        property_: The property within the wmi object to return
        *args: Args to pass to the WMI class as it is created
        **kwargs: KWargs to pass to the WMI class as it is created
    """
    info = getattr(hub.exec.wmi.WMI, class_)(*args, **kwargs)
    if index is not None:
        info = info[index]

    if property_:
        # Return the property on the object
        return getattr(info, property_)

    # Return the wmi object
    return info
