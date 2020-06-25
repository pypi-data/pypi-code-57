
#!/usr/bin/env python
"""
FIXME: insert program metadata
"""

import click
import json
from depcrank.display import find_single_rank, find_top_ranks


DEFAULT_RANKS = "1-30"


@click.command()
@click.option('--input-path', '-i', help='Path to input file.')
@click.option('--ranks', '-r', default=DEFAULT_RANKS, help='Ranks to display.')
@click.option('--package', '-p', default=None, help='Specify a package.')
@click.option('--exclude-path', '-e', default=None)
def main(input_path, ranks, package, exclude_path):
    with open(input_path) as fp:
        input_data = json.load(fp)
    if exclude_path:
        with open(exclude_path) as fp:
            exclude = json.load(fp)
    else:
        exclude = None
    if package is not None:
        package_stats = find_single_rank(input_data, package, exclude)
        if package_stats is None:
            click.echo('No rank stats found for %s' % package)
        else:
            click.echo('Package %s has rank %d with score %f' % \
                (package, package_stats[0], package_stats[1]))
    else:
        rank_stats = find_top_ranks(input_data, ranks, exclude)
        # TODO: different error handling? return None?
        for item in rank_stats:
            click.echo('%d\t%s\t%f' % item)


if __name__ == '__main__':
    main()
