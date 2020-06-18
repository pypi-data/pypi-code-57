"""Directive for highlighting placeholder variables.

This module defines a new directive ``.. samp::``, which behaves like
the builtin inline ``:samp:`` role, but for blocks.

:copyright: Copyright 2020, Kai Welke.
:license: MIT, see LICENSE for details
"""

try:
    from importlib.metadata import version, PackageNotFoundError  # type: ignore
except ImportError:  # pragma: nocover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore

from typing import Any, Dict, List

from docutils import nodes
from docutils.nodes import Node
import pygments
from pygments.lexer import bygroups, RegexLexer
from pygments.token import Generic, Text  # noqa: F401
from sphinx.application import Sphinx
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

logger = logging.getLogger(__name__)

try:
    __version__ = version(__name__.replace(".", "-"))
except PackageNotFoundError:  # pragma: nocover
    __version__ = "unknown"


class SampLexer(RegexLexer):
    """Lexer for parsing the code blocks.

    The lexer starts at the beginning of the string and tries to match the first
    pattern. If that does not match, try the second pattern, and so on. If the current
    character can't be matched to anything, return it as an error token.

    1) Check if the first character is a prompt character (followed by a whitespace)
    2) Check, if we have escaped curly braces. Everything is regular text.
    3) Check, if we have a ``{PLACEHOLDER}`` pattern.
    4) Check if it's text. Match all characters that are not the opening brace
       or newline.
    5) The opening curly brace and the newline character on their own are text too.
       (otherwise this would return an error token and prompts on multiple lines would
       not be parsed correctly.
    """

    tokens = {
        "root": [
            (r"^[$#~]\s", Generic.Prompt),
            (r"\\{.+?\\?}?", Text),
            (
                r"({)(.+?)(})",
                bygroups(Generic.Punctuation, Generic.Emph, Generic.Punctuation),
            ),
            (r"[^{\n]+", Text),
            (r"[{\n]", Text),
        ]
    }


class SampDirective(SphinxDirective):
    """Directive for literal block with empasis.

    Anything in '{}' becomes an emphasized node and can be styled separately from the
    surrounding literal text (e.g. typewriter *and* italic).
    """

    has_content = True

    def run(self) -> List[Node]:
        """Create a literal block and parse the children."""
        code = "\n".join(self.content)
        children = self.parse(code)
        node = nodes.literal_block(code, "", *children)

        self.add_name(node)
        return [node]

    def parse(self, content: str) -> List[Node]:
        """Parse a literal code block.

        Use an instance of SampLexer() to lex the literal block
        into a list of tokens and parse it into docutils nodes.
        """
        result = []

        for token_type, token in pygments.lex(content, SampLexer()):
            logger.debug(f"TOK: {token} of {token_type}")
            if token_type == Generic.Prompt:
                result.append(nodes.inline(token, token, classes=["gp"]))
            elif token_type == Generic.Emph:
                result.append(nodes.emphasis(token, token, classes=["var"]))
            elif token_type == Generic.Punctuation:
                # don't carry over the curly braces
                continue
            else:
                result.append(nodes.Text(token, token))

        return result


def setup(app: "Sphinx") -> Dict[str, Any]:
    """Register the directive."""
    app.add_directive("samp", SampDirective)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
