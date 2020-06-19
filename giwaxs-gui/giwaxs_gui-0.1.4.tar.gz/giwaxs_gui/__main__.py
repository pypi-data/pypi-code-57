# -*- coding: utf-8 -*-

import site
import sys
import gc


def main():
    from giwaxs_gui.update import check_version_program, CheckVersionMessage

    res: CheckVersionMessage = check_version_program()

    user_path = site.getusersitepackages()
    system_path = site.getsitepackages()

    sys.path = [user_path] + system_path + sys.path

    modules = [module for module in sys.modules if module.startswith('giwaxs_gui')]
    for module in modules:
        sys.modules.pop(module)

    gc.collect()

    from giwaxs_gui import run

    sys.exit(run(res))


if __name__ == '__main__':
    main()
