from lb_dev_formatting.formatter.python_formatter import PythonFormatter
from lb_dev_formatting.formatter.c_formatter import CFormatter
from lb_dev_formatting import constants
from lb_utils.file_utils import FileUtils

from pyOptional import Optional
import logging

log = logging.getLogger(__name__)


class FormatterFacade:
    def __init__(self,
                 yapf_version=constants.YAPF_VERSION,
                 clang_version=constants.CLANG_FORMAT_VERSION,
                 shouldReturnDiff=False,
                 shouldOverwrite=True):
        log.debug(
            'FormatterFacade initialized with yapf version: {}, clang format version {}, shouldReturnDiff {} and shouldOverwrite {}'
            .format(yapf_version, clang_version, shouldReturnDiff,
                    shouldOverwrite))
        self.python_formatter = PythonFormatter(yapf_version)
        self.c_formatter = CFormatter(clang_version)
        self.shouldOverwrite = shouldOverwrite
        self.shouldReturnDiff = shouldReturnDiff
        self.files_formatted = 0

    def format_file(self, file_path):
        log.debug('formatting file {}'.format(file_path))
        formatter = self.get_appropriate_formatter(file_path)
        if formatter is None:
            log.error('No appropriate formatter for {}'.format(file_path))
            return Optional.empty()
        else:
            result = formatter.format_file(file_path)

            return self.handle_formatting_result(result, file_path)

    def handle_formatting_result(self, result, file_path):
        if result.is_present():
            log.info('result is present')
            
            diff = result.get()
            before = diff['before']
            after = diff['after']

            need_to_apply_formatting = after != before

            if need_to_apply_formatting:
                self.files_formatted += 1

                if self.shouldReturnDiff:
                    log.info('returning result as is')
                    return result

                log.info('file does not comply with formatting rules')
                if self.shouldOverwrite:
                    log.info('overwriting file')
                    log.info('%s changed', file_path)
                    FileUtils.write_to_file(file_path, after)
                else:
                    print(file_path, 'should be changed')

        return result

    def format_in_pipeline(self, file_type):
        formatter = self.get_appropriate_formatter_by_file_extension(file_type)

        formatter.format_in_pipeline()

    def get_appropriate_formatter_by_file_extension(self, file_extension):
        log.info('choosing appropriate formatter by file extension')
        if 'c' == file_extension:
            formatter = self.c_formatter
        elif 'py' == file_extension:
            formatter = self.python_formatter
        else:
            formatter = None
            print('invalid extension {}'.format(file_extension))

        return formatter

    def get_appropriate_formatter(self, file_path):
        log.info('choosing appropriate formatter')
        if 'c' == FileUtils.get_language_family(file_path):
            formatter = self.c_formatter
        elif 'py' == FileUtils.get_language_family(file_path):
            formatter = self.python_formatter
        else:
            formatter = None
            print('invalid file: {}'.format(file_path))

        return formatter
