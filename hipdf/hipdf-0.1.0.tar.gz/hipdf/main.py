import argparse
from pathlib import Path

from .core import highlight


def calc_path(path, prefix, out):
    if not out and not prefix:
        return None
    o = Path(out if out else path)
    if prefix:
        valid_prefix = True
        try:
            o = o.with_name(prefix + o.name)
        except ValueError as e:
            valid_prefix = False
        if not valid_prefix:
            raise ValueError(f'Invalid prefix "{prefix}"')
    return o


def main():
    parser = argparse.ArgumentParser(
        description='Highlight the first word of an English sentence in PDF file.'
    )
    parser.add_argument('path', help='Name of the file to be highlighted.')
    parser.add_argument('-o', dest='out', help='Name of the output file.')
    parser.add_argument('-p', dest='prefix', help='Prefix of the output file.')
    args = parser.parse_args()

    path = Path(args.path)
    out_path = calc_path(path, args.prefix, args.out)
    if not path.exists():
        raise ValueError(f'File "{path}" do not exist.')

    out, count = highlight(path, out_path)
    print(f'Saving to "{out}" with {count} highlights.')


if __name__ == '__main__':
    main()
