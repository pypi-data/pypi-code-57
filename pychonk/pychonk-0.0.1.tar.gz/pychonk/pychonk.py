import os
from dataclasses import dataclass
from distutils.sysconfig import get_python_lib


# https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python
def get_size(start_path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


@dataclass
class PackageInfo:
    name: str
    size: int


def chonk(topx: int = None):
    package_dir = get_python_lib()
    potential_packages = get_immediate_subdirectories(package_dir)

    # must be a better way. Anything 'universal' we can detect in package subfolders?
    potential_packages = [p for p in potential_packages if not p.endswith('-info') and not p.startswith('_')]

    loooongest_package_nam = 0
    package_infos = []
    for package_name in potential_packages:
        package_location = os.path.join(package_dir, package_name)
        size = get_size(package_location)
        package_infos.append(PackageInfo(name=package_name, size=size))
        len_package_name = len(package_name)
        if len_package_name > loooongest_package_nam:
            loooongest_package_nam = len_package_name

    package_infos.sort(key=lambda x: x.size, reverse=False)
    if topx:
        package_infos = package_infos[-topx:]
    biggest = package_infos[-1].size
    for p in package_infos:

        dif_from_biggest = int(60 * (p.size / biggest))
        size_indicator = ''.join(['#' for _ in range(dif_from_biggest)])
        if len(size_indicator) == 0:
            size_indicator = ' '

        mb = str(round(p.size / 1000000, 1)) + ' MB'
        max_expected_package_mb_chars = 9  # <1000.00 MB
        mb += ''.join(' ' for _ in range(max_expected_package_mb_chars - len(mb)))
        suffix_spaces = ''.join([' ' for _ in range(loooongest_package_nam - len(p.name))])

        print(f"{p.name}{suffix_spaces} {mb} {size_indicator}")


chonk()
