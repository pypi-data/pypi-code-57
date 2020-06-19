import subprocess
import sys
import logging
from pathlib import Path
import argparse

CREATE_NO_WINDOW = 0x08000000


def update_version(version: str = '', num_of_attempts: int = 3):
    logger = logging.getLogger(__name__)
    logger.info(f'Updating the package ...')

    try:
        subprocess.check_call(['dummy_autoupdate_update', f'--version={version}',
                               f'--num_of_attempts={num_of_attempts}'])
        return True

    except subprocess.CalledProcessError:
        return False


def update_version_old(package: str = 'dummy_autoupdate',
                       version: str = None,
                       num_of_attempts: int = 3) -> bool:
    logger = logging.getLogger(__name__)

    if version:
        package = f'{package}=={version}'

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

    for i in range(num_of_attempts):
        try:
            logger.info(f'Updating the package with {executable} (attempt {i + 1}).')
            subprocess.check_call([executable, "-m", "pip", "install", "--upgrade", package],
                                  creationflags=CREATE_NO_WINDOW)
            return True

        except subprocess.CalledProcessError:
            continue

    return False


def script_update():
    parser = argparse.ArgumentParser(description='Update dummy_autoupdate package.')

    parser.add_argument('--version', type=str, default='', help='the target version')
    parser.add_argument('--num_of_attempts', type=int, default=2, help='number of attempts to update')
    parser.add_argument('--package', type=str, default='dummy_autoupdate', help='the target package')

    args = parser.parse_args()
    num_of_attempts: int = args.num_of_attempts
    package: str = args.package
    version: str = args.version

    if version:
        package = f'{package}=={version}'

    for i in range(num_of_attempts):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
            return True

        except subprocess.CalledProcessError:
            continue

    return False


if __name__ == '__main__':
    script_update()
