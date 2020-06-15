"""Comparison logic for tests"""
import codecs
import enum
import re

from scruf import exception

_EOL_CHARACTERS = "\n\r"
_STDOUT_FLAG = "1:"
_STDERR_FLAG = "2:"
_ESCAPE_FLAG = "[ESC]"
_NO_EOL_FLAG = "[NEoL]"
_REGEX_FLAG = "[RE]"
_RETURNCODE_REGEX = re.compile(r"\[(\d+)\]\s*$")


class ComparisonTypes(enum.Enum):
    """The possible types of comparison"""

    BASIC = enum.auto()
    ESCAPE = enum.auto()
    REGEX = enum.auto()
    NO_EOL = enum.auto()
    RETURNCODE = enum.auto()


def get_comparison_details(test_line):
    """Get details of the comparison built from a test line

    Parameters
    ----------
    test_line : str
        The test line to process

    Returns
    -------
    dict
        Details of the comparison defined by the test, contains keys:
            "type": scruf.compare.ComparisonTypes
            "content": str
                The content to be used to make the comparison, generally just the
                `test_line` with any flags stripped
            "source": str
                The expected source for the line, one of "stdout" or "stderr"
    """

    content, source = _get_source_and_content(test_line)

    if _has_regex_flag(content):
        content = _strip_flag(content, _REGEX_FLAG).rstrip(_EOL_CHARACTERS)
        return {
            "type": ComparisonTypes.REGEX,
            "content": content,
            "source": source,
        }
    elif _has_no_eol_flag(content):
        content = _strip_flag(content, _NO_EOL_FLAG).rstrip(_EOL_CHARACTERS)
        return {
            "type": ComparisonTypes.NO_EOL,
            "content": content,
            "source": source,
        }
    elif _has_returncode_flag(content):
        content = _get_returncode(content)
        return {
            "type": ComparisonTypes.RETURNCODE,
            "content": content,
            "source": "returncode",
        }
    elif _has_esc_flag(content):
        content = _get_escape_content(_strip_flag(content, _ESCAPE_FLAG))
        return {
            "type": ComparisonTypes.ESCAPE,
            "content": content,
            "source": source,
        }
    else:
        return {"content": content, "type": ComparisonTypes.BASIC, "source": source}


def get_comparer(comparison_type):
    """Get function to be used to make comparison for the given type

    Note if `comparison_type` is `scruf.compare.ComparisonTypes.REGEX`, the returned
    function will raise a `scruf.compare.RegexError` if it is run with an invalid regex.

    Parameters
    ----------
    comparison_type : scruf.compare.ComparisonTypes

    Returns
    -------
    function(expected_content, exec_result_content)
        Function that can be used to make the comparison, returning bool
    """
    return {
        ComparisonTypes.BASIC: _basic_compare,
        ComparisonTypes.ESCAPE: _basic_compare,
        ComparisonTypes.REGEX: _regex_compare,
        ComparisonTypes.NO_EOL: _no_eol_compare,
        ComparisonTypes.RETURNCODE: _returncode_compare,
    }[comparison_type]


def _get_source_and_content(line):
    if _has_stdout_flag(line):
        return _strip_flag(line, _STDOUT_FLAG), "stdout"
    if _has_stderr_flag(line):
        return _strip_flag(line, _STDERR_FLAG), "stderr"
    return line, "stdout"


class RegexError(exception.CramerError):
    def __init__(self, regex, regex_error):
        message = "Error in regex {}: {}".format(regex, str(regex_error))
        super().__init__(message)

        self.regex = regex


def _lstrip_space(line):
    if line[0] == " ":
        return line[1:]
    return line


def _strip_flag(line, flag):
    return _lstrip_space(line[len(flag) :])


def _has_stdout_flag(test_line):
    return test_line.startswith(_STDOUT_FLAG)


def _has_stderr_flag(test_line):
    return test_line.startswith(_STDERR_FLAG)


def _has_esc_flag(test_line):
    return test_line.startswith(_ESCAPE_FLAG)


def _has_regex_flag(test_line):
    return test_line.startswith(_REGEX_FLAG)


def _has_no_eol_flag(test_line):
    return test_line.startswith(_NO_EOL_FLAG)


def _has_returncode_flag(test_line):
    return _RETURNCODE_REGEX.match(test_line) is not None


def _get_escape_content(test_line):
    return codecs.decode(test_line, "unicode-escape")


def _get_returncode(test_line):
    return int(_RETURNCODE_REGEX.match(test_line).group(1))


def _basic_compare(expected_content, content):
    return content == expected_content


def _returncode_compare(expected_returncode, returncode):
    return returncode == expected_returncode


def _no_eol_compare(expected_content, content):
    return _basic_compare(expected_content.rstrip(_EOL_CHARACTERS), content)


def _build_regex(test_line):
    try:
        regex = re.compile(test_line)
    except re.error as e:
        raise RegexError(test_line, e)
    return regex


def _regex_compare(raw_regex, content):
    regex = _build_regex(raw_regex)
    return regex.search(content) is not None
