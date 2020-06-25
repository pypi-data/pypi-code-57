#!/usr/bin/env python
"""
FIXME: insert program metadata
"""

import click
import json
from depcrank.rank import calculate_pagerank, calculate_transitive_indegree


@click.command()
@click.option('--input-path', '-i', help='Path to input file.')
@click.option('--output-path', '-o',
    help='Path to output file. If directory, a default file is created within '
    'the directory.')
@click.option('--personalization-path', '-p', default=None,
    help='Path to personalization scores.')
@click.option('--algorithm', '-a', default='transitive-indegree',
    help='Algorithm to use to rank packages.')
def main(input_path, output_path, personalization_path, algorithm):
    with open(input_path) as fp:
        input_data = json.load(fp)
    if personalization_path:
        with open(personalization_path) as fp:
            personalization = json.load(fp)

    if algorithm == 'pagerank':
        result = calculate_pagerank(input_data, personalization)
    elif algorithm == 'transitive-indegree':
        result = calculate_transitive_indegree(input_data)

    with open(output_path, 'w+') as fp:
        json.dump(result, fp)


if __name__ == '__main__':
    main()
