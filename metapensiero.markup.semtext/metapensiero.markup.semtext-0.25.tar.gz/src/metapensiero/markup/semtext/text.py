# -*- coding: utf-8 -*-
# :Project:   metapensiero.markup.semtext -- Text parser
# :Created:   sab 01 apr 2017 13:18:38 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2017 Arstecnica s.r.l.
# :Copyright: © 2018, 2019, 2020 Lele Gaifax
#

from .ast import Paragraph, Span, Text
from .exc import UnparsableError
from .lexer import Lexer, SemError
from .parser import Parser


def parse_text(text, parse_as_plain_text_on_errors=False):
    "Parse `text` and return a :class:`.ast.Text` with the equivalent *AST*."

    if not text.strip():
        return Text([])

    lexer = Lexer()
    parser = Parser()

    try:
        parsed = parser.parse(lexer.tokenize(text.strip()))
    except SemError as e:  # pragma: nocover
        if parse_as_plain_text_on_errors:
            return Text([Paragraph([Span(p)]) for p in text.strip().split('\n\n')])
        else:
            raise UnparsableError(e.message, text) from None

    if parser.errors:
        if parse_as_plain_text_on_errors:
            return Text([Paragraph([Span(p)]) for p in text.strip().split('\n\n')])
        else:
            token = parser.errors[0]
            lineno = getattr(token, 'lineno', 0)
            column = lexer._column(text, token.index)
            msg = 'token "%s" at line %d column %d' % (token.type, lineno, column)
            raise UnparsableError('Could not parse SEM text: %s' % msg, text)

    return parsed
