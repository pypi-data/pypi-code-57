from lb_dev_formatting import constants
from lb_utils.shell_utils import ShellUtils
from lb_utils.file_utils import FileUtils

from pyOptional import Optional
import logging
from subprocess import check_output
import sys

log = logging.getLogger(__name__)


class PythonFormatter:
    def __init__(self, yapf_version):
        self.yapf_version = yapf_version
        self.is_yapf_available = None
        self.check_if_format_command_is_available()
        log.debug(
            'python formatter initialized with yapf version: {}. Is formatting command available: {}'
            .format(self.yapf_version, self.is_yapf_available))

    def check_if_format_command_is_available(self):
        log.info('looking for compatible yapf version in the system')
        yapf_command = ShellUtils.find_command(['yapf'])
        yapf_version = None

        if yapf_command:
            yapf_version = check_output([yapf_command,
                                     '--version']).split()[-1].decode()
        log.debug('system yapf version: {}. Self yapf version: {}'.format(
            yapf_version, self.yapf_version))
        if yapf_version != self.yapf_version:
            log.error('no yapf version {} found in the system'.format(
                self.yapf_version))
            print('Error: no yapf version {} found in the system'.format(
                self.yapf_version))
            self.is_yapf_available = False
        else:
            self.is_yapf_available = True

    def format_file(self, file):
        if self.is_yapf_available:
            log.debug('formatting file: {}'.format(file))
            with open(file, 'rb') as f:
                before = f.read()
                if FileUtils.is_empty(file):
                    log.info('file is empty')
                    output = Optional(b'')
                else:
                    output = Optional(ShellUtils.run_in_shell(['yapf'],
                                                              before))
                if output.is_present():
                    after = output.get()

                return Optional({'before': before, 'after': after})
        else:
            log.error('python formatter is not available, skipping file')
        return Optional.empty()

    def format_in_pipeline(self):
        print(ShellUtils.run_in_shell(['yapf'],
                                      sys.stdin.read().encode()),
              end='')
