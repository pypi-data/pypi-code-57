# Is there a __virtual__() function like in salt?
# because there are many linux ways of doing "service" even if
# systemd is the most prominent
# TODO verify that async contracts are working

import os
import re
import shlex
from typing import List, Text


# TODO once we figure out exceptions use this properly
CommandExecutionError = OSError
SaltInvocationError = CommandExecutionError

__func_alias__ = {
    "list_": "list",
}
__virtualname__ = "service"


def __virtual__(hub):
    "this module is kept here for historic purposes, it should not be used"
    return False
    if _booted():
        return True
    else:
        return (
            False,
            "The systemd execution module failed to load: only available on Linux "
            "systems which have been booted with systemd.",
        )


def __init__(hub):
    hub.exec.service.CHECK_FOR_UNIT_CHANGES = hub.pop.data.map()
    hub.exec.service.INITSCRIPT_PATH = "/etc/init.d"
    hub.exec.service.LOCAL_CONFIG_PATH = "/etc/systemd/system"
    hub.exec.service.VALID_UNIT_TYPES = (
        "automount",
        "device",
        "mount",
        "path",
        "service",
        "socket",
        "swap",
        "target",
        "timer",
    )
    hub.exec.service.SYSTEM_CONFIG_PATHS = (
        "/lib/systemd/system",
        "/usr/lib/systemd/system",
    )
    hub.exec.service.SYSTEMCTL_STATUS = hub.pop.data.map()
    hub.exec.service.SYSTEMD = hub.pop.data.map()


def _booted() -> bool:
    try:
        return bool(os.stat("/run/systemd/system"))
    except OSError:
        return False


def _canonical_unit_name(hub, name: Text) -> str:
    """
    Build a canonical unit name treating unit names without one
    of the valid suffixes as a service.
    """
    if any(name.endswith(suffix) for suffix in hub.exec.service.VALID_UNIT_TYPES):
        return name
    return f"{name}.service"


def _check_available(hub, name: str) -> bool:
    """
    Returns boolean telling whether or not the named service is available
    """
    _status = _systemctl_status(name)
    sd_version = salt.utils.systemd.version(__context__)
    if sd_version is not None and sd_version >= 231:
        # systemd 231 changed the output of "systemctl status" for unknown
        # services, and also made it return an exit status of 4. If we are on
        # a new enough version, check the retcode, otherwise fall back to
        # parsing the "systemctl status" output.
        # See: https://github.com/systemd/systemd/pull/3385
        # Also: https://github.com/systemd/systemd/commit/3dced37
        return 0 <= _status["retcode"] < 4

    out = _status["stdout"].lower()
    if "could not be found" in out:
        # Catch cases where the systemd version is < 231 but the return code
        # and output changes have been backported (e.g. RHEL 7.3).
        return False

    for line in salt.utils.itertools.split(out, "\n"):
        match = re.match(r"\s+loaded:\s+(\S+)", line)
        if match:
            ret = match.group(1) != "not-found"
            break
    else:
        raise CommandExecutionError("Failed to get information on unit '%s'" % name)
    return ret


async def _check_for_unit_changes(hub, name: str):
    """
    Check for modified/updated unit files, and run a daemon-reload if any are
    found.
    """
    if name not in hub.exec.service.CHECK_FOR_UNIT_CHANGES:
        if _untracked_custom_unit_found(hub, name) or await _unit_file_changed(
            hub, name
        ):
            systemctl_reload()
        # Set context key to avoid repeating this check
        hub.exec.service.CHECK_FOR_UNIT_CHANGES[name] = True


def _root(hub, path: str, root: str = None) -> str:
    """
    Relocate an absolute path to a new root directory.
    """
    if root:
        return os.path.join(root, os.path.relpath(path, os.path.sep))
    else:
        return path


async def _systemctl_cmd(
    hub,
    action,
    name: str = None,
    systemd_scope: bool = False,
    no_block: bool = False,
    root: str = None,
) -> List[str]:
    """
    Build a systemctl command line. Treat unit names without one
    of the valid suffixes as a service.
    """
    ret = []
    if (
        systemd_scope
        and await hub.exec.service.has_scope()
        and hub.OPT.exec.systmed_scope
        and __salt__["config.get"]("systemd.scope", True)
    ):
        ret.extend(["systemd-run", "--scope"])
    ret.append("systemctl")
    if no_block:
        ret.append("--no-block")
    if root:
        ret.extend(["--root", root])
    if isinstance(action, Text):
        action = shlex.split(action)
    ret.extend(action)
    if name is not None:
        ret.append(_canonical_unit_name(name))
    if "status" in ret:
        ret.extend(["-n", "0"])
    return ret


async def _systemctl_status(hub, name: str) -> str:
    """
    Helper function which leverages __context__ to keep from running 'systemctl
    status' more than once.
    """
    if name not in hub.exec.service.SYSTEMCTL_STATUS:
        hub.exec.service.SYSTEMCTL_STATUS[name] = await hub.exec.cmd.run(
            _systemctl_cmd("status", name), shell=False,
        )
    return hub.exec.service.SYSTEMCTL_STATUS[name]


async def _unit_file_changed(hub, name):
    """
    Returns True if systemctl reports that the unit file has changed, otherwise
    returns False.
    """
    status = await _systemctl_status(hub, name)["stdout"].lower()
    return "'systemctl daemon-reload'" in status


def _untracked_custom_unit_found(hub, name: str, root: str = None) -> bool:
    """
    If the passed service name is not available, but a unit file exist in
    /etc/systemd/system, return True. Otherwise, return False.
    """
    system = _root(hub, "/etc/systemd/system", root)
    unit_path = os.path.join(system, _canonical_unit_name(hub, name))
    return os.access(unit_path, os.R_OK) and not _check_available(hub, name)


async def available(hub, name: str) -> bool:
    """
    Check that the given service is available taking into account template
    units.
    """
    await _check_for_unit_changes(hub, name)
    return _check_available(hub, name)


def booted(hub) -> bool:
    """
    Return True if the system was booted with systemd, False otherwise.
    """
    if "booted" not in hub.exec.service.SYSTEMD:
        try:
            # This check does the same as sd_booted() from libsystemd-daemon:
            # http://www.freedesktop.org/software/systemd/man/sd_booted.html
            hub.exec.service.SYSTEMD.booted = _booted()
        except OSError:
            hub.exec.service.SYSTEMD.booted = False

    return hub.exec.service.SYSTEMD.booted


async def has_scope(hub) -> bool:
    """
    Scopes were introduced in systemd 205, this function returns a boolean
    which is true when the minion is systemd-booted and running systemd>=205.
    """
    if not hub.exec.service.booted():
        return False
    _sd_version = await hub.exec.service.version()
    if _sd_version is None:
        return False
    return _sd_version >= 205


async def version(hub) -> int:
    """
    Attempts to run systemctl --version. Returns None if unable to determine version.
    """
    if "version" not in hub.exec.service.SYSTEMD:
        ret = await hub.exec.cmd.run(["systemctl", "--version"])
        if ret.retcode:
            hub.log.error(
                f"`systemctl --version` encountered an error {ret.retcode}:\n{ret.stderr}"
            )

        match = re.search(r"^\w+\s+([0-9]+)", ret.stdout.splitlines()[0])
        if match:
            hub.exec.service.SYSTEMD.version = int(match.group(1))
        else:
            hub.log.error(
                f"Unable to determine systemd version from `systemctl --version`, output follows:\n{ret.stdout}"
            )
            hub.exec.service.SYSTEMD.version = None
    return hub.exec.service.SYSTEMD.version
