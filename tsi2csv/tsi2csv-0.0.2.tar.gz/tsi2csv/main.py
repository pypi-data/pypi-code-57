"""
main.py - main functionality for tsi2csv

The conversion is simple, so everything is done in the cli main function.
"""

import click
import csv
import sys

@click.command(help='Convert from multi-omics tsi data to csv')
@click.option('--output', '-o', type=click.File('w'), default=sys.stdout,
              help='Optional output file')
@click.argument('infile', type=click.File('r'), default=sys.stdin)
def cli(output, infile):
    data = dict()
    for line in infile:
        vals = line.strip().split("\t")
        data[vals[0]] = vals[1:]

    keys = [k for k in data.keys()]
    rows = list()
    rows.append(keys)
    data_len = len(data[keys[0]])
    for i in range(data_len):
        row = list()
        for k in keys:
            row.append(data[k][i])
        rows.append(row)

    writer = csv.writer(output)
    writer.writerows(rows)

if __name__ == '__main__':
    cli()
