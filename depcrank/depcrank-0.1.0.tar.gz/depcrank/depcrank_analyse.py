
#!/usr/bin/env python
"""
FIXME: insert program metadata
"""

import click
import json
from depcrank.analyse import calculate_average_consumers


@click.command()
@click.option('--input-path', '-i', help='Path to input file.')
@click.option('--calculate-average-consumption', '-c', is_flag=True,
    default=None, help='Calculate the average consumption of a package')
def main(input_path, calculate_average_consumption):
    with open(input_path) as fp:
        input_data = json.load(fp)
    if calculate_average_consumption is True:
        average_consumers = calculate_average_consumers(input_data)
        click.echo('The average consumption of a package is %f.' % \
            average_consumers)


if __name__ == '__main__':
    main()
