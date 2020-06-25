import logging
import sys

import click
import click_log

from . import repo_has_same_ast


def _get_logger():
    logger = logging.getLogger(__name__)
    click_log.basic_config(logger)
    return logger


@click.command()
@click.option('--git-dir', default='.', type=click.Path(exists=True, file_okay=False))
@click_log.simple_verbosity_option(_get_logger())
def main(git_dir):
    try:
        has_same_ast = repo_has_same_ast(git_dir, _get_logger())
    except ValueError as e:
        raise click.BadParameter(e)
    if has_same_ast:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
