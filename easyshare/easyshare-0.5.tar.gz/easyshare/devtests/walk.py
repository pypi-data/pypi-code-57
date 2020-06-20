import os
from pathlib import Path

from easyshare.logging import init_logging
from easyshare.utils.os import walk_preorder

if __name__ == "__main__":
    print("-- TOPDOWN --")
    for root, dirnames, files in os.walk("/home/stefano/Temp", topdown=True):
        print(f"{root}")

        for f in files:
            print(f"-> f = {f}")

        for d in dirnames:
            print(f"-> f = {d}")

    print()
    # print("-- NO TOPDOWN --")
    # for root, dirnames, files in os.walk("/home/stefano/Temp", topdown=False):
    #     print(f"{root}")
    #
    #     for f in files:
    #         print(f"-> f = {f}")
    #
    #     for d in dirnames:
    #         print(f"-> f = {d}")

    init_logging(5)
    os.chdir("/home/stefano/Temp")
    for f in walk_preorder(Path("")):
        print(f)
    # walk_preorder(Path("/home/stefano/Temp"))