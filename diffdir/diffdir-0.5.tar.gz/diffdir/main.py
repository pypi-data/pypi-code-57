import os
import sys
from diffdir.ContentDirCmp import ContentDirCmp
import argparse
import signal
from colorama import init, Style, Fore


def catchthesignal(signal, frame):
    sys.exit(1)


signal.signal(signal.SIGINT, catchthesignal)


init()


def is_tool(name):
    from shutil import which

    return which(name) is not None


def diff_files(f1, f2):
    if is_tool("nvim"):
        os.system("nvim -d " + f1 + " " + f2)
    else:
        os.system("vimdiff " + f1 + " " + f2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir_a", help="directory a")
    parser.add_argument("dir_b", help="directory b")

    args = parser.parse_args()

    dir_a = os.path.expanduser(args.dir_a)
    dir_b = os.path.expanduser(args.dir_b)
    dd = ContentDirCmp(dir_a, dir_b)
    lefts, rights, diffs, funnys = [], [], [], []
    for lx, rx, dx, fx in dd.work():
        lefts.extend(lx)
        rights.extend(rx)
        diffs.extend(dx)
        funnys.extend(fx)
    if not lefts and not rights and not diffs and not funnys:
        print(">>> The two dirs are identical.")
        sys.exit(0)
    # main loop
    while True:
        for lx in lefts:
            print(f"{Fore.MAGENTA}Only in {dir_a}:\t{lx}{Style.RESET_ALL}")
        for rx in rights:
            print(f"{Fore.CYAN}Only in {dir_b}:\t{rx}{Style.RESET_ALL}")
        for i, dx in enumerate(diffs):
            print(
                Fore.YELLOW
                + f"({i})  Diff {Fore.MAGENTA}{dir_a}\t{Fore.CYAN}{dir_b}\t\t{Fore.YELLOW}{dx}{Style.RESET_ALL}"
            )
        print("(q)Quit;(d)Diff all;(dX)Diff line X")
        op = input()
        if op == "q":
            break
        if op == "d":
            for diff_item in diffs:
                diff_item = diff_item.lstrip("/")
                f1 = os.path.join(dir_a.rstrip("/"), diff_item)
                f2 = os.path.join(dir_b.rstrip("/"), diff_item)
                diff_files(f1, f2)
                input("Press any key to continue")
        elif len(op) > 1 and op[0] == "d":
            try:
                diff_item = diffs[int(op[1:])]
                f1 = os.path.join(dir_a.rstrip("/"), diff_item)
                f2 = os.path.join(dir_b.rstrip("/"), diff_item)
                diff_files(f1, f2)
            except:
                print(
                    Fore.RED + "*" * 5 + " Invalid input! " + "*" * 5 + Style.RESET_ALL
                )
