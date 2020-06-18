import json
from enum import Enum, auto
import logging
import requests
from pkg_resources import parse_version

logger = logging.getLogger(__name__)


class CheckVersionMessage(Enum):
    new_version_available = auto()
    latest_version_installed = auto()
    no_internet = auto()
    error = auto()
    not_checked = auto()


def check_outdated(version: str, package: str = 'dummpy_autoupdate') -> CheckVersionMessage:
    logger.info(f'Checking the latest version of the {package} package.')

    url = 'https://pypi.python.org/pypi/%s/json' % package

    try:
        response = requests.get(url).text
    except requests.ConnectionError:
        logger.info(f'No internet.')
        return CheckVersionMessage.no_internet

    try:
        current_version = parse_version(version)
        latest_version = json.loads(response)['info']['version']
        latest_version = parse_version(latest_version)

        if current_version < latest_version:
            message = CheckVersionMessage.new_version_available
            message.version = latest_version
            logger.info(f'new version available : {message.version}.')
            return message
        else:
            message = CheckVersionMessage.latest_version_installed
            message.version = latest_version
            logger.info(f'latest_version_installed : {message.version}.')
            return message
    except Exception as err:
        logger.exception(err)
        return CheckVersionMessage.error
