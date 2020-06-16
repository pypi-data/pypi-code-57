from os import path
from typing import Tuple

import click

from super3 import __version__
from super3 import main


def _format_path_and_lineno(
    source_file: main.SourceFile, violation: main.Violation
) -> str:
    source_path = source_file.path
    source_path = path.abspath(source_path)
    line = violation.lineno
    return f"{source_path}:{line}"


def _format_violation(source_file: main.SourceFile, violation: main.Violation) -> str:
    lines = source_file.source.splitlines()

    line = lines[violation.lineno - 1]

    formatted = []
    formatted.append(line[: violation.col_offset])
    formatted.append(
        click.style(line[violation.col_offset : violation.end_col_offset], bold=True)
    )
    formatted.append(line[violation.end_col_offset :])
    return "".join(formatted)


@click.command()
@click.version_option(version=__version__)
@click.option("--check", is_flag=True, help="Check only.")
@click.option("--list", is_flag=True, help="List all violations.")
@click.option("--list-files", is_flag=True, help="The person to greet.")
@click.argument(
    "paths",
    nargs=-1,
    type=click.Path(
        exists=True, file_okay=True, dir_okay=True, readable=True, allow_dash=True
    ),
    is_eager=True,
)
def cli(list_files: bool, list: bool, check: bool, paths: Tuple[str, ...]):

    if sum([check, list, list_files]) > 1:
        print("Only one of --check, --list and --list files should be used.")
        return

    has_violations = False

    if list_files:
        for path in paths:
            for source_file in main.read_files(path):
                has_violation = main.has_violation(source_file)
                if has_violation:
                    has_violations = True
                    print(source_file.path)
    elif list:
        for path in paths:
            for source_file in main.read_files(path):
                for v in main.list_violations(source_file):
                    has_violations = True
                    v_fmt = _format_violation(source_file, v)
                    path_lineno = _format_path_and_lineno(source_file, v)
                    print(f"{path_lineno}:{v_fmt}")
    elif check:
        for path in paths:
            for source_file in main.read_files(path):
                has_violation = main.has_violation(source_file)
                if has_violation:
                    has_violations = True
                    print(f"Would update {source_file.path}")
    else:
        for path in paths:
            for source_file in main.read_files(path):
                main.upgrade_file(source_file)

    if has_violations:
        raise click.ClickException("Oh no! 🔥")
    else:
        print("All done! 👍")


if __name__ == "__main__":
    cli()
