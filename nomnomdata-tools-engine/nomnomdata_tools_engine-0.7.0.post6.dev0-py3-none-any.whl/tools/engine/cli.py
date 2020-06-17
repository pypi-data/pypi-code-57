import click

from nomnomdata.tools.engine import create_new, engine_build, engine_deploy, model_update

from . import __version__


@click.group(name="engine-tools")
@click.version_option(version=__version__, prog_name="nomnomdata-engine-tools")
def cli():
    """Used for building/deploying engines"""


@cli.command()
def test():
    """Run unittests for nomnomdata engine tools"""
    import pytest

    pytest.main(["--pyargs", "nomnomdata.tools.engine"])


cli.add_command(create_new.create_new)
cli.add_command(engine_build.engine_build)
cli.add_command(engine_deploy.deploy)
cli.add_command(model_update.model_update)
