# -*- coding: utf-8 -*-

import site
import logging
import sys
import gc
import argparse
from giwaxs_gui.update import check_version_program, CheckVersionMessage


def main():
    parser = argparse.ArgumentParser(description='Program for GIWAXS analysis')

    parser.add_argument('--skip_update', action='store_true', help='skip checking for updates before launching')
    parser.add_argument('-d', '--debug', action='store_true', help='open program in debug mode')

    args = parser.parse_args()
    skip_update: bool = args.skip_update
    level = logging.DEBUG if args.debug else logging.ERROR

    if not skip_update:

        res: CheckVersionMessage = check_version_program()

        user_path = site.getusersitepackages()
        system_path = site.getsitepackages()

        sys.path = [user_path] + system_path + sys.path

        modules = [module for module in sys.modules if module.startswith('giwaxs_gui')]

        for module in modules:
            sys.modules.pop(module)

        gc.collect()

    else:
        res: CheckVersionMessage = CheckVersionMessage.not_checked

    from giwaxs_gui import run

    sys.exit(run(res, level))


if __name__ == '__main__':
    main()
