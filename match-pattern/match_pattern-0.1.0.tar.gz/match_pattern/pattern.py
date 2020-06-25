import os
import re
from typing import Union, List


def qoute_non_regex_chars(txt: str) -> str:
    """Quotes any non regex chars for regex.
    Based on: http://kevin.vanzonneveld.net
    """
    assert isinstance(txt, str), ValueError("txt must be a string")

    return re.sub(r"([.\\+*?\[\^\]$(){}=!<>|:-])", r"\\\1", txt)


def glob_string_to_regex_string(txt: str, is_full_match: bool = True):
    """Convert a glob string to a regex string.

    Args:
        txt (str): The glob string
        is_full_match ([type], optional): If true will augment the pattern with ^....$, to make sure only
                full string matches are captured. Defaults to True.

    Returns:
        str: The regex pattern.
    """
    as_regex = qoute_non_regex_chars(txt)
    as_regex = re.sub(r"\\\*", ".*", as_regex)
    as_regex = re.sub(r"\\\?", ".", as_regex)
    if is_full_match:
        if not as_regex.startswith("^"):
            as_regex = r"^" + as_regex
        if not as_regex.endswith("$"):
            as_regex = as_regex + "$"
    return as_regex


def glob_string_to_regex(txt: str, is_full_match: bool = True, flags: Union[re.RegexFlag, int] = re.MULTILINE):
    """Convert a glob string to a regex object (re.Pattern)

    Args:
        txt (str): The glob string
        is_full_match ([type], optional): If true will augment the pattern with ^....$, to make sure only
                full string matches are captured. Defaults to True.
        flags (Union[re.RegexFlag, int], optional): The regex flags to use. Defaults to re.MULTILINE.

    Returns:
        re.Pattern: The regex pattern.
    """
    return re.compile(glob_string_to_regex_string(txt, is_full_match=is_full_match), flags=flags)


