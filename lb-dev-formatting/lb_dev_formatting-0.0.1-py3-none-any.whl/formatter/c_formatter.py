from lb_dev_formatting import constants
from lb_utils.file_utils import FileUtils
from lb_utils.shell_utils import ShellUtils
import logging
from pyOptional import Optional
import os
import sys

log = logging.getLogger(__name__)


class CFormatter:

    clang_format_commands = [
        'clang-format-{}', 'lcg-clang-format-{}', 'lcg-clang-format-{}.0',
        'lcg-clang-format-{}.0.0'
    ]

    def __init__(self, clang_version):
        self.clang_version = clang_version
        self.is_clang_format_available = None
        self.clang_format_command = ''
        self.check_if_format_command_is_available()
        log.debug(
            'c formatter initialized with clang-format version: {}. Is formatting command available: {}'
            .format(self.clang_version, self.is_clang_format_available))

    def check_if_format_command_is_available(self):
        possible_clang_format_commands = [
            command.format(self.clang_version)
            for command in self.clang_format_commands
        ]
        self.clang_format_command = self.find_command(
            possible_clang_format_commands)
        if not self.clang_format_command:
            self.is_clang_format_available = False
            log.debug('No clang format found for version {}'.format(
                self.clang_version))
        else:
            self.is_clang_format_available = True

    def format_file(self, file):
        if self.is_clang_format_available:
            log.debug('formatting file: {}'.format(file))
            with open(file, 'rb') as f:
                before = f.read()
                if FileUtils.is_empty(file):
                    log.info('file is empty')
                    output = Optional(b'')
                else:
                    output = self.apply_formating(
                        before,
                        file,
                    )

                if output.is_present():
                    after = output.get()

                return Optional({'before': before, 'after': after})
        else:
            log.error('c formatter is not available, skipping file')
            return Optional.empty()

    def find_command(self, names):
        from whichcraft import which
        try:
            return next(path for path in (which(name) for name in names)
                        if path)
        except StopIteration:
            return None

    def apply_formating(self, input, path, retry=True):
        '''
        Apply formatting rules to a file.

        :param input: content of the file to format
        :param path: name of the file
        :param retry: boolean flag to tell if we have to retry the formatting
                      with a slightly modified name (see
                      https://gitlab.cern.ch/lhcb-core/LbDevTools/issues/20)

        :return: modified file, exception in case of problems
        '''
        import logging
        from subprocess import CalledProcessError
        path = os.path.join(constants.DATA_DIR, 'default.clang-format')
        FileUtils.ensure_file_exists_in_repository(
            path, '.clang-format',
            open('{}/default.clang-format'.format(constants.DATA_DIR)))

        try:
            formatting_command = [
                self.clang_format_command, '-style=file',
                '-fallback-style=none', '-assume-filename=' + path
            ]
            log.debug('formatting command is: {}'.format(formatting_command))
            return Optional(ShellUtils.run_in_shell(formatting_command, input))

        except CalledProcessError:
            if path.endswith('.h') and retry:
                # this is a workaround for cases where clang-format does
                # not correctly detect the language
                try:
                    alias = path + 'h'
                    logging.info('retry formatting of %s as %s', path, alias)
                    return self.apply_formating(input, alias, False)
                except CalledProcessError:
                    # ignore failures in the retry
                    pass
            raise  # raise original exception

    def format_in_pipeline(self):
        FileUtils.ensure_file_exists_in_repository(
            os.getcwd(), '.clang-format',
            open(os.path.join(constants.DATA_DIR, 'default.clang-format')))
        formatting_command = [
            self.clang_format_command, '-style=file', '-fallback-style=none'
        ]
        log.debug('formatting command is: {}'.format(formatting_command))
        print(ShellUtils.run_in_shell(formatting_command,
                                      sys.stdin.read().encode()),
              end='')
