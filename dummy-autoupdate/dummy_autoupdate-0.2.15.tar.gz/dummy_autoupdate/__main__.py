import dummy_autoupdate
import importlib
import sys
import site


def main():
    global dummy_autoupdate
    reboot_code = dummy_autoupdate.MainWindow.EXIT_CODE_REBOOT
    exit_code = dummy_autoupdate.run()

    while exit_code == reboot_code:
        user_path = site.getusersitepackages()
        system_path = site.getsitepackages()

        sys.path = [user_path] + system_path + sys.path

        dummy = [module for module in sys.modules if module.startswith('dummy_autoupdate')]
        for module in dummy:
            sys.modules.pop(module)

        del dummy_autoupdate
        import dummy_autoupdate

        reboot_code = dummy_autoupdate.MainWindow.EXIT_CODE_REBOOT

        exit_code = dummy_autoupdate.run()

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
