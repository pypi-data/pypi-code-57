import sys

from .file_system_root import FilesystemRoot
from .commander import Commander
from .bash import Bash


def main():
    bash = Bash(*sys.argv[1:])
    try:
        output = Commander(bash.root).handle(*bash.commands)
    except (RuntimeError, ValueError) as error:
        output = f"Error: {str(error)}"
    if output:
        print(output)


if __name__ == '__main__':
    main()
