
import sys
import site
import gc


def main():
    import dummy_autoupdate

    reboot_code: int = dummy_autoupdate.MainWindow.EXIT_CODE_REBOOT
    exit_code: int = dummy_autoupdate.run()

    while exit_code == reboot_code:

        user_path = site.getusersitepackages()
        system_path = site.getsitepackages()

        sys.path = [user_path] + system_path + sys.path

        modules = [module for module in sys.modules if module.startswith('dummy_autoupdate')]
        for module in modules:
            sys.modules.pop(module)

        del dummy_autoupdate

        gc.collect()

        import dummy_autoupdate

        reboot_code = dummy_autoupdate.MainWindow.EXIT_CODE_REBOOT

        exit_code = dummy_autoupdate.run()

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
