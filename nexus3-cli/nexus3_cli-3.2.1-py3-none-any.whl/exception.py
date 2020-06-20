import json
from click import ClickException
from enum import Enum


class CliReturnCode(Enum):
    """Error codes returned by :py:mod:`nexuscli.cli`"""
    SUCCESS = 0
    NO_FILES = 1
    API_ERROR = 2
    CONNECTION_ERROR = 3
    DOWNLOAD_ERROR = 4
    INVALID_CREDENTIALS = 5
    INVALID_SUBCOMMAND = 10
    SUBCOMMAND_ERROR = 11
    POLICY_NOT_FOUND = 20
    REPOSITORY_NOT_FOUND = 30
    CONFIG_ERROR = 40
    UNKNOWN_ERROR = 99


API_ERROR_MAP = {
    'Creating and updating scripts is disabled': {
        'class': 'ConfigError',
        'msg': (
            'Please enable scripting in your Nexus instance; see https://support.sonatype.com/hc'
            '/en-us/articles/360045220393-Scripting-Nexus-Repository-Manager-3#how-to-enable')
    },
}
"""Map from Nexus API response to an exception class and user-friendly error"""


class NexusClientBaseError(ClickException):
    exit_code = CliReturnCode.UNKNOWN_ERROR.value


def _raise_if_error_is_mapped(nexus_message_bytes):
    try:
        nexus_response = json.loads(nexus_message_bytes)
    except (TypeError, json.JSONDecodeError):
        return

    if not isinstance(nexus_response, dict):
        return

    try:
        result = nexus_response['result']
        print('RESULT IS', result)
    except KeyError:
        raise TypeError from None

    if result in API_ERROR_MAP.keys():
        raise globals()[API_ERROR_MAP[result]['class']](API_ERROR_MAP[result]['msg']) from None


class NexusClientAPIError(NexusClientBaseError):
    """Unexpected response from Nexus service."""
    exit_code = CliReturnCode.API_ERROR.value

    def __init__(self, message_bytes=None):
        super().__init__(message_bytes)
        print('message is', message_bytes)
        _raise_if_error_is_mapped(message_bytes)


class NexusClientConnectionError(NexusClientBaseError):
    """Generic network connector error."""
    exit_code = CliReturnCode.CONNECTION_ERROR.value


class NexusClientInvalidCredentials(NexusClientBaseError):
    """
    Login credentials not accepted by Nexus service. Usually the result of a
    HTTP 401 response.
    """
    exit_code = CliReturnCode.INVALID_CREDENTIALS.value


class NexusClientInvalidRepositoryPath(NexusClientBaseError):
    """
    Used when an operation against the Nexus service uses an invalid or
    non-existent path.
    """
    pass


class NexusClientInvalidRepository(NexusClientBaseError):
    """The given repository does not exist in Nexus."""
    exit_code = CliReturnCode.REPOSITORY_NOT_FOUND.value


class NexusClientInvalidCleanupPolicy(NexusClientBaseError):
    """The given cleanup policy does not exist in Nexus."""
    exit_code = CliReturnCode.SUBCOMMAND_ERROR.value


class NexusClientCreateRepositoryError(NexusClientBaseError):
    """Used when a repository creation operation in Nexus fails."""
    exit_code = CliReturnCode.SUBCOMMAND_ERROR.value


class NexusClientCreateCleanupPolicyError(NexusClientBaseError):
    """Used when a cleanup policy creation operation in Nexus fails."""
    exit_code = CliReturnCode.SUBCOMMAND_ERROR.value


class DownloadError(NexusClientBaseError):
    """Error retrieving artefact from Nexus service."""
    exit_code = CliReturnCode.DOWNLOAD_ERROR.value


class ConfigError(NexusClientBaseError):
    """Configuration error."""
    exit_code = CliReturnCode.CONFIG_ERROR.value
