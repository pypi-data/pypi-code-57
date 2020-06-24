import argparse

from dipas.build import from_file


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()

    sequence = from_file(args.file)
    print(sequence)
    print(f'# {len(sequence.elements)}')
