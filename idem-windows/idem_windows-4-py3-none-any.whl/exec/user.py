# Get information about the current running process
# Ported partly from salt.utils.win_funcions.py
import pywintypes
import re
import win32api
import win32net
import win32security
from typing import Set


def is_admin(hub, name: str = None) -> bool:
    """
    Is the passed user a member of the Administrators group

    Args:
        name (str): The name to check

    Returns:
        bool: True if user is a member of the Administrators group, False
        otherwise
    """
    if name is None:
        name = hub.exec.user.current()
    groups = hub.exec.user.groups(name, True)

    for group in groups:
        if group in ("S-1-5-32-544", "S-1-5-18"):
            return True

    return False


def groups(hub, name: str = None, sid: bool = False) -> Set[str]:
    """
    Get the groups to which a user belongs

    Args:
        name (str): The user name to query
        sid (bool): True will return a list of SIDs, False will return a list of
        group names

    Returns:
        list: A list of group names or sids
    """
    if name is None:
        name = hub.exec.user.current()
    if name == "SYSTEM":
        # 'win32net.NetUserGetLocalGroups' will fail if you pass in 'SYSTEM'.
        groups = [name]
    else:
        groups_ = win32net.NetUserGetLocalGroups(None, name)

    if not sid:
        return set(groups_)

    return {hub.exec.user.sid_from_name(group) for group in groups_}


def sid_from_name(hub, name: str = None) -> str:
    """
    This is a tool for getting a sid from a name. The name can be any object.
    Usually a user or a group

    Args:
        name (str): The name of the user or group for which to get the sid

    Returns:
        str: The corresponding SID
    """
    # If None is passed, use the Universal Well-known SID "Null SID"
    if name is None:
        name = "NULL SID"

    try:
        sid = win32security.LookupAccountName(None, name)[0]
    except pywintypes.error as exc:
        raise OSError(f"User {name} not found: {exc}")
    return win32security.ConvertSidToStringSid(sid)


def current(with_domain: bool = True):
    """
    Gets the user executing the process

    Args:

        with_domain (bool):
            ``True`` will prepend the user name with the machine name or domain
            separated by a backslash

    Returns:
        str: The user name
    """
    user_name = win32api.GetUserNameEx(win32api.NameSamCompatible)
    if user_name[-1] == "$":
        # Make the system account easier to identify.
        # Fetch sid so as to handle other language than english
        test_user = win32api.GetUserName()
        if test_user == "SYSTEM":
            user_name = "SYSTEM"
        elif sid_from_name(test_user) == "S-1-5-18":
            user_name = "SYSTEM"
    elif not with_domain:
        user_name = win32api.GetUserName()

    return user_name


def sam_name(hub, username: str = None) -> str:
    r"""
    Gets the SAM name for a user. It basically prefixes a username without a
    backslash with the computer name. If the user does not exist, a SAM
    compatible name will be returned using the local hostname as the domain.

    i.e. salt.utils.same_name('Administrator') would return 'DOMAIN.COM\Administrator'

    .. note:: Long computer names are truncated to 15 characters
    """
    if username is None:
        username = hub.exec.user.current()
    sid_obj = win32security.LookupAccountName(None, username)[0]
    username, domain, _ = win32security.LookupAccountSid(None, sid_obj)
    return "\\".join([domain, username])


def guid_to_squid(guid: str) -> str:
    """
    Converts a GUID   to a compressed guid (SQUID)

    Each Guid has 5 parts separated by '-'. For the first three each one will be
    totally reversed, and for the remaining two each one will be reversed by
    every other character. Then the final compressed Guid will be constructed by
    concatenating all the reversed parts without '-'.

    .. Example::

        Input:                  2BE0FA87-5B36-43CF-95C8-C68D6673FB94
        Reversed:               78AF0EB2-63B5-FC34-598C-6CD86637BF49
        Final Compressed Guid:  78AF0EB263B5FC34598C6CD86637BF49

    Args:

        guid (str): A valid GUID

    Returns:
        str: A valid compressed GUID (SQUID)
    """
    guid_pattern = re.compile(
        r"^\{(\w{8})-(\w{4})-(\w{4})-(\w\w)(\w\w)-(\w\w)(\w\w)(\w\w)(\w\w)(\w\w)(\w\w)\}$"
    )
    guid_match = guid_pattern.match(guid)
    squid = ""
    if guid_match is not None:
        for index in range(1, 12):
            squid += guid_match.group(index)[::-1]
    return squid


def squid_to_guid(squid: str) -> str:
    """
    Converts a compressed GUID (SQUID) back into a GUID

    Args:

        squid (str): A valid compressed GUID

    Returns:
        str: A valid GUID
    """
    squid_pattern = re.compile(
        r"^(\w{8})(\w{4})(\w{4})(\w\w)(\w\w)(\w\w)(\w\w)(\w\w)(\w\w)(\w\w)(\w\w)$"
    )
    squid_match = squid_pattern.match(squid)
    guid = ""
    if squid_match is not None:
        guid = (
            "{"
            + squid_match.group(1)[::-1]
            + "-"
            + squid_match.group(2)[::-1]
            + "-"
            + squid_match.group(3)[::-1]
            + "-"
            + squid_match.group(4)[::-1]
            + squid_match.group(5)[::-1]
            + "-"
        )
        for index in range(6, 12):
            guid += squid_match.group(index)[::-1]
        guid += "}"
    return guid
