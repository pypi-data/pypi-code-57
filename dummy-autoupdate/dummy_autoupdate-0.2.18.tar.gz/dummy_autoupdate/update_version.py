import subprocess
import sys
import logging
from pathlib import Path


def update_version(package: str = 'dummy_autoupdate') -> bool:
    logger = logging.getLogger(__name__)
    logger.info(f'Updating package {package}')

    executable: str = sys.executable

    if executable.endswith('pythonw.exe'):
        logger.info(f'Executable is pythonw.exe: {executable}.')
        p = Path(executable).parent / 'python.exe'
        if p.is_file():
            executable = str(p.resolve())
        else:
            logger.info(f'No python.exe interpreter found.')
            return False

    try:
        logger.info(f'Updating the package with {executable}.')
        CREATE_NO_WINDOW = 0x08000000
        res = subprocess.check_call([executable, "-m", "pip", "install", "--upgrade", package],
                                    creationflags=CREATE_NO_WINDOW)
        logger.info(f'res = {res}')
        return True

    except subprocess.CalledProcessError:
        return False
