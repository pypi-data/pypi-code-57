from . import *


def main():
    import sys
    command = sys.argv[1]
    print(globals()[command](*sys.argv[2:]))


if __name__ == "__main__":
    main()
