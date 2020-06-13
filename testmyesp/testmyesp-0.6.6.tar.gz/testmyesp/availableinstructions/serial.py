
import codecs
import re
import time

from colibris import schemas
from colibris import settings

from testmyesp import schemafields
from testmyesp.instructions import BaseInstruction, register_instruction, InstructionException


class UnexpectedContent(InstructionException):
    def __init__(self, expected_content, received_content):
        self.expected_content = expected_content
        self.received_content = received_content

    def __str__(self):
        if not isinstance(self.expected_content, bytes) or not isinstance(self.received_content, bytes):
            return 'unexpected content'

        try:
            expected_content = self.expected_content.decode().replace('\n', '\\n').replace('\r', '\\r')
            received_content = self.received_content.decode().replace('\n', '\\n').replace('\r', '\\r')
            return 'expected content "{expected}", got "{received}"'.format(expected=expected_content,
                                                                            received=received_content)

        except UnicodeDecodeError:
            content_hex = codecs.encode(self.expected_content, 'hex').upper()
            expected_content_hex = b' '.join([content_hex[2 * i:2 * i + 2] for i in range(len(content_hex) // 2)])
            expected_content_hex = expected_content_hex.decode()

            content_hex = codecs.encode(self.received_content, 'hex').upper()
            received_content_hex = b' '.join([content_hex[2 * i:2 * i + 2] for i in range(len(content_hex) // 2)])
            received_content_hex = received_content_hex.decode()

            return 'expected content hex "{expected}", got "{received}"'.format(expected=expected_content_hex,
                                                                                received=received_content_hex)


class UnexpectedContentRegex(InstructionException):
    def __init__(self, expected_content_regex, received_content):
        self.expected_content_regex = expected_content_regex
        self.received_content = received_content

    def __str__(self):
        try:
            expected_content_regex = self.expected_content_regex.decode().replace('\n', '\\n').replace('\r', '\\r')
            received_content = self.received_content.decode().replace('\n', '\\n').replace('\r', '\\r')
            msg = 'received content "{received}" does not match regex "{regex}"'
            return msg.format(received=received_content, regex=expected_content_regex)

        except UnicodeDecodeError:
            content_hex = codecs.encode(self.expected_content_regex, 'hex').upper()
            expected_content_hex = b' '.join([content_hex[2 * i:2 * i + 2] for i in range(len(content_hex) // 2)])
            expected_content_hex = expected_content_hex.decode()

            content_hex = codecs.encode(self.received_content, 'hex').upper()
            received_content_hex = b' '.join([content_hex[2 * i:2 * i + 2] for i in range(len(content_hex) // 2)])
            received_content_hex = received_content_hex.decode()

            return 'expected content hex "{expected}", got "{received}"'.format(expected=expected_content_hex,
                                                                                received=received_content_hex)


@register_instruction
class ResetSerialLog(BaseInstruction):
    NAME = 'reset-serial-log'

    DEF_WAIT_DURATION = 500

    def __init__(self, wait_duration=DEF_WAIT_DURATION):
        self.wait_duration = wait_duration

        super().__init__()

    def execute(self):
        time.sleep(self.wait_duration / 1000.0)
        self.test_case.reset_instruction_serial_log()

    class Schema(schemas.Schema):
        wait_duration = schemas.fields.Integer(validate=schemas.validate.Range(0, settings.MAX_JOB_TIME * 1000))


@register_instruction
class CheckSerial(BaseInstruction):
    NAME = 'check-serial'

    DEF_WAIT_DURATION = 500

    CONTENT_WILDCARD_NONE = None
    CONTENT_WILDCARD_STARTS = 'start'
    CONTENT_WILDCARD_ENDS = 'end'
    CONTENT_WILDCARD_CONTAINS = 'contains'

    def __init__(self, wait_duration=DEF_WAIT_DURATION,
                 expected_content=None, expected_content_bytes=None, expected_content_hex=None,
                 expected_content_regex=None):

        self.wait_duration = wait_duration
        self.expected_content_wildcard = self.CONTENT_WILDCARD_NONE

        if expected_content is not None:
            self.expected_content = expected_content.encode()

        elif expected_content_bytes is not None:
            self.expected_content = expected_content_bytes

        elif expected_content_hex is not None:
            expected_content_hex = re.sub('[^a-fA-F0-9*]', '', expected_content_hex)
            if expected_content_hex.startswith('*'):
                if expected_content_hex.endswith('*'):
                    self.expected_content_wildcard = self.CONTENT_WILDCARD_CONTAINS

                else:
                    self.expected_content_wildcard = self.CONTENT_WILDCARD_ENDS

            elif expected_content_hex.endswith('*'):
                self.expected_content_wildcard = self.CONTENT_WILDCARD_STARTS

            expected_content_hex = expected_content_hex.strip('*')
            self.expected_content = codecs.decode(expected_content_hex, 'hex')

        else:
            self.expected_content = None

        if expected_content_regex is not None:
            self.expected_content_regex = expected_content_regex.encode()

        else:
            self.expected_content_regex = None

        super().__init__()

    def execute(self):
        # sleep in small slices so that we can read serial data, preventing serial input buffer overflow
        for i in range(self.wait_duration // 100):
            time.sleep(0.1)
            self.test_case.get_instruction_serial_log()

        data = self.test_case.get_instruction_serial_log()

        # reset instruction serial log with each check
        self.test_case.reset_instruction_serial_log()

        if self.expected_content is not None:
            if self.expected_content_wildcard == self.CONTENT_WILDCARD_STARTS:
                if not data.startswith(self.expected_content):
                    raise UnexpectedContent(self.expected_content, data)

            elif self.expected_content_wildcard == self.CONTENT_WILDCARD_ENDS:
                if not data.endswith(self.expected_content):
                    raise UnexpectedContent(self.expected_content, data)

            elif self.expected_content_wildcard == self.CONTENT_WILDCARD_CONTAINS:
                if not data.contains(self.expected_content):
                    raise UnexpectedContent(self.expected_content, data)

            else:
                if data != self.expected_content:
                    raise UnexpectedContent(self.expected_content, data)

        if self.expected_content_regex is not None:
            if not re.match(self.expected_content_regex, data, re.MULTILINE | re.DOTALL):
                raise UnexpectedContentRegex(self.expected_content_regex, received_content=data)

    class Schema(schemas.Schema):
        wait_duration = schemas.fields.Integer(validate=schemas.validate.Range(0, settings.MAX_JOB_TIME * 1000))

        expected_content = schemas.fields.String(validate=schemas.validate.Length(min=0, max=65536))
        expected_content_bytes = schemafields.Base64Field()
        expected_content_hex = schemas.fields.String(validate=schemas.validate.Length(min=0, max=65536))
        expected_content_regex = schemas.fields.String(validate=schemas.validate.Length(min=1, max=65536))


@register_instruction
class WriteSerial(BaseInstruction):
    NAME = 'write-serial'

    def __init__(self, content=None, content_bytes=None, content_hex=None):
        if content is not None:
            self.content = content.encode()

        elif content_bytes is not None:
            self.content = content_bytes

        elif content_hex is not None:
            content_hex = re.sub('[^a-fA-F0-9]', '', content_hex)
            self.content = codecs.decode(content_hex, 'hex')

        else:
            self.content = b''

        super().__init__()

    def execute(self):
        content_str = None
        try:
            content_str = self.content.decode().replace('\n', '\\n').replace('\r', '\\r')

        except UnicodeDecodeError:
            pass

        if content_str is not None:
            self.logger.debug('writing "%s"', content_str)

        else:
            self.logger.debug('writing %d bytes', len(self.content))  # TODO could be printed as hex

        self.serial.write(self.content)

    class Schema(schemas.Schema):
        content = schemas.fields.String(validate=schemas.validate.Length(min=0, max=65536))
        content_bytes = schemafields.Base64Field()
        content_hex = schemas.fields.String(validate=schemas.validate.Length(min=0, max=65536))
