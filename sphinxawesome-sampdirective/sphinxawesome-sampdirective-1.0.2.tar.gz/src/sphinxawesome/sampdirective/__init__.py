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
from pygments.lexer import RegexLexer
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
    """Improved Lexer with two states."""

    tokens = {
        "root": [
            (r"^[$#~]\s", Generic.Prompt),  # prompt characters at the beginning
            (r"[^{$#~]+", Text),  # everything except the `{` is Text
            (r"{", Generic.Punctuation, "samp"),  # `{` enter samp state
        ],
        "samp": [
            (r"[^}]+", Generic.Emph),  # everything except `}` is Emph inside
            (r"}", Generic.Punctuation, "#pop"),  # match closing `}`, exit samp state
        ],
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
