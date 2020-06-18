import click
import logging
import os
import re
from datetime import date
from itertools import islice
import fileinput


from lb_dev.commands.copyright.builders.copyright_builder import CopyrightBuilder
from lb_dev.commands.copyright.scanner.copyright_scanner import CopyrightScanner
from lb_utils.log_utils import set_up_logging
from lb_utils.file_utils import FileUtils
from lb_utils.string_utils import StringUtils
from lb_dev.constants import license_constants

logger = logging.getLogger(__name__)

# TODO re-enable when copyright package is split
# @click.command(name='add-copyright', help='Add standard LHCb copyright statement to files.')
# @click.argument('files', nargs=-1)
# @click.option('--year', '-y', help='copyright year specification (default: current year)')
# @click.option('--license-type', '-t', type=click.Choice(['apache-2.0', 'gpl-3.0', 'mit'], case_sensitive=False), default='gpl-3.0', help='Type of license to use in the copyright (default: GPL3)')
# @click.option('--owner', '-o', default='CERN for the benefit of the LHCb collaboration', help='rights owner (default: CERN for the benefit of the LHCb collaboration)')
# @click.option('--license-fn', '-l', help='Name of the license file (default: COPYING)')
# @click.option('--force', '-f', is_flag=True, help='add copyright also to non supported file types')
# @click.option('-v', '--verbose', count=True)
# def add_copyright_command(files, year, license_fn, force, verbose):
#     set_up_logging(verbose)
#     add_copyright(files, year, license_fn, force)


def add_copyright(files, year, license_type, owner, license_fn, force):
    logger.debug('called \'lb-dev add-copyright\' with files: {}, \
    , year: {}, license type: {}, owner: {}, license filename: {}, force: {}'
    .format(files, year, license_constants, owner, license_fn, force))
    logger.info('generating copyright statement')
    results = []
    for path in files:
        if not force and not FileUtils.to_check(path, license_constants.CHECKED_FILES):
            print('warning: cannot add copyright to {} (file type not '
                'supported)'.format(path))
            results.append(1)
        elif FileUtils.has_pattern(path, license_constants.COPYRIGHT_SIGNATURE):
            print('warning: {} already has a copyright statement'.format(path))
            results.append(1)
        else:
            results.append(add_copyright_to_file(path, year, license_type,
                                owner, license_fn))

    return 1 if 1 in results else 0

def update_copyright_year(files, update_year):
    results = []
    for file in files:
        copyright_scanner = CopyrightScanner()
        copyright_scanner.set_file_path(file)
        owner = copyright_scanner.extract_owner()
        license_file_name = copyright_scanner.extract_license_file_name()
        license_type = copyright_scanner.extract_license_type()

        _, start_line, end_line = copyright_scanner.extract_copyright_statement()

        FileUtils.delete_lines(file, start_line, end_line)

        result = add_copyright_to_file(file, update_year, license_type, owner, license_file_name)
        results.append(result)

    return 1 if 1 in results else 0

def add_copyright_to_file(path, year=None, license_type='gpl-3.0', owner='CERN for the benefit of the LHCb collaboration', license_fn=None):
    '''
    Add copyright statement to the given file for the specified year (or range
    of years).  If the year argument is not specified, the current year is
    used.
    '''
    lang = FileUtils.get_language_family(path)
    logger.debug('language family of {} is {}'.format(path, lang))
    copyright_text = get_copyright_text(year, owner, license_type, license_fn)
    line_length = len(copyright_text.split('\n')[0]) + 5 if len(copyright_text.split('\n')[0]) > 75 else 80
    commented_copyright = StringUtils.to_comment(copyright_text, lang, line_length)

    with open(path, 'r') as f:
        data = f.readlines()

    offset = get_copyright_offset(data, path, lang)
    
    logger.info('writing copyright statement to file')
    data.insert(offset, commented_copyright)
    with open(path, 'w') as f:
        f.writelines(data)

    return 0

def get_copyright_offset(file_data, path, lang):
    offset = 0
    encoding_offset = FileUtils.find_pattern_line(file_data, license_constants.ENCODING_DECLARATION)

    if encoding_offset is not None:
        offset = encoding_offset + 1
    elif file_data[0].startswith('#!'):
        offset = 1
    elif lang == 'xml':
        offset = 1 if not path.endswith('.ent') else 0
        for l in file_data:
            if l.strip():
                # lcgdict selection files are a bit special
                if 'lcgdict' in l or '<!--' in l:
                    offset = 0
                break

    return offset

def get_copyright_text(year, owner, license_type, license_fn):
    copyright_builder = CopyrightBuilder()
    copyright_builder.add_year(year or date.today().year)
    copyright_builder.add_owner(owner)
    copyright_builder.add_license_type(license_type)
    copyright_builder.add_license_file(license_fn or 'COPYING')

    copyright_text = copyright_builder.build_copyright()

    return copyright_text
    



