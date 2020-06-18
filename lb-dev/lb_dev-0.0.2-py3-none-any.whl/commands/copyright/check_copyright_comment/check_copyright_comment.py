import click
from lb_utils.log_utils import set_up_logging
from lb_dev.constants import license_constants
from lb_utils.file_utils import FileUtils
import os
import re
from itertools import islice
import logging
from subprocess import check_output

logger = logging.getLogger(__name__)

# TODO re-enable when copyright package is split
# @click.command(name='check-copyright-comment', help='Check that each git tracked source file in the current directory contains a copyright statement.')
# @click.option('--reference', '-r', help='commit-ish to use as reference to only check changed file')
# @click.option('--porcelain', is_flag=True, help='only print the list of files w/o copyright')
# @click.option('-s', 'separator', flag_value='\n', default=True, help='paths are separated with \\n character')
# @click.option('-z', 'separator', flag_value='\x00', help='when using --porcelain, paths are separated with NUL character')
# @click.option('--inverted', is_flag=True, help='list files w/ copyright, instead of w/o (Default)')
# @click.option('--exclude', '-x', multiple=True, help='Regex of filenames that should be ignored')
# @click.option('-v', '--verbose', count=True)
# def check_copyright_comment_command(reference, porcelain, separator, inverted, exclude, verbose):
#     set_up_logging(verbose)
#     check_copyright(reference, porcelain, separator, inverted, exclude)


def check_copyright(reference=None, porcelain=False, separator='\n', inverted=False, exclude=[]):
    logger.debug('called \'lb-dev check-copyright-comment\' with \
    referense: {}, porcelain: {}, separator: {}, inverted: {}, exclude: {}'
                 .format(reference, porcelain, separator, inverted, exclude))

    logger.info('checking for copyright statements in files')
    print('checking for copyright statements in files')

    potential_files = get_potential_files(reference, exclude)

    matching_files = get_matching_files(potential_files, inverted)

    if matching_files:
        matching_files.sort()
        if not porcelain:
            report(matching_files, inverted, reference)
        else:
            print(separator.join(matching_files), end=separator)
        return 1
    return 0


def get_potential_files(reference, exclude):
    logging.info('getting the potential files')
    return [
        path for path in get_files(reference) if not FileUtils.is_empty(path)
        and not any(pattern.search(path) for pattern in map(re.compile, exclude))
    ]


def get_matching_files(potential_files, inverted):
    logger.info('filtering out non-matching files')
    if inverted:
        matching_files = list(filter(lambda path: FileUtils.has_pattern(path, license_constants.COPYRIGHT_SIGNATURE), potential_files))
    else:
        print('yolo')
        matching_files = list(
            filter(lambda path: not FileUtils.has_pattern(path, license_constants.COPYRIGHT_SIGNATURE), potential_files))

    return matching_files


def get_files(reference=None):
    '''
    Return iterable with the list of names of files to check.
    '''
    files_tracked_in_repo = get_all_files_tracked_in_repo(reference)

    files_to_check = set(filter(lambda path: FileUtils.to_check(path, license_constants.CHECKED_FILES), files_tracked_in_repo))

    logger.debug('files to check: {}'.format(files_to_check))

    return files_to_check


def get_all_files_tracked_in_repo(reference):
    
    logger.info('getting all files where copyright is applicable')
    logger.debug('reference: {}'.format(reference))
    if reference is None:
        files_in_repo = (path.decode() for path in check_output(
            ['git', 'ls-files', '-z']).rstrip(b'\x00').split(b'\x00'))
    else:
        prefix_len = len(
            check_output(['git', 'rev-parse', '--show-prefix']).strip())
        files_in_repo = (path[prefix_len:].decode() for path in check_output([
            'git', 'diff', '--name-only', '--no-renames', '--diff-filter=MA',
            '-z', reference
        ]).rstrip(b'\x00').split(b'\x00'))

    return files_in_repo


def report(filenames, inverted=False, target=None):
    '''
    Print a report with the list of filenames.

    If porcelain is True, print only the names without descriptive message.
    '''
    report_message = 'The following {} files {}contain a copyright statement:\n- '.format(
        len(filenames), '' if inverted else 'do not ')
    logger.info('The following {} files {}contain a copyright statement:\n- '.format(
        len(filenames), '' if inverted else 'do not '))

    filenames_list = '\n- '.join(filenames)
    fix_message = ''
    if not inverted:
        if target:
            fix_message = '\nYou can fix the {} files without copyright statement with:\n\n$ lb-check-copyright --porcelain {} | xargs -r lb-dev add-copyright\n'.format(
                len(filenames), target)
        else:
            fix_message = '\n\nyou can fix them with the command lb-dev add-copyright\n'
    final_message = ''.join([report_message, filenames_list, fix_message])
    print(final_message)
    return final_message
