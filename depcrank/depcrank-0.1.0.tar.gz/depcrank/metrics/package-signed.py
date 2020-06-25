"""
FIXME: insert program metadata
"""

import os
import json

PKGBUILD_SUB_ROOTS = ['packages', 'community']
PKGBUILD_FULL_PATH_FORMAT = '{}/{}/trunk/PKGBUILD'
DEFAULT_LOG_COUNT = 75


def _check_if_signed(pkgbuild):
    if 'validpgpkeys' in pkgbuild:
        if '.sig' in pkgbuild or '.asc' in pkgbuild or '.sign' in pkgbuild:
            # FIXME: makes a massive assumption that the strings can only occur
            # for signatures
            # example: "ascii" will trigger this but hopefully we don't have a
            # bunch of validpgpkeys without actually having signatures :/
            return True
    return False

def _dump_stats(package_status, output_path):
    with open(output_path, 'w') as fp:
        json.dump(package_status, fp)


def find_if_signed(pkgbuild_root, output_path, fresh=False):
    if fresh and os.path.exists(output_path):
        with open(output_path) as fp:
            package_status = json.load(fp)
    else:
        package_status = {}

    i = 0
    for sub_root in PKGBUILD_SUB_ROOTS:
        sub_root_path = os.path.join(os.path.abspath(pkgbuild_root), sub_root)
        for package in os.listdir(sub_root_path):
            if not os.path.isdir(os.path.join(sub_root_path, package)):
                #FIXME: log failure
                continue
            pkgbuild_path = PKGBUILD_FULL_PATH_FORMAT.format(
                sub_root_path, package)
            if not os.path.exists(pkgbuild_path):
                package_status[package] = "PKGBUILD NOT FOUND"
                continue
            
            with open(pkgbuild_path, encoding='ISO-8859-1') as fp:
                pkgbuild = fp.read()
            
            print('Checking if {} is signed...'.format(package), end='',
                flush=True)
            package_status[package] = _check_if_signed(pkgbuild)
            i += 1
            if i % DEFAULT_LOG_COUNT == 0:
                _dump_stats(package_status, output_path)
        
        _dump_stats(package_status, output_path) # between sub roots
    
    _dump_stats(package_status, output_path) # final