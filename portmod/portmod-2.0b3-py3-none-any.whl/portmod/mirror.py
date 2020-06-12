# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
import shutil
import argparse
import sys
import traceback
from logging import error
from portmod.repo.loader import load_all
from portmod.repo.download import download_mod, mirrorable


def mirror():
    parser = argparse.ArgumentParser(
        description="Command line interface to update a local mirror"
    )
    parser.add_argument("--mirror", metavar="DIR", help="Directory to mirror into")
    parser.add_argument("--debug", help="Enables debug traces", action="store_true")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()

    if args.mirror:
        os.makedirs(args.mirror, exist_ok=True)
        for mod in load_all():
            if mirrorable(mod):
                try:
                    for source in download_mod(mod, True):
                        path = os.path.join(args.mirror, source.name)
                        if not os.path.exists(path):
                            print("Copying {} -> {}".format(source.path, path))
                            shutil.copy(source.path, path)
                except Exception as e:
                    traceback.print_exc()
                    error("{}", e)