class Pattern(object):
    def __init__(
        self, pattern, flags: Union[re.RegexFlag, int] = re.MULTILINE, is_full_match=True,
    ):
        """Create a pattern object that can match and test a glob or regex pattern against a string value.

        Args:
            pattern (str|Pattern): The pattern source, can be either a glob or regex.
            flags (Union[re.RegexFlag, int], optional): The regex flags to use. Defaults to re.MULTILINE.
            is_full_match ([type], optional): If true will augment the pattern with ^....$, to make sure only
                full string matches are captured. Defaults to True.
        """
        super().__init__()
        self.flags = flags

        assert self.__validate_pattern_input(pattern), ValueError("pattern must be a string or a Pattern")

        if not isinstance(pattern, list):
            pattern = [pattern]
        pattern = [str(p) for p in pattern]

        self.matcher = self._parse_pattern_regex(pattern, flags=flags, is_full_match=is_full_match)

    @classmethod
    def __validate_pattern_input(cls, pattern):
        if isinstance(pattern, list):
            return all(cls.__validate_pattern_input(v) for v in pattern)
        return isinstance(pattern, (str, Pattern))

    @classmethod
    def _is_regular_expression(cls, txt: str):
        """Returns true if this pattern text is a regular expression.

        Args:
            txt (str): The string to evaluate.

        Returns:
            bool: If true this should be parsed as a regex pattern.
        """
        return txt.startswith("re::")

    @classmethod
    def _parse_pattern_regex(
        cls, pattern: List[str], flags: Union[re.RegexFlag, int] = re.MULTILINE, is_full_match: bool = True,
    ):
        """Parses a glob pattern string or a pattern string array into a single regex.

        Args:
            pattern (str|List[str]): A pattern or a list of patterns to match.
            flags (Union[re.RegexFlag, int], optional): Regex flags to use. Defaults to re.MULTILINE.
            is_full_match (bool, optional): If true will augment the pattern with ^....$, to make sure only
                full string matches are captured. Defaults to True.

        Returns:
            re.Pattern: A regex pattern.
        """

        assert isinstance(pattern, list) and all(isinstance(p, str) for p in pattern)

        pattern_parts = []
        for p in pattern:
            if not cls._is_regular_expression(p):
                pattern_parts += p.split("|")
            else:
                pattern_parts.append(p)

        def parse_pattern_part_to_regex_string(txt: str) -> str:
            if cls._is_regular_expression(txt):
                return txt[4:]
            else:
                return glob_string_to_regex_string(txt, is_full_match=is_full_match)

        as_regex_strings = [parse_pattern_part_to_regex_string(v) for v in pattern_parts]

        as_regex = "|".join(as_regex_strings)
        as_regex = re.compile(as_regex, flags)

        return as_regex

    def test(pattern, val: str):
        """Test a pattern, true if matches.

        Arguments:
            pattern {str|Pattern} -- The pattern to test
            val {str} -- The string to test against

        Returns:
            bool -- True if matches
        """
        if not isinstance(pattern, Pattern):
            pattern = Pattern(pattern)

        assert isinstance(val, str), ValueError("Val must be a string")
        return pattern.matcher.match(val) is not None

    def match(pattern, val: str):
        """Match a pattern

        Arguments:
            pattern {str|Pattern} -- The pattern
            val {str} -- The string to test against

        Returns:
            str -- The matched value.
        """
        if not isinstance(pattern, Pattern):
            pattern = Pattern(pattern)

        assert isinstance(val, str), ValueError("Val must be a string")

        return pattern.matcher.match(val) is not None

    def find_all(pattern, val: str):
        """Match all occurrences of a pattern

        Arguments:
            pattern {str|Pattern} -- The pattern
            val {str} -- The string to test against

        Returns:
            [str] -- The matched values.
        """
        if not isinstance(pattern, Pattern):
            pattern = Pattern(pattern)

        assert isinstance(val, str), ValueError("Val must be a string")

        return pattern.matcher.findall(val) is not None

    def replace(pattern, replace_with, val: str):
        """Replace all occurances of a pattern within the value.

        Args:
            pattern (Patter|str): A pattern string or a pattern object.
            replace_with (str|Callable): The string/method to replace with, see, re.sub.
            val (str): The value to search within.

        Returns:
            str: The augmented string
        """
        if not isinstance(pattern, Pattern):
            pattern = Pattern(pattern, is_full_match=False)

        return re.sub(pattern.matcher, replace_with, val)

    def scan_path(pattern, src_path, include_directories: bool = True, include_files: bool = True) -> List[str]:
        """Scans a folder path and subpaths for the file/folder paths that match the pattern.
        A filepath match would include relative subpaths.

        Args:
            pattern (str|Pattern): The pattern to match.
            src_path (str): The root folder for the search.
            include_directories (bool, optional): If true include directories in result. Defaults to True.
            include_files (bool, optional): If true include files in the results. Defaults to True.

        Returns:
            List[str]: Matched abs paths.
        """
        assert os.path.exists(src_path), ValueError(f"Path dose not exist: {src_path}")

        if not isinstance(pattern, Pattern):
            pattern = Pattern(pattern)

        matched = []
        for dirpath, dirnames, filenames in os.walk(src_path):
            relative_dirname = os.path.relpath(dirpath, src_path)
            to_match = []
            if include_directories:
                to_match += dirnames
            if include_files:
                to_match += filenames
            for name in to_match:
                fpath = os.path.join(relative_dirname, name).strip(os.sep)
                if pattern.test(fpath):
                    matched.append(os.path.join(dirpath, name))

        return matched

    @classmethod
    def format(
        cls, val: str, custom_start_pattern: str = "{{", custom_end_pattern: str = "}}", **kwargs,
    ):
        """Custom format using patterns. Allows for an alternate python style string format
        with a custom start token and end token.

        Args:
            val (str): The value to format.
            custom_start_pattern (str, optional): The start token to match. Defaults to "{{".
            custom_end_pattern (str, optional): The end token to match. Defaults to "}}".

        NOTE:
            There are three custom internal arguments which will not be allowed in the format list,
            1. val
            2. custom_start_pattern
            3. custom_end_pattern
        """

        def custom_replace_with(val: str):
            key = (val[1] or "").strip()
            if key in kwargs:
                return kwargs[val[1]]
            raise Exception("Predict value not found in values dictionary: " + key)

        pattern_start_regex = Pattern(custom_start_pattern, is_full_match=False).matcher.pattern
        pattern_end_regex = Pattern(custom_end_pattern, is_full_match=False).matcher.pattern
        replace_pattern = pattern_start_regex + "(.*)" + pattern_end_regex

        return Pattern("re::" + replace_pattern).replace(custom_replace_with, val)

    def __str__(self):
        return "re::" + self.matcher.pattern.__str__()

    def __repr__(self):
        return self.__str__()
