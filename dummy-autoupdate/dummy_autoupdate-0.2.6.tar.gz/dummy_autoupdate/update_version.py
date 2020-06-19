import subprocess
import sys
import logging
from pathlib import Path


def update_version(package: str = 'dummy_autoupdate') -> bool:
    logger = logging.getLogger(__name__)
    logger.info(f'Updating package {package}')

    executable: str = sys.executable

    if executable.endswith('pythonw.exe'):
        p = Path(executable).parent / 'python.exe'
        if p.is_file():
            executable = str(p.resolve())
        else:
            return False

    try:
        res = subprocess.check_call([executable, "-m", "pip", "install", "--upgrade", package])
        logger.info(f'res = {res}')
        return True
    except subprocess.CalledProcessError:
        return False
