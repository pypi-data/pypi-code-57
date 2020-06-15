"The command line interface and entry point for classifier"
import logging

import click

from classifier.classify import classify_, classify_timeseries
from classifier.segment import simple_segmentation
from classifier.segment import classify_segments
from classifier.utils.general import cli_init, save_dict_as_json


CLI_LOGGER = logging.getLogger(__name__)


@click.group()
def cli():
    """---Classifier---
     Classification,segmentation and object detection"""
    pass


@cli.command()
@click.argument(
    'rasters',
    nargs=-1,
    type=click.Path(),
)

@click.option(
    '--rois',
    default=None,
    type=click.Path(),
    help="""OGR supported polygon file"""
)
@click.option(
    '--name',
    type=click.STRING,
    help="""Name of the output folder"""
)

@click.option(
    '--overwrite',
    default=False,
    type=click.BOOL,
    help="""Overwrite Existing output folder"""
)

def classification(name, rasters, rois, overwrite):
    """Do a traditional (un)supervised classification

    Raster input paths can be added like arguments without a prefix.
    Multiple raster paths can be added

    For additional options, create a config file in your workspace. Also see
    https://satelligence.gitlab.io/classifier/usage/configfile.html.

    """
    out_dir, rasters, config_dict = cli_init(name, rasters, overwrite)
    config_dict['name'] = name
    if config_dict['app_rasters_are_timeseries']:
        classify_timeseries(rasters, config_dict, out_dir, rois)
    else:
        classify_(rasters, config_dict, out_dir, rois)


@cli.command()
@click.argument(
    'rasters',
    nargs=-1,
    type=click.Path(),
)
@click.option(
    '--name',
    type=click.STRING,
    help="""Name of the output folder"""
)
@click.option(
    '--rois',
    default=None,
    type=click.Path(),
    help="""OGR supported polygon file"""
)
@click.option(
    '--overwrite',
    default=False,
    type=click.BOOL,
    help="""Overwrite Existing output folder"""
)
def segmentation(name, rasters, rois, overwrite):
    """Do a segmentation with Raster input data.

    For changing the segmentation parameters create a config file in your
    workspace. For more information see
    https://satelligence.gitlab.io/classifier/usage/configfile.html

    """
    out_dir, rasters, config_dict = cli_init(name, rasters, overwrite)
    if not config_dict['segm_custom_segments']:
        simple_segmentation(out_dir, rasters, config_dict)
    if config_dict['segm_classify']:
        if config_dict['app_rasters_are_timeseries']:
            classify_timeseries(rasters, config_dict, out_dir, rois)
        else:
            classify_(rasters, config_dict, out_dir, rois)

        classify_segments(out_dir, config_dict)


@cli.command()
def objectdetection():
    """Object detection in raster imagery. Not yet implemented"""
    raise NotImplementedError


@cli.command()
def make_config():
    """Make a config file with default values in your workspace directory
    and exit"""
    save_dict_as_json()


if __name__ == '__main__':
    cli()
