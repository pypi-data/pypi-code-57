"""
Command line interface(s)
"""
import logging
import os
import os.path

import click

from .cli_utils import _get_timestamp, _init_logging, _make_path_if_not_exists
from .crunching import _crunch_data
from .definitions import OUTPUT_PREFIX
from .stitching import _stitch_netdf_scm_ncs
from .wrangling import _do_wrangling, _tuningstrucs_blended_model_wrangling

logger = logging.getLogger("netcdf_scm")


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("src", type=click.Path(exists=True, readable=True, resolve_path=True))
@click.argument(
    "dst", type=click.Path(file_okay=False, writable=True, resolve_path=True)
)
@click.argument("crunch_contact")
@click.option(
    "--drs",
    default="Scm",
    type=click.Choice(["Scm", "MarbleCMIP5", "CMIP6Input4MIPs", "CMIP6Output"]),
    show_default=True,
    help="Data reference syntax to use for crunching.",
)
@click.option(
    "--regexp",
    default="^(?!.*(fx)).*$",
    show_default=True,
    help=(
        "Regular expression to apply to file directory (only crunches "
        "matches). Be careful, if you use a very copmlex regexp directory "
        "sorting can be extremely slow (see e.g. discussion at "
        "https://stackoverflow.com/a/5428712)!"
    ),
)
@click.option(
    "--regions",
    default="World,World|Northern Hemisphere,World|Southern Hemisphere,World|Land,World|Ocean,World|Northern Hemisphere|Land,World|Southern Hemisphere|Land,World|Northern Hemisphere|Ocean,World|Southern Hemisphere|Ocean",
    show_default=True,
    help="Comma-separated regions to crunch.",
)
@click.option(
    "--data-sub-dir",
    default="{}-crunched".format(OUTPUT_PREFIX),
    show_default=True,
    help="Sub-directory of ``dst`` to save data in.",
)
@click.option(
    "--force/--do-not-force",
    "-f",
    help="Overwrite any existing files.",
    default=False,
    show_default=True,
)
@click.option(
    "--small-number-workers",
    default=10,
    show_default=True,
    help="Maximum number of workers to use when crunching files.",
)
@click.option(
    "--small-threshold",
    default=50.0,
    show_default=True,
    help="Maximum number of data points (in millions) in a file for it to be processed in parallel with ``small-number-workers``",
)
@click.option(
    "--medium-number-workers",
    default=3,
    show_default=True,
    help="Maximum number of workers to use when crunching files.",
)
@click.option(
    "--medium-threshold",  # pylint:disable=too-many-arguments,too-many-locals
    default=120.0,
    show_default=True,
    help="Maximum number of data points (in millions) in a file for it to be processed in parallel with ``medium-number-workers``",
)
@click.option(
    "--force-lazy-threshold",
    default=1000.0,
    show_default=True,
    help="Maximum number of data points (in millions) in a file for it to be processed in memory",
)
@click.option(
    "--cell-weights",
    default=None,
    type=click.Choice(["area-only", "area-surface-fraction"]),
    show_default=True,
    help=(
        "How to weight cells when calculating aggregates. "
        "If 'area-surface-fraction', land surface fraction weights will be included when taking cell means. "
        "If 'area-only', land surface fraction weights will not be included when taking cell means, "
        "hence cells will only be weighted by their area. "
        "If nothing is provided, netCDF-SCM will guess whether land surface fraction weights should "
        "be included or not based on the data being processed. "
        "See :meth:`netcdf_scm.iris_cube_wrappers.ScmCube.get_scm_timeseries_weights` for more details."
    ),
)
def crunch_data(
    src,
    dst,
    crunch_contact,
    drs,
    regexp,
    regions,
    data_sub_dir,
    force,
    small_number_workers,
    small_threshold,
    medium_number_workers,
    medium_threshold,
    force_lazy_threshold,
    cell_weights,
):
    r"""
    Crunch data in ``src`` to netCDF-SCM ``.nc`` files in ``dst``.

    ``src`` is searched recursively and netcdf-scm will attempt to crunch all the files
    found. The directory structure in ``src`` will be mirrored in ``dst``.

    Failures and warnings are recorded and written into a text file in ``dst``. We
    recommend examining this file using a file analysis tool such as ``grep``. We
    often use the command ``grep "\|WARNING\|INFO\|ERROR <log-file>``.

    ``crunch_contact`` is written into the output ``.nc`` files' ``crunch_contact``
    attribute.
    """
    _crunch_data(
        logger,
        src,
        dst,
        crunch_contact,
        drs,
        regexp,
        regions,
        data_sub_dir,
        force,
        small_number_workers,
        small_threshold,
        medium_number_workers,
        medium_threshold,
        force_lazy_threshold,
        cell_weights,
    )


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("src", type=click.Path(exists=True, readable=True, resolve_path=True))
@click.argument(
    "dst", type=click.Path(file_okay=False, writable=True, resolve_path=True)
)
@click.argument("wrangle_contact")
@click.option(
    "--regexp",
    default="^(?!.*(fx)).*$",
    show_default=True,
    help=(
        "Regular expression to apply to file directory (only wrangles "
        "matches). Be careful, if you use a very copmlex regexp directory "
        "sorting can be extremely slow (see e.g. discussion at "
        "https://stackoverflow.com/a/5428712)!"
    ),
)
@click.option(
    "--prefix", default=None, help="Prefix to apply to output file names (not paths)."
)
@click.option(
    "--out-format",
    default="mag-files",
    type=click.Choice(
        [
            "mag-files",
            "mag-files-average-year-start-year",
            "mag-files-average-year-mid-year",
            "mag-files-average-year-end-year",
            "mag-files-point-start-year",
            "mag-files-point-mid-year",
            "mag-files-point-end-year",
            "magicc-input-files",
            "magicc-input-files-average-year-start-year",
            "magicc-input-files-average-year-mid-year",
            "magicc-input-files-average-year-end-year",
            "magicc-input-files-point-start-year",
            "magicc-input-files-point-mid-year",
            "magicc-input-files-point-end-year",
            "tuningstrucs-blend-model",
        ]
    ),
    show_default=True,
    help=(
        "Format to re-write crunched data into. The time operation conventions follow "
        "those in "
        "`Pymagicc <https://pymagicc.readthedocs.io/en/latest/file_conventions.html#namelists>`_."
    ),
)
@click.option(
    "--drs",
    default="None",
    type=click.Choice(["None", "MarbleCMIP5", "CMIP6Input4MIPs", "CMIP6Output"]),
    show_default=True,
    help="Data reference syntax to use to decipher paths. This is required to ensure the output folders match the input data reference syntax.",
)
@click.option(
    "--force/--do-not-force",
    "-f",
    help="Overwrite any existing files.",
    default=False,
    show_default=True,
)  # pylint:disable=too-many-arguments
@click.option(
    "--number-workers",  # pylint:disable=too-many-arguments
    help="Number of worker (threads) to use when wrangling.",
    default=4,
    show_default=True,
)
@click.option(
    "--target-units-specs",  # pylint:disable=too-many-arguments
    help="csv containing target units for wrangled variables.",
    default=None,
    show_default=False,
    type=click.Path(exists=True, readable=True, resolve_path=True),
)
def wrangle_netcdf_scm_ncs(
    src,
    dst,
    wrangle_contact,
    regexp,
    prefix,
    out_format,
    drs,
    force,
    number_workers,
    target_units_specs,
):
    """
    Wrangle netCDF-SCM ``.nc`` files into other formats and directory structures.

    ``src`` is searched recursively and netcdf-scm will attempt to wrangle all the
    files found.

    ``wrangle_contact`` is written into the header of the output files.
    """
    log_file = os.path.join(
        dst,
        "{}-wrangle.log".format(_get_timestamp().replace(" ", "_").replace(":", "")),
    )
    _make_path_if_not_exists(dst)
    _init_logging(
        logger,
        [
            ("wrangle_contact", wrangle_contact),
            ("source", src),
            ("destination", dst),
            ("regexp", regexp),
            ("prefix", prefix),
            ("drs", drs),
            ("out_format", out_format),
            ("force", force),
        ],
        out_filename=log_file,
    )

    # TODO: turn all wranglers into subclasses of a base `Wrangler` class
    if out_format == "tuningstrucs-blend-model":
        _tuningstrucs_blended_model_wrangling(
            logger, src, dst, regexp, force, drs, prefix
        )
    else:
        _do_wrangling(
            logger,
            src,
            dst,
            regexp,
            out_format,
            force,
            wrangle_contact,
            drs,
            number_workers,
            target_units_specs,
        )


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("src", type=click.Path(exists=True, readable=True, resolve_path=True))
@click.argument(
    "dst", type=click.Path(file_okay=False, writable=True, resolve_path=True)
)
@click.argument("stitch_contact")
@click.option(
    "--regexp",
    default="^(?!.*(fx)).*$",
    show_default=True,
    help=(
        "Regular expression to apply to file directory (only stitches "
        "matches). Be careful, if you use a very copmlex regexp directory "
        "sorting can be extremely slow (see e.g. discussion at "
        "https://stackoverflow.com/a/5428712)!"
    ),
)
@click.option(
    "--prefix", default=None, help="Prefix to apply to output file names (not paths)."
)
@click.option(
    "--out-format",
    default="mag-files",
    type=click.Choice(
        [
            "mag-files",
            "mag-files-average-year-start-year",
            "mag-files-average-year-mid-year",
            "mag-files-average-year-end-year",
            "mag-files-point-start-year",
            "mag-files-point-mid-year",
            "mag-files-point-end-year",
            "magicc-input-files",
            "magicc-input-files-average-year-start-year",
            "magicc-input-files-average-year-mid-year",
            "magicc-input-files-average-year-end-year",
            "magicc-input-files-point-start-year",
            "magicc-input-files-point-mid-year",
            "magicc-input-files-point-end-year",
            "tuningstrucs-blend-model",
        ]
    ),
    show_default=True,
    help=(
        "Format to re-write crunched data into. The time operation conventions follow "
        "those in "
        "`Pymagicc <https://pymagicc.readthedocs.io/en/latest/file_conventions.html#namelists>`_ ."
    ),
)
@click.option(
    "--drs",
    default="None",
    type=click.Choice(["None", "MarbleCMIP5", "CMIP6Input4MIPs", "CMIP6Output"]),
    show_default=True,
    help="Data reference syntax to use to decipher paths. This is required to ensure the output folders match the input data reference syntax.",
)
@click.option(
    "--force/--do-not-force",
    "-f",
    help="Overwrite any existing files.",
    default=False,
    show_default=True,
)  # pylint:disable=too-many-arguments
@click.option(
    "--number-workers",  # pylint:disable=too-many-arguments
    help="Number of worker (threads) to use when stitching.",
    default=4,
    show_default=True,
)
@click.option(
    "--target-units-specs",  # pylint:disable=too-many-arguments
    help="csv containing target units for stitched variables.",
    default=None,
    show_default=False,
    type=click.Path(exists=True, readable=True, resolve_path=True),
)
@click.option(
    "--normalise",
    default=None,
    type=click.Choice(
        [
            "31-yr-mean-after-branch-time",
            "21-yr-running-mean",
            "21-yr-running-mean-dedrift",
        ]
    ),
    show_default=False,
    help="How to normalise the data relative to piControl (if not provided, no normalisation is performed).",
)
def stitch_netcdf_scm_ncs(
    src,
    dst,
    stitch_contact,
    regexp,
    prefix,
    out_format,
    drs,
    force,
    number_workers,
    target_units_specs,
    normalise,
):
    """
    Stitch netCDF-SCM ``.nc`` files together and write out in the specified format.

    ``SRC`` is searched recursively and netcdf-scm will attempt to stitch all the
    files found. Output is written in ``DST``.

    ``STITCH_CONTACT`` is written into the header of the output files.
    """
    log_file = os.path.join(
        dst,
        "{}-stitch.log".format(_get_timestamp().replace(" ", "_").replace(":", "")),
    )
    _make_path_if_not_exists(dst)
    _init_logging(
        logger,
        [
            ("stitch-contact", stitch_contact),
            ("source", src),
            ("destination", dst),
            ("regexp", regexp),
            ("prefix", prefix),
            ("out-format", out_format),
            ("drs", drs),
            ("force", force),
            ("number-workers", number_workers),
            ("target-units-specs", target_units_specs),
            ("normalise", normalise),
        ],
        out_filename=log_file,
    )

    _stitch_netdf_scm_ncs(
        logger,
        src,
        dst,
        stitch_contact,
        regexp,
        prefix,
        out_format,
        drs,
        force,
        number_workers,
        target_units_specs,
        normalise,
    )
