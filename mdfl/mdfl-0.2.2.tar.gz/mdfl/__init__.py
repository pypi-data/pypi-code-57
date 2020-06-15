"""
PyMDFL: A command-line tool for parsing MDFL and generating Data Packs.

Usage:
    mdfl <script> [--output=<path>]
    mdfl <script> [--tree]
    mdfl -h | --help
    mdfl -V | --version

Options:
    -h --help        Show this screen.
    -V --version     Show version.
    --output=<path>  Output path for the datapack.
    --tree           Print a syntax tree without compiling.
"""

__version__ = "0.2.2"

from pathlib import Path

from docopt import docopt

from mdfl.parser import create_pack, parser


def main() -> None:
    """Entry point for the command line interface."""
    arguments = docopt(__doc__, version=f"mdfl {__version__}")
    script = Path(arguments.get("<script>"))
    with script.open() as file:
        contents = file.read()
    syntax_tree = parser.parse(contents)
    if not arguments.get("--tree"):
        create_pack(
            syntax_tree,
            pack_name=script.stem,
            path=arguments.get("--output")
        )
    else:
        print(syntax_tree.pretty())
