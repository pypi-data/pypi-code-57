"""
The command line interface to s3bkt.

Major help from: https://www.youtube.com/watch?v=kNke39OZ2k0
"""
import sys
import logging
import click
from s3bkt import S3Utility

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s (%(module)s) %(message)s',
    datefmt='%Y/%m/%d-%H:%M:%S'
)

logger = logging.getLogger(__name__)


@click.command()
@click.option('--directory', '-d', required=True, help='directory that holds the bucket config')
@click.option('--region', '-r', help='AWS region')
@click.option('--profile', '-p', help='AWS credential profile')
@click.version_option(version='0.2.0')
def main(directory, region, profile):
    '''
    The main entry point for this utility

    Args:
        directory - directory that holds the bucket config

    Returns:
        None
    '''
    try:
        tool = S3Utility(
            directory=directory,
            profile=profile,
            region=region
        )

        if tool.work():
            logger.info('bucket work went well')
            sys.exit(0)
        else:
            logger.warning('bucket work did not go well')
            sys.exit(1)
    except Exception as wtf:
        logger.error(wtf, exc_info=False)
        sys.exit(2)
