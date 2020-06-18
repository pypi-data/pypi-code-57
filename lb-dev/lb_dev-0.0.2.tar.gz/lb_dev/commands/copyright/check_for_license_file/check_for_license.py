import click
import logging

from lb_utils.log_utils import set_up_logging
from lb_utils.file_utils import FileUtils
from lb_utils.string_utils import StringUtils
from lb_dev.constants import license_constants

logger = logging.getLogger(__name__)

# TODO re-enable when copyright package is split
# @click.command(name='check-for-license')
# @click.option('--path', '-p', default='.')
# @click.option('-v', '--verbose', count=True)
# def check_for_license_command(path, verbose):
#     set_up_logging(verbose)
#     check_for_license(path)    

def check_for_license(path='.'):
    """
    Takes in as a parameter a path as string 
    (by default current directory)
    Checks if a license file exists in [path]
    Returns 0 if exists, otherwise 1

    :param path: str

    :return 0/1
    """
    file_names = FileUtils.get_non_empty_filenames(path)

    logger.info('These files exist in the given path and are not empty: {}'.format(file_names))

    license_files = StringUtils.find_strings_in_list(
        file_names, license_constants.LICENSE_FILESNAMES)

    logger.debug('found license files: {}'.format(license_files))

    if license_files:
        logger.info('found {} license files in directory'.format(
            len(license_files)))
        print('This directory does have a license file')
        return 0
    else:
        logger.info('There is no license file in this directory')
        print('There is no license file in this directory\n\nYou can fix this by running \'lb-dev create-license-file\'')
        return 1
