import logging
import click
from lb_utils.log_utils import set_up_logging
from lb_utils.string_utils import StringUtils
from lb_utils.file_utils import FileUtils
from lb_dev.constants import license_constants
from lb_dev.commands.copyright.check_for_license_file.check_for_license import check_for_license
import requests
from requests.models import Response
from json import loads
from datetime import datetime
import os

logger = logging.getLogger(__name__)

# TODO re-enable when copyright package is split
# @click.command(name='create-license-file')
# @click.option('-v', '--verbose', count=True)
# @click.option('--path', '-p', default='.')
# @click.option('--name', '-n', default='LICENSE')
# @click.option('--license', '-l', type=click.Choice(['apache-2.0', 'gpl-3.0', 'mit']), default='gpl-3.0',)
# def create_license_file_command(verbose, path, name, license):
#     set_up_logging(verbose)
#     return create_license_file_if_not_exists(path, name, license)


def create_license_file_if_not_exists(path, name, license):
    """
    takes in as a parameter a path as a string, a file name
    and a license type. If a license file already exists in that
    path, exits. Otherwise, creates a file called [name] in [path]
    and writes the [license] content inside it. Returns 0 if it
    succeeded or non-zero number if it failed

    :param path: str

    :param name: str

    :param license: str
    
    :return int
    """
    logger.debug(
        'Called create-license-file with parameters: path={}, name={}, license={}'.format(path, name, license))
    print('creating license file')

    logger.info('checking for existing copyright file')
    has_copyright = check_for_license(path) == 0

    if has_copyright:
        logger.error('Error: This repository already has a copyright file')
        print('Error: This repository already has a copyright file')
        return 1
    else:
        return create_license_file(path, name, license)


def create_license_file(path, name, license):
    """
    takes in as a parameter a path, a file name and a
    license as strings. Attempts to create a file called [name] 
    in [path] and writes the [license] content inside it. 
    Returns 0 if it succeeded or non-zero number if it failed

    :param path: str

    :param name: str

    :param license: str
    
    :return int
    """
    if StringUtils.find_strings_in_list([name], license_constants.LICENSE_FILESNAMES):
        license_file = '/'.join([path, name])

        logger.debug(
            'fetching license from {}'.format(''.join([license_constants.LICENSE_REST_ENDPOINT, license])))
        license_text = get_license_text(license)

        logger.debug('writing {} license in file {}'.format(license, name))
        result_code = write_license_to_file(
            license, license_file, license_text)

        if result_code == 0:
            logger.info('{} created, containing {} license'.format(
                license_file, license))
            print('{} created, containing {} license'.format(
                license_file, license))

        return result_code
    else:
        logger.error('file name {} not in acceptable file names {}'.format(
            name, license_constants.LICENSE_FILESNAMES))
        print('Error: bad file name: {}. Accepted filnames are: {}'.format(name,
                                                                           license_constants.LICENSE_FILESNAMES))

        return 1


def get_license_text(license):
    """
    Takes in as a parameter a license type as string
    Gets the license template from an external API
    and returns it

    :param license: str

    :return str
    """
    request = requests.get(
        ''.join([license_constants.LICENSE_REST_ENDPOINT, license]))
    license_json = request.json()

    return license_json['body']


def write_license_to_file(license, copyright_filename, license_text):
    """
    Takes in as a parameter a license type, a file name
    to write the license and a template of the license content
    If the [license] type is legit, then it  replaces the generic 
    values of [license_text] with normal values and rights the
    content inside [copyright_filename]. Returns 0 if it
    succeeded or 1 if it failed

    :param license: str

    :param copyright_filename: str

    :param license_text: str

    :return int
    """
    license_content = replace_license_placeholders(license_text, license)

    if license_content == 1:
        return license_content

    FileUtils.write_to_file(copyright_filename, license_content)

    return 0


def replace_license_placeholders(license_text, license):
    """
    Takes in as a parameter a license template and a license
    type. If [license] is of a legit type, the generic values
    of the tempalte get replaced with normal ones and the new
    content is returned. Returns 1 if it fails

    :param license_text: str

    :param license: str

    :return str / 1
    """
    if license == 'mit':
        license_content = license_text.replace('[year]', str(
            datetime.now().year)).replace('[fullname]', 'CERN')
    elif license == 'apache-2.0':
        license_content = license_text.replace('[yyyy]', str(
            datetime.now().year)).replace('[name of copyright owner]', 'CERN')
    elif license == 'gpl-3.0':
        license_content = license_text.split(
            'END OF TERMS AND CONDITIONS', 1)[0]
    else:
        print('The license you are trying to use is not currently supported')
        return 1

    return license_content
