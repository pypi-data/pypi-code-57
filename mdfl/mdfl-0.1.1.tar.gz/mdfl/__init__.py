"""
Command-line tool for parsing MDFL.

Usage:
    mdfl <script>
    mdfl -h | --help
    mdfl --version
"""

__version__ = '0.1.1'

from pathlib import Path

from docopt import docopt

from mdfl.parser import create_pack, parser


def main() -> None:
    """Entry point for the command line interface."""
    arguments = docopt(__doc__, version=f'mdfl {__version__}')
    script = Path(arguments.get('<script>'))
    with script.open() as file:
        contents = file.read()
    syntax_tree = parser.parse(contents)
    create_pack(syntax_tree, pack_name=script.stem)
