import subprocess
import sys
import logging
import argparse

CREATE_NO_WINDOW = 0x08000000


def update_version(version: str = '', num_of_attempts: int = 3):
    logger = logging.getLogger(__name__)
    logger.info(f'Updating the package ...')

    try:
        subprocess.check_call(['dummy_autoupdate_update', f'--version={version}',
                               f'--num_of_attempts={num_of_attempts}'],
                              creationflags=CREATE_NO_WINDOW)
        return True

    except subprocess.CalledProcessError as err:
        logger.exception(err)
        return False


def script_update() -> int:
    parser = argparse.ArgumentParser(description='Update dummy_autoupdate package.')

    parser.add_argument('--version', type=str, default='', help='the target version')
    parser.add_argument('--num_of_attempts', type=int, default=3, help='number of attempts to update')
    parser.add_argument('--package', type=str, default='dummy_autoupdate', help='the target package')

    args = parser.parse_args()
    num_of_attempts: int = args.num_of_attempts
    package: str = args.package
    version: str = args.version

    if version:
        package = f'{package}=={version}'

    for i in range(num_of_attempts):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "--upgrade", package],
                                  creationflags=CREATE_NO_WINDOW)
            return 0

        except subprocess.CalledProcessError:
            continue

    return 1


if __name__ == '__main__':
    script_update()
