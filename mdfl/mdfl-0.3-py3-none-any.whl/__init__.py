"""
PyMDFL: A command-line tool for parsing MDFL and generating Data Packs.

The <source> argument can be one of:
    A text file conforming to the MDFL specification
    A directory containing MDFL files

Usage:
    mdfl <source> [--output=<path>]
    mdfl <source> [--tree]
    mdfl -h | --help
    mdfl -V | --version

Options:
    -h --help        Show this screen.
    -V --version     Show version.
    --output=<path>  Output path for the datapack.
    --tree           Print a syntax tree without compiling.
"""

__version__ = "0.3"

from pathlib import Path

from docopt import docopt

from mdfl.parser import create_pack, parser


def main() -> None:
    """Entry point for the command line interface."""
    arguments = docopt(__doc__, version=f"mdfl {__version__}")

    contents = ""
    source = Path(arguments.get("<source>"))
    if source.is_dir():
        name = source.name
        for script in source.glob("*.mdfl"):
            with script.open() as file:
                contents += "\n" + file.read()
    else:
        name = source.stem
        with source.open() as file:
            contents += "\n" + file.read()
    syntax_tree = parser.parse(contents)
    if not arguments.get("--tree"):
        create_pack(
            syntax_tree,
            pack_name=name,
            source=source,
            target=arguments.get("--output")
        )
    else:
        print(syntax_tree.pretty())
