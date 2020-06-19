import dummy_autoupdate
import importlib
import sys


def main():
    reboot_code = dummy_autoupdate.MainWindow.EXIT_CODE_REBOOT
    exit_code = dummy_autoupdate.run()

    while exit_code == reboot_code:
        importlib.reload(dummy_autoupdate)
        reboot_code = dummy_autoupdate.MainWindow.EXIT_CODE_REBOOT

        exit_code = dummy_autoupdate.run()

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
