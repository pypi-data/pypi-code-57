import re
import subprocess
import sys
import logging
import typing
import datetime
import asyncio
import pyaware

log = logging.getLogger(__file__)


def pip_update_pip_subprocess() -> str:
    process = subprocess.Popen([sys.executable, "-m", "pip", "install", "--upgrade", "wheel", "pip"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode:
        raise IOError(f"Pip update failed Return code {process.returncode}\n{stderr.decode('utf-8')}")
    return stdout.decode('utf-8')


def pip_search_subprocess() -> str:
    process = subprocess.Popen([sys.executable, "-m", "pip", "search", "pyaware"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode:
        raise IOError(f"Pip search failed Return code {process.returncode}\n{stderr.decode('utf-8')}")
    return stdout.decode('utf-8')


def pip_install_subprocess(version: str) -> str:
    if version:
        str_pyaware = f"pyaware=={version}"
    else:
        str_pyaware = f"pyaware"
    process = subprocess.Popen([sys.executable, "-m", "pip", "install", "--upgrade", str_pyaware],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode:
        raise IOError(f"Pip install failed Return code {process.returncode}\n{stderr.decode('utf-8')}")
    return stdout.decode('utf-8')


def find_latest_version() -> str:
    output = pip_search_subprocess()
    try:
        return re.match("pyaware \(([\w\d\.]+)\)", output).group(1)
    except AttributeError:
        raise IOError("Invalid version returned from pip search")


def should_update(spec_version: str, latest_version: bool) -> bool:
    from packaging import version
    try:
        installed_version = version.parse(pyaware.__version__)
    except (TypeError, NameError):
        log.warning(f"Installed pyaware version is an invalid version")
        installed_version = version.parse("")
    if spec_version == "manual":
        log.info("Skipping auto update as version is set to manual")
        return False

    spec_version = version.parse(spec_version)

    if latest_version:
        if installed_version > spec_version:
            log.warning("Installed version is greater than latest version in pypi")
            return False
        if installed_version == spec_version:
            log.info("Installation up to date")
            return False
        return True
    else:
        if installed_version == spec_version:
            log.info("Installation up to date")
            return False
        else:
            return True


def get_versions(version: str):
    if version == "latest":
        try:
            spec_version = find_latest_version()
            latest = True
        except IOError as e:
            log.warning(e.args[0])
            return
    else:
        latest = False
        spec_version = version
    return spec_version, latest


def check_for_updates() -> typing.Optional[str]:
    config = pyaware.config.load_config(pyaware.config.config_main_path)
    version = config.get("aware_version", "latest")
    spec_version, latest = get_versions(version)
    if should_update(spec_version, latest):
        return spec_version


def do_updates():
    version = check_for_updates()
    if version:
        update_pyaware(version)


def update_pyaware(version):
    log.info(f"Updating pyaware to {version}")
    try:
        pip_update_pip_subprocess()
    except IOError as e:
        log.exception(e)
    try:
        pip_install_subprocess(version)
        log.info(f"Successfully updated pyaware to {version}")
        log.info("Stopping pyaware to launch updated version")
        pyaware.stop()
    except IOError as e:
        log.exception(e)
    try:
        pip_install_subprocess("")
        log.error("Updated to latest pyaware version after failed specific version update")
        log.info("Stopping pyaware to launch updated version")
        pyaware.stop()
    except IOError as e:
        log.exception(e)
        log.info(f"Failed to update pyaware to latest version. Continuing execution")
        return


def scheduled_restart(hour, **kwargs):
    now = datetime.datetime.now()
    restart_time = datetime.datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0)
    if restart_time - now < datetime.timedelta(seconds=0):
        restart_time = restart_time + datetime.timedelta(days=1)
    loop = asyncio.get_event_loop()
    return loop.create_task(_restart((restart_time - now).seconds))


async def _restart(seconds):
    await asyncio.sleep(seconds)
    pyaware.stop()
