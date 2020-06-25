import warnings

import click

from . import __version__
from .run import run
from .run_tests import run_mock, run_tests


@click.group(name="engine")
@click.version_option(version=__version__, prog_name="nomnomdata-engine")
def cli():
    """NomNomData Engine CLI, used for the execution of engines"""
    warnings.warn(
        "nnd engine cli is deprecated, please use new python models", DeprecationWarning,
    )


@cli.command()
def test():
    """Run unittests for the nomnomdata-engine module"""
    pass


cli.add_command(run)
cli.add_command(run_tests)
cli.add_command(run_mock)
