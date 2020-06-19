import abc
import aiofiles
import asyncio
import collections.abc as abc
import glob

import os
import plistlib
import re
import types
import xml.parsers.expat
from typing import Any, Dict, List, Text, Tuple


__virtualname__ = "service"
__func_alias__ = {
    "list_": "list",
}

# TODO once we figure out exceptions use this properly
CommandExecutionError = OSError
SaltInvocationError = CommandExecutionError


def __virtual__(hub):
    # This plugin should not be used, it's broken, kept here for legacy purposes
    return False


def __init__(hub):
    # TODO should this be a config option from hub.opt?
    hub.exec.service.USING_CACHED_SERVICES = True
    hub.exec.service.CACHED_SERVICES = {}

    hub.exec.service.LAUNCHD_PATHS = {
        "/Library/LaunchAgents",
        "/Library/LaunchDaemons",
        "/System/Library/LaunchAgents",
        "/System/Library/LaunchDaemons",
    }
    hub.exec.service.LAUNCHD_PATHS.update(glob.glob("/Users/*/Library/LaunchAgents"))


async def _always_running_service(hub, name: str) -> bool:
    """
    Check if the service should always be running based on the KeepAlive Key
    in the service plist.

    :param str name: Service label, file name, or full path

    :return: True if the KeepAlive key is set to True, False if set to False or
        not set in the plist at all.
    """

    # get all the info from the launchctl service
    service_info = await hub.exec.service.show(name)

    # get the value for the KeepAlive key in service plist
    try:
        keep_alive = service_info.plist.KeepAlive
    except KeyError:
        return False

    # check if KeepAlive is True and not just set.

    if isinstance(keep_alive, abc.MutableMapping):
        # check for pathstate
        for _file, value in keep_alive.get("PathState", {}).items():
            if value is True and os.path.exists(_file):
                return True
            elif value is False and not os.path.exists(_file):
                return True

    if keep_alive is True:
        return True

    return False


def _check_launchctl_stderr(ret: Dict[str, Any]) -> bool:
    """
    helper class to check the launchctl stderr.
    launchctl does not always return bad exit code
    if there is a failure
    """
    err = ret["stderr"].lower()
    if "service is disabled" in err:
        return True
    return False


async def _get_domain_target(
    hub, name: str, service_target: bool = False
) -> Tuple[str, str]:
    """
    Returns the domain/service target and path for a service. This is used to
    determine whether or not a service should be loaded in a user space or
    system space.

    :param str name: Service label, file name, or full path

    :param bool service_target: Whether to return a full
    service target. This is needed for the enable and disable
    subcommands of /bin/launchctl. Defaults to False

    :return: Tuple of the domain/service target and the path to the service.
    """

    # Get service information
    service = await _get_service(hub, name)

    # get the path to the service
    path = service.file_path

    # most of the time we'll be at the system level.
    domain_target = "system"

    # check if a LaunchAgent as we should treat these differently.
    if "LaunchAgents" in path:
        # Get the console user so we can service in the correct session
        uid = hub.grains.GRAINS.console_user
        domain_target = f"gui/{uid}"

    # check to see if we need to make it a full service target.
    if service_target:
        domain_target = f"{domain_target}/{service.plist.Label}"

    return domain_target, path


async def _get_service(hub, name: str) -> Tuple[str]:
    """
    Get information about a service.  If the service is not found, raise an
    error

    :param str name: Service label, file name, or full path
    :return: The service information for the service, otherwise an Error
    """
    services = await hub.exec.service.available_services()
    name = name.lower()

    service = _name_in_services(hub, name, services)

    # if we would the service we can return it
    if service:
        return hub.pop.data.imap(service)

    # if we got here our service is not available, now we can check to see if
    # we received a cached batch of services, if not we did a fresh check
    # so we need to raise that the service could not be found.
    if not hub.exec.service.USING_CACHED_SERVICES:
        raise CommandExecutionError(f"Service not found: {name}")

    # we used a cached version to check, a service could have been made
    # between now and then, we should refresh our available services.
    services = await hub.exec.service.available_services(refresh=True)

    # check to see if we found the service we are looking for.
    service = _name_in_services(hub, name, services)

    if not service:
        # Could not find the service after refresh raise.
        raise CommandExecutionError("Service not found: {0}".format(name))

    # found it :)
    return hub.pop.data.imap(service)


async def _launch_agent(hub, name: str) -> bool:
    """
    Checks to see if the provided service is a LaunchAgent

    :param str name: Service label, file name, or full path

    :return: True if a LaunchAgent, False if not.
    """
    # Get the path to the service.
    service = await _get_service(hub, name)
    return "LaunchAgents" in service.file_path


