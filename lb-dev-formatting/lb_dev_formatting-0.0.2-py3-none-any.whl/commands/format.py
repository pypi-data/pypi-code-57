import click
import click_plugins
import logging
import os
from subprocess import check_output, CalledProcessError
from pyOptional import Optional
from difflib import unified_diff

from lb_dev_formatting import constants
from lb_dev_formatting.exceptions.command_not_found import CommandNotFoundError
from lb_dev_formatting.exceptions.illegal_argument import IllegalArgumentError
from lb_utils.log_utils import set_up_logging
from lb_utils.file_utils import FileUtils
from lb_utils.git_utils import GitUtils
from lb_utils.shell_utils import ShellUtils
from lb_dev_formatting.formatter.formatter_facade import FormatterFacade

log = logging.getLogger(__name__)


@click.command(
    name='format',
    help='Apply formatting rules to files given (Python and C++ files)')
@click.argument('files', nargs=-1)
@click.option('--clang-format-version',
              '-c',
              default=constants.CLANG_FORMAT_VERSION,
              help='version of clang-format to use (default: {})'.format(
                  constants.CLANG_FORMAT_VERSION))
@click.option('--yapf-version',
              '-y',
              default=constants.YAPF_VERSION,
              help='version of yapf to use (default: {})'.format(
                  constants.YAPF_VERSION))
@click.option('--dry-run', '-d', is_flag=True, help='do not modify the files')
@click.option(
    '--reference',
    '-r',
    help=
    'check/format only the files select the files that have changed since the REFERENCE commit/branch'
)
@click.option('--format-patch',
              '-f',
              help='create a patch file with the changes')
@click.option('--pipe',
              '-p',
              type=click.Choice(constants.FORMATTABLE_LANGUAGES),
              help='format from stdin to stdout (allowed values: {})'.format(
                  constants.FORMATTABLE_LANGUAGES))
@click.option('-v', '--verbose', count=True)
def format_command(files, clang_format_version, yapf_version, dry_run,
                   reference, format_patch, pipe, verbose):
    set_up_logging(verbose)
    log.debug('called `format` with parameters: files={}, \
clang_format_version={}, yapf_version={}, dry_run={}, reference={}, \
format_patch={}, pipe={}'.format(files, clang_format_version, yapf_version,
                                 dry_run, reference, format_patch, pipe))
    return format_files(files, clang_format_version, yapf_version, dry_run,
                        reference, format_patch, pipe)


def format_files(files, clang_format_version, yapf_version, dry_run, reference,
                 format_patch, pipe):
    log.info('applying formatting to files')

    check_for_illegal_arguments(files, reference, format_patch, pipe)

    if not pipe and not files:
        files = FileUtils.get_files(reference)

    patch = []
    encoding_errors = []
    shouldReturnDiff = True if format_patch else False

    formatter = FormatterFacade(yapf_version, clang_format_version,
                                shouldReturnDiff, not dry_run)

    if not files:
        log.info('formatting in pipe mode')
        formatter.format_in_pipeline(pipe)
        return 0

    for file in files:
        try:
            log.debug('formatting file {}'.format(file))
            result = formatter.format_file(file)
            if result.is_present() and format_patch:
                patch = add_diff_to_patch(result.get(), file)

        except CalledProcessError as err:
            log.warning('could not format %r: %s\n%s', file, err,
                        err.output.rstrip())

        except UnicodeDecodeError as err:
            log.error('invalid encoding in %r: %s', file, err)
            encoding_errors.append(file)

    if encoding_errors:
        log.info('found encoding errors')
        inform_about_encoding_errors(encoding_errors)
        return 1

    if patch:
        log.info('creating formatting patch')
        create_formatting_patch(patch, format_patch)

    if patch or encoding_errors:
        return 1

    if dry_run and formatter.files_formatted > 0:
        return 1

    return 0


def add_diff_to_patch(diff, file):
    log.info('adding formatting differences to patch')
    patch = []
    before = diff['before']
    after = diff['after']

    patch.extend(
        line if line.endswith('\n') else (line +
                                          '\n\\ No newline at end of file\n')
        for line in unified_diff(
            before.decode('utf-8').splitlines(True),
            after.decode('utf-8').splitlines(True), os.path.join('a', file),
            os.path.join('b', file)))

    return patch


def check_for_illegal_arguments(files, reference, format_patch, pipe):
    if pipe:
        if format_patch:
            raise IllegalArgumentError(
                'incompatible options -f/--format-patch and -p/--pipe')
        elif reference:
            raise IllegalArgumentError(
                'incompatible options -r/--reference and -p/--pipe')
        elif files:
            raise IllegalArgumentError(
                'cannot process explicit files in --pipe mode')

    if reference and files:
        raise IllegalArgumentError('you cannot specify files with --reference')

    return 0


def inform_about_encoding_errors(encoding_errors):
    print('=======================================',
          ' Detected files with encoding (UTF-8) errors:',
          sep='\n')
    print('', *encoding_errors, sep='\n - ')
    print('', '=======================================', sep='\n')


def create_formatting_patch(patch, format_patch):
    from email.message import Message
    msg = Message()
    msg = add_headers_to_message(msg)

    payload = get_message_payload(patch)

    try:
        payload.encode()
        charset = None
    except UnicodeEncodeError:
        charset = 'utf-8'
    msg.set_payload(payload, charset=charset)

    if format_patch == '-':
        print(msg)
    else:
        create_patch_file(format_patch, msg)

        print('=======================================',
              ' You can fix formatting with:',
              '',
              sep='\n')
        if 'CI' in os.environ:
            print('   curl {CI_PROJECT_URL}/-/jobs/{CI_JOB_ID}/'
                  'artifacts/raw/{0} | '
                  'git am'.format(format_patch, **os.environ))
        else:
            print('   git am {}'.format(format_patch))
        print('', '=======================================', sep='\n')


def add_headers_to_message(msg):
    from email.utils import formatdate
    log.info('adding headers to message for patch')
    msg.add_header('From', 'Gitlab CI <noreply@cern.ch>')
    msg.add_header('Date', formatdate())
    msg.add_header('Subject', '[PATCH] Fixed formatting')

    return msg


def get_message_payload(patch):
    log.info('adding payload to the message for patch')
    return '\n'.join([
        'patch generated by {}'.format(
            '{CI_PROJECT_URL}/-/jobs/{CI_JOB_ID}'.format(
                **os.environ) if 'CI' in os.environ else 'standalone job'), '',
        '', ''.join(patch)
    ])


def create_patch_file(format_patch, msg):
    log.info('creating patch file')
    if (os.path.dirname(format_patch)
            and not os.path.isdir(os.path.dirname(format_patch))):
        os.makedirs(os.path.dirname(format_patch))
    with open(format_patch, 'wb') as patchfile:
        patchfile.write(bytes(msg))
