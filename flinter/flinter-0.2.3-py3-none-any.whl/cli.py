#!/usr/bin/env python
"""
cli.py

Command line interface for tools in ms_thermo
"""

import click
from flinter.struct_analysis import (struct_analysis, print_errors, print_score)
from flinter.fmt_analysis import fmt_analysis

@click.group()
def main_cli():
    """--------------------    FLINT  ---------------------

.      - Flint, because our code stinks... -


You are now using the Command line interface of Flint,
a Fortran linter created at CERFACS (https://cerfacs.fr).

This is a python package currently installed in your python environement.

"""
    pass


@click.command()
@click.argument('file', nargs=1)
def fmt(file):
    """Score the formatting of .f90 FILE.
    """
    with open(file, "r") as fin:
        lines = fin.readlines()
    fmt_analysis(lines)

main_cli.add_command(fmt)


@click.command()
@click.argument('file', nargs=1,)
def cplx(file):
    """Score the complexity of .f90 FILE.
    """
    with open(file, "r") as fin:
        st_ct = fin.read()
    info_errors = struct_analysis(st_ct)
    print_errors(info_errors)
    print_score(info_errors)
main_cli.add_command(cplx)

