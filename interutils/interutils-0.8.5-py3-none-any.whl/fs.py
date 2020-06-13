from subprocess import call, check_output, DEVNULL, CalledProcessError
from os import listdir
from pathlib import Path
from typing import Optional

from .interactive import pr, choose, cyan


def choose_file(root_dir: Path) -> Optional[Path]:
    def _format(root_dir: Path, entry: str) -> str:
        f = root_dir / entry
        if f.is_dir():
            return entry
        return f'{entry}\t({human_bytes(f.stat().st_size)}, {count_lines(f)})'
    listing = listdir(root_dir)
    if not listing:
        return pr('Empty directory!', '!')
    while 1:
        c = choose([_format(root_dir, i) for i in listing], default=-1)
        if c < 0:
            return
        f = root_dir / listing[c]
        if f.is_dir():
            f = choose_file(root_dir / f)
            if not f:
                continue
        return f


def count_lines(file_path: Path) -> int:
    # TODO Crossplatformize
    return 1 + int(check_output(('/usr/bin/wc', '-l', str(file_path.resolve()))).decode().split(' ')[0])


def human_bytes(size_in_bytes: int) -> str:
    unit = 0
    while size_in_bytes >= 1024:
        unit += 1
        size_in_bytes /= 1024
    return str(round(size_in_bytes)) + ('', 'KB', 'MB', 'GB', 'TB')[unit]


def file_volume(path: Path) -> tuple:
    """
    Returns:
        [0] => Size in bytes
        [1] => Lines count
        [2] => A colored string that includes a human-readable representation of both values 
    """
    sb = path.stat().st_size
    lc = count_lines(path)
    return sb, lc, f'{cyan(path.name)} ({human_bytes(sb)}, {lc})'


def is_image(image_path: str) -> (str, None):
    """
    Checks the file signature (magic number)
            for an image

    :param image_path: The path to the image
    :return: True if the image is PNG or JPG
    """

    signatures = {'JPG': 'ffd8ff',
                  'PNG': '89504e',
                  'GIF': '474946'}

    with open(image_path, 'rb') as img_file:
        signature = img_file.read(3).hex()
        for sig in signatures:
            if signature == signatures[sig]:
                return sig
    return None


def is_package(package_name) -> (str, None):
    """
    Check if a system package is installed

    :param package_name: Package to check
    :return: The version of the installed package or None if no such package
    """
    try:
        return check_output(['/usr/bin/pacman', '-Q', package_name], stderr=DEVNULL).decode().strip().split(' ')[1]
    except CalledProcessError:
        return False
    except FileNotFoundError:
        try:
            return check_output(('apt', 'list', '-qq', package_name)).decode().split(' ')[1]
        except CalledProcessError:
            pass
    return None
