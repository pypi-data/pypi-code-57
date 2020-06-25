from textwrap import indent

from datainventory.core import Manifest
from datainventory.formats import ascii


def render(table: Manifest) -> str:
    return indent(ascii.render(table), '    ') + '\n    '
