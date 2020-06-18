import subprocess
import sys
import logging


def update_version(package: str = 'dummy_autoupdate') -> bool:
    logger = logging.getLogger(__name__)
    logger.info(f'Updating package {package}')
    # return False
    try:
        res = subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
        logger.info(f'res = {res}')
        return True
    except subprocess.CalledProcessError as err:
        logger.exception(err)
        return False



