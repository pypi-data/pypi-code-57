from .spyder import Spyder

from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser('Spyder')
    parser.add_argument('-p', '--path', default=None,
                        help="A directory to crawl recursively (default: CWD)")
    parser.add_argument('-d', '--depth', default=-1, type=int,
                        help="Depth in directories (default: -1)")
    parser.add_argument('-x', '--exclude', nargs='+',
                        help="List of node names to exclude")
    parser.add_argument('-id', '--include-dot-files', dest='inc_df', action='store_true',
                        help="Include all nodes starting with a dot")

    # Specify suffixes (include/exclude)
    suffixes_group = parser.add_mutually_exclusive_group()
    suffixes_group.add_argument('-si', '--suffix-include', dest='si', nargs='+',
                                help="List of suffixes to include")
    suffixes_group.add_argument('-sx', '--suffix-exclude', dest='sx', nargs='+',
                                help="List of suffixes to exclude")

    # Specify printing options
    printing_group = parser.add_argument_group('Printing')
    printing_group.add_argument('-i', '--ignore-suffixes', action='store_true',
                                help="Don't sort by suffixes")
    return parser.parse_args()


def main():
    args = parse_args()

    spyder = Spyder(args.path, args.depth, args.exclude,
                    args.inc_df, args.si, args.sx)
    print(spyder.summary(args.ignore_suffixes))


if __name__ == "__main__":
    main()