def _name_in_services(hub, name: str, services: Dict[str, Dict]) -> Dict[str, Any]:
    """
    Checks to see if the given service is in the given services.

    :param str name: Service label, file name, or full path

    :param dict services: The currently available services.

    :return: The service information for the service, otherwise
    an empty dictionary
    """
    if name in services:
        # Match on label
        return hub.pop.data.imap(services[name])

    for service in services.values():
        if service["file_path"].lower() == name:
            # Match on full path
            return hub.pop.data.imap(service)
        basename, ext = os.path.splitext(service["file_name"])
        if basename.lower() == name:
            # Match on basename
            return hub.pop.data.imap(service)

    return hub.pop.data.imap({})


async def available(hub, name: str) -> bool:
    """
    Check that the given service is available.

    :param str name: The name of the service

    :return: True if the service is available, otherwise False
    """
    try:
        await _get_service(hub, name)
        return True
    except CommandExecutionError:
        return False


async def available_services(hub, refresh: bool = False) -> Dict[str, Any]:
    """
    This is a helper function for getting the available macOS services.

    The strategy is to look through the known system locations for
    launchd plist files, parse them, and use their information for
    populating the list of services. Services can run without a plist
    file present, but normally services which have an automated startup
    will have a plist file, so this is a minor compromise.
    """
    if hub.exec.service.CACHED_SERVICES and not refresh:
        hub.log.debug("Found context for available services.")
        return hub.pop.data.imap(hub.exec.service.CACHED_SERVICES)

    result = {}
    for launch_dir in hub.exec.service.LAUNCHD_PATHS:
        for root, dirs, files in os.walk(launch_dir):
            print("-" * 100)
            print(root)
            for file_name in files:
                if "com.apple.apsd" in file_name:
                    print("asdf" * 100)
                    print("asdf" * 100)
                    print("asdf" * 100)
                    print(root)
                    print(file_name)
                data = await hub.exec.service.read_plist_file(root, file_name)
                if data:
                    result[data.plist.Label.lower()] = data

    hub.exec.service.CACHED_SERVICES = result
    return hub.pop.data.imap(hub.exec.service.CACHED_SERVICES)


async def confirm_updated(
    hub,
    value: str,
    check_fun: types.FunctionType,
    normalize_ret: bool = False,
    wait: int = 5,
) -> bool:
    """
    Wait up to ``wait`` seconds for a system parameter to be changed before
    deciding it hasn't changed.

    :param str value: The value indicating a successful change

    :param function check_fun: The function whose return is compared with
        ``value``

    :param bool normalize_ret: Whether to normalize the return from
        ``check_fun`` with ``validate_enabled``

    :param int wait: The maximum amount of seconds to wait for a system
        parameter to change
    """
    for i in range(wait):
        state = (
            hub.exec.service.validate_enabled(check_fun())
            if normalize_ret
            else check_fun()
        )
        hub.log.debug(
            f"confirm update try: {i} func:{check_fun} state:{state} value:{value}"
        )
        if value in state:
            return True
        await asyncio.sleep(1)
    return False


async def disable(hub, name: str, runas: str = None) -> bool:
    """
    Disable a launchd service. Raises an error if the service fails to be
    disabled

    :param str name: Service label, file name, or full path

    :param str runas: User to run launchctl commands

    :return: ``True`` if successful or if the service is already disabled
    """
    # Get the service target. enable requires a full <service-target>
    service_target = await _get_domain_target(name, service_target=True)[0]

    # disable the service: will raise an error if it fails
    return await hub.exec.service.launchctl("disable", service_target, runas=runas)


async def disabled(hub, name: str, runas: str = None, domain: str = "system") -> bool:
    """
    Check if the specified service is not enabled. This is the opposite of
    ``service.enabled``

    :param str name: The name to look up

    :param str runas: User to run launchctl commands

    :param str domain: domain to check for disabled services. Default is system.

    :return: True if the specified service is NOT enabled, otherwise False
    """

    disabled = await hub.exec.service.launchctl(
        "print-disabled", domain, return_stdout=True, runas=runas
    )
    for service in disabled.split("\n"):
        if name in service:
            srv_name = service.split("=>")[0].split('"')[1]
            status = service.split("=>")[1]
            if name != srv_name:
                pass
            else:
                return True if "true" in status.lower() else False

    return False


async def enable(hub, name: str, runas: str = None) -> bool:
    """
    Enable a launchd service. Raises an error if the service fails to be enabled

    :param str name: Service label, file name, or full path

    :param str runas: User to run launchctl commands

    :return: ``True`` if successful or if the service is already enabled
    """
    # Get the domain target. enable requires a full <service-target>
    service_target = await _get_domain_target(hub, name, service_target=True)[0]

    # Enable the service: will raise an error if it fails
    return await hub.exec.service.launchctl("enable", service_target, runas=runas)


