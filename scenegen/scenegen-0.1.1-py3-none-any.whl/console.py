"""CLI entrypoints"""
# pylint: disable=C0330,R0913
import logging
import sys

from pathlib import Path
import click

from scenegen import __version__
from scenegen.testscene import TestScene


LOGGER = logging.getLogger(__name__)


@click.command()
@click.version_option(version=__version__)
@click.option("-l", "--loglevel", help="Python log level, 10=DEBUG, 20=INFO, 30=WARNING, 40=CRITICAL", default=30)
@click.option("-v", "--verbose", count=True, help="Shorthand for info/debug loglevel (-v/-vv)")
@click.option(
    "-s",
    "--scene",
    help=f"""The test scene selection, one of {",".join([f' "{scene}"' for scene in TestScene.scene_descriptions()])}""",  # pylint: disable=C0301
    default="default",
)
@click.option("-w", "--width", help="Scene width", default=512)
@click.option("-h", "--height", help="Scene height", default=512)
@click.option("-f", "--length", help="How many frames of test scenery to produce", default=512)
@click.argument("output", type=click.Path())
def testscene_cli(output: Path, loglevel: int, verbose: int, scene: str, width: int, height: int, length: int,) -> None:
    """Run the test scene generator"""
    if verbose == 1:
        loglevel = 20
    if verbose >= 2:
        loglevel = 10
    LOGGER.setLevel(loglevel)
    instance = TestScene(scene=scene, width=width, height=height, length=length, output=Path(output))
    instance.save()
    sys.exit(0)
