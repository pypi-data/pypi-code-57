import regex


def clean_regex(verbose_regex: str) -> str:
    """Cleans a verbose regex pattern with comments and newlines and returns the basic pattern of the regex.

    Arguments:
        verbose_regex (str) -- The verbose regex pattern that is to be cleaned.

    Returns:
        str -- The regex pattern without any comments or whitespaces.
    """
    comment_pattern = regex.compile(
        r"""
            \# # Every comment starts with a # symbol.
            .* # Match every character after the #.
            \n # The newline is the end of the comment.
        """,
        regex.VERBOSE,
    )
    # Remove all comments from the pattern.
    cleaned_pattern = regex.sub(comment_pattern, "", verbose_regex)
    # Now remove all whitespace leftover.
    cleaned_pattern = regex.sub(r"\s", "", cleaned_pattern)
    return cleaned_pattern