async def enabled(hub, name: str, runas: str = None) -> bool:
    """
    Check if the specified service is enabled

    :param str name: The name of the service to look up

    :param str runas: User to run launchctl commands

    :return: True if the specified service enabled, otherwise False
    """
    # Try to list the service.  If it can't be listed, it's not enabled
    try:
        await hub.exec.service.list(name=name, runas=runas)
        return True
    except CommandExecutionError:
        return False


async def get_all(hub, runas: str = None) -> List[str]:
    """
    Return a list of services that are enabled or available. Can be used to
    find the name of a service.

    :param str runas: User to run launchctl commands

    :return: A list of all the services available or enabled
    """
    # Get list of enabled services
    result = set(await hub.exec.services.get_enabled(runas=runas))

    # Get list of all services
    result.update((await hub.exec.services.available_services()).keys())

    # Return composite list
    return sorted(result)


async def get_enabled(hub, runas: str = None) -> List[str]:
    """
    Return a list of all services that are enabled. Can be used to find the
    name of a service.

    :param str runas: User to run launchctl commands

    :return: A list of all the services enabled on the system
    """
    # Collect list of enabled services
    stdout = await hub.exec.service.list(runas=runas)
    service_lines = [line for line in stdout.splitlines()]

    # Construct list of enabled services
    return sorted(
        {
            # Skip the header line that starts with "PID"
            # Second value in the split is the label
            line.split("\t")[2]
            for line in service_lines
            if not line.startswith("PID")
        }
    )


async def list_(hub, name: str = None, runas: str = None) -> str:
    """
    Run launchctl list and return the output
    :param str name: The name of the service to list

    :param str runas: User to run launchctl commands

    :return: If a name is passed returns information about the named service,
        otherwise returns a list of all services and pids
    """
    if name:
        # Get service information and label
        service = await _get_service(hub, name)
        label = service.plist.Label

        # we can assume if we are trying to list a LaunchAgent we need
        # to run as a user, if not provided, we'll use the console user.
        if not runas and await _launch_agent(hub, name):
            runas = hub.grains.GRAINS.console_username

        # Collect information on service: will raise an error if it fails
        return await hub.exec.service.launchctl(
            "list", label, return_stdout=True, runas=runas
        )

    # Collect information on all services: will raise an error if it fails
    return await hub.exec.service.launchctl("list", return_stdout=True, runas=runas)


async def launchctl(hub, sub_cmd: str, *args, **kwargs) -> str:
    """
    Run a launchctl command and raise an error if it fails

    Args: additional args are passed to launchctl
        sub_cmd (str): Sub command supplied to launchctl

    Kwargs: passed to ``hub.exec.cmd.run``
        return_stdout (bool): A keyword argument. If true return the stdout of
            the launchctl command

    Returns:
        str: The stdout of the launchctl command if requested
             The return will be empty if successful

    Raises:
        CommandExecutionError: If command fails
    """
    # Get return type
    return_stdout = kwargs.pop("return_stdout", False)

    # Construct command
    cmd = ["launchctl", sub_cmd]
    cmd.extend(args)

    # Run command
    kwargs["shell"] = False
    ret = await hub.exec.cmd.run(cmd, **kwargs)
    error = _check_launchctl_stderr(ret)

    # Raise an error or return successful result
    if ret.retcode or error:
        out = f"Failed to {sub_cmd} service:\n"
        out += f"stdout: {ret.stdout}\n"
        out += f"stderr: {ret.stderr}\n"
        out += f"retcode: {ret.retcode}"
        raise CommandExecutionError(out)
    else:
        return ret.stdout


async def missing(hub, name: str) -> bool:
    """
    The inverse of service.available
    Check that the given service is not available.

    :param str name: The name of the service

    :return: True if the service is not available, otherwise False
    """
    return not await hub.exec.service.available(name)


async def read_plist_file(hub, root: str, file_name: str) -> Dict[str, Any]:
    """
    :param root: The root path of the plist file
    :param file_name: The name of the plist file
    :return:  An empty dictionary if the plist file was invalid, otherwise, a dictionary with plist data
    """
    file_path = os.path.join(root, file_name)
    hub.log.debug("read_plist: Gathering service info for {}".format(file_path))

    # Must be a plist file
    if not file_path.lower().endswith(".plist"):
        hub.log.debug("read_plist: Not a plist file: {}".format(file_path))
        return hub.pop.data.imap({})

    # ignore broken symlinks
    if not os.path.exists(os.path.realpath(file_path)):
        hub.log.warning("read_plist: Ignoring broken symlink: {}".format(file_path))
        return hub.pop.data.imap({})

    async with aiofiles.open(file_path, "rb") as fh:
        try:
            plist = plistlib.loads(await fh.read())
        except plistlib.InvalidFileException:
            return hub.pop.data.imap({})

    if "Label" not in plist:
        # not all launchd plists contain a Label key
        hub.log.debug(
            "read_plist: Service does not contain a Label key. Skipping {}.".format(
                file_path
            )
        )
        return hub.pop.data.imap({})

    return hub.pop.data.imap(
        {"file_name": file_name, "file_path": file_path, "plist": plist,}
    )


