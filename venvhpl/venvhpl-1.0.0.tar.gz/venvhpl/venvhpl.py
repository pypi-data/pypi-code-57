"""Main script for linking packages into a virtualenv's site-packages"""
import os, sys, glob, subprocess, logging
from distutils import sysconfig

VENV = os.environ.get('VIRTUAL_ENV')
PYTHON = 'python%s.%s' % sys.version_info[:2]


def get_host_package_location(package):
    """Find the given host-package to link"""
    env = os.environ.copy()
    env['PATH'] = os.pathsep.join(
        [
            p
            for p in os.environ.get('PATH').split(os.pathsep)
            if not p.startswith(VENV + os.sep)
        ]
    )
    output = (
        subprocess.check_output(
            [
                PYTHON,
                '-c',
                'import os, %(package)s; print(os.path.abspath(os.path.dirname(%(package)s.__file__)))'
                % {'package': package,},
            ],
            env=env,
        )
        .decode('ascii', 'ignore')
        .strip()
    )
    return output


def get_target_directory():
    """Get the directory into which distutils would install packages"""
    if not VENV:
        raise RuntimeError("We don't seem to be running in a virtualenv")
    return os.path.abspath(sysconfig.get_python_lib())


def get_options():
    import argparse

    parser = argparse.ArgumentParser(
        description='Link host python package into the current virtualenv'
    )
    parser.add_argument(
        'packages',
        nargs='+',
        help='Python package name (importable name) to link into site packages',
    )
    return parser


def main():
    options = get_options().parse_args()
    log = logging.getLogger('venv-hpl')
    sources = []
    for package in options.packages:
        sources.append((package, get_host_package_location(package)))
    site = get_target_directory()
    for package, source in sources:
        target = os.path.join(site, package)
        if os.path.lexists(target):
            os.remove(target)
        log.info("%s => %s", source, target)
        os.symlink(source, target)