async def restart(hub, name: str, runas: str = None) -> bool:
    """
    Unloads and reloads a launchd service.  Raises an error if the service
    fails to reload

    :param str name: Service label, file name, or full path

    :param str runas: User to run launchctl commands

    :return: ``True`` if successful
    """
    # Restart the service: will raise an error if it fails
    ret = True
    if await hub.exec.serive.enabled(name, runas=runas):
        ret = ret and await hub.exec.service.stop(name, runas=runas)
    ret = ret and await hub.exec.service.start(name, runas=runas)

    return ret


async def show(hub, name: str):
    """
    Show properties of a launchctl service

    :param str name: Service label, file name, or full path

    :return: The service information if the service is found
    :rtype: dict

    CLI Example:

    .. code-block:: bash

        salt '*' service.show org.cups.cupsd  # service label
        salt '*' service.show org.cups.cupsd.plist  # file name
        salt '*' service.show /System/Library/LaunchDaemons/org.cups.cupsd.plist  # full path
    """
    return await _get_service(hub, name)


async def start(hub, name: str, runas: str = None) -> bool:
    """
    Start a launchd service.  Raises an error if the service fails to start

    .. note::
        To start a service in macOS the service must be enabled first. Use
        ``service.enable`` to enable the service.

    :param str name: Service label, file name, or full path

    :param str runas: User to run launchctl commands

    :return: ``True`` if successful or if the service is already running
    """
    # Get the domain target.
    domain_target, path = await _get_domain_target(name)

    # Load (bootstrap) the service: will raise an error if it fails
    return await hub.exec.service.launchctl(
        "bootstrap", domain_target, path, runas=runas
    )


async def status(hub, name: str, sig: str = None, runas: str = None) -> str:
    """
    Return the status for a service.

    :param str name: Used to find the service from launchctl.  Can be any part
        of the service name or a regex expression.

    :param str sig: Find the service with status.pid instead.  Note that
        ``name`` must still be provided.

    :param str runas: User to run launchctl commands

    :return: The PID for the service if it is running, or 'loaded' if the
        service should not always have a PID, or otherwise an empty string
    """
    # Find service with ps
    if sig:
        return "\n".join(await hub.exec.status.pid(sig))

    try:
        await _get_service(hub, name)
    except CommandExecutionError as msg:
        hub.log.error(msg)
        return ""

    if not runas and await _launch_agent(hub, name):
        runas = hub.grains.GRAINS.console_username

    output = await hub.exec.service.list(runas=runas)

    pids = []
    for line in output.splitlines():
        if "PID" in line:
            continue
        if re.search(name, line.split()[-1]):
            if line.split()[0].isdigit():
                pids.append(line.split()[0])

    # mac services are a little different than other platforms as they may be
    # set to run on intervals and may not always active with a PID. This will
    # return a string 'loaded' if it shouldn't always be running and is enabled.
    if (
        not await _always_running_service(hub, name)
        and await hub.exec.service.enabled(name)
        and not pids
    ):
        return "loaded"

    return "\n".join(pids)


async def stop(hub, name: str, runas: str = None) -> bool:
    """
    Stop a launchd service.  Raises an error if the service fails to stop

    .. note::
        Though ``service.stop`` will unload a service in macOS, the service
        will start on next boot unless it is disabled. Use ``service.disable``
        to disable the service

    :param str name: Service label, file name, or full path

    :param str runas: User to run launchctl commands

    :return: ``True`` if successful or if the service is already stopped
    """
    # Get the domain target.
    domain_target, path = await _get_domain_target(name)

    # Stop (bootout) the service: will raise an error if it fails
    return await hub.exec.service.launchctl("bootout", domain_target, path, runas=runas)


def validate_enabled(hub, enabled: bool or int or str) -> str:
    """
    Helper function to validate the enabled parameter. Boolean values are
    converted to "on" and "off". String values are checked to make sure they are
    either "on" or "off"/"yes" or "no". Integer ``0`` will return "off". All
    other integers will return "on"

    :param enabled: Enabled can be boolean True or False, Integers, or string
    values "on" and "off"/"yes" and "no".

    :return: "on" or "off" or errors
    """
    if isinstance(enabled, Text):
        if enabled.lower() not in ["on", "off", "yes", "no"]:
            msg = (
                "\nMac Power: Invalid String Value for Enabled.\n"
                "String values must be 'on' or 'off'/'yes' or 'no'.\n"
                f"Passed: {enabled}"
            )
            raise SaltInvocationError(msg)

        return "on" if enabled.lower() in ["on", "yes"] else "off"

    return "on" if enabled else "off"
