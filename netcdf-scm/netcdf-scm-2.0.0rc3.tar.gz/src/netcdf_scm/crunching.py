"""
Module for crunching raw netCDF data into netCDF-SCM netCDF files
"""
import os.path
import re

import click
import numpy as np
import tqdm

from .cli_parallel import _apply_func
from .cli_utils import (
    _find_dirs_meeting_func,
    _get_timestamp,
    _init_logging,
    _load_scm_cube,
    _make_path_if_not_exists,
    _set_crunch_contact_in_results,
)
from .definitions import NAME_COMPONENTS_SEPARATOR, OUTPUT_PREFIX
from .io import get_scmcube_helper, save_netcdf_scm_nc
from .output import OutputFileDatabase


def _crunch_data(  # pylint:disable=too-many-arguments,too-many-locals,too-many-statements
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
):
    separator = NAME_COMPONENTS_SEPARATOR
    out_dir = os.path.join(dst, data_sub_dir)

    log_file = os.path.join(
        out_dir,
        "{}-crunch.log".format(_get_timestamp().replace(" ", "_").replace(":", "")),
    )
    _make_path_if_not_exists(out_dir)
    _init_logging(
        logger,
        [
            ("crunch-contact", crunch_contact),
            ("source", src),
            ("destination", out_dir),
            ("drs", drs),
            ("regexp", regexp),
            ("regions", regions),
            ("force", force),
            ("small_number_workers", small_number_workers),
            ("small_threshold", small_threshold),
            ("medium_number_workers", medium_number_workers),
            ("medium_threshold", medium_threshold),
            ("force_lazy_threshold", force_lazy_threshold),
            ("cell_weights", cell_weights),
        ],
        out_filename=log_file,
    )

    tracker = OutputFileDatabase(out_dir)
    regexp_to_match = re.compile(regexp)
    helper = get_scmcube_helper(drs)

    def keep_dir(dpath):
        if not regexp_to_match.match(dpath):
            logger.debug("Skipping (did not match regexp) %s", dpath)
            return False
        logger.info("Adding directory to queue %s", dpath)

        return True

    found_dirs, failures_dir_finding = _find_dirs_meeting_func(src, keep_dir)

    failures_calculating_data_points = False

    _get_number_data_points_kwarglist = [
        {"dpath_h": dpath, "files": files, "helper": helper}
        for dpath, files in found_dirs
    ]

    logger.info("Calculating number of points in each directory")
    dir_files_npoints = _apply_func(
        logger,
        _get_number_data_points_in_millions,
        _get_number_data_points_kwarglist,
        n_workers=small_number_workers,
        return_res=True,
    )

    dirs_to_crunch = []
    for dpath, files, no_points in tqdm.tqdm(
        dir_files_npoints, desc="Sorting directories"
    ):
        if no_points is None:
            failures_calculating_data_points = True
            try:
                helper.load_data_in_directory(dpath, process_warnings=False)
            except Exception as e:  # pylint:disable=broad-except
                logger.exception(
                    "Could not calculate size of data in %s, exception: %s", dpath, e
                )
        else:
            logger.debug("Data in %s has %s million data points", dpath, no_points)
            dirs_to_crunch.append((dpath, files, no_points))

    crunch_kwargs = {
        "logger": logger,
        "drs": drs,
        "separator": separator,
        "output_prefix": OUTPUT_PREFIX,
        "out_dir": out_dir,
        "regions": regions,
        "force": force,
        "existing_files": tracker._data,  # pylint:disable=protected-access
        "crunch_contact": crunch_contact,
        "force_lazy_threshold": force_lazy_threshold,
        "cell_weights": cell_weights,
    }

    def process_results(res):
        if res is None:
            return  # skipped crunching
        scm_timeseries_cubes, out_filepath, info = res
        logger.info("Registering %s", out_filepath)
        tracker.register(out_filepath, info)
        logger.info("Writing file to %s", out_filepath)
        save_netcdf_scm_nc(scm_timeseries_cubes, out_filepath)

    def crunch_from_list(crunch_list, n_workers=1):
        return _apply_func(
            logger,
            _crunch_files,
            crunch_list,
            common_kwarglist=crunch_kwargs,
            postprocess_func=process_results,
            n_workers=n_workers,
            style="processes",
        )

    failures_small = False
    dirs_to_crunch_small = [
        {"fnames": f, "dpath": d} for d, f, n in dirs_to_crunch if n < small_threshold
    ]
    logger.info(
        "Crunching %s directories with less than %s million data points",
        len(dirs_to_crunch_small),
        small_threshold,
    )
    if dirs_to_crunch_small:
        failures_small = crunch_from_list(
            dirs_to_crunch_small, n_workers=small_number_workers
        )

    failures_medium = False
    dirs_to_crunch_medium = [
        {"fnames": f, "dpath": d}
        for d, f, n in dirs_to_crunch
        if small_threshold <= n < medium_threshold
    ]
    logger.info(
        "Crunching %s directories with greater than or equal to %s and less than %s million data points",
        len(dirs_to_crunch_medium),
        small_threshold,
        medium_threshold,
    )
    if dirs_to_crunch_medium:
        failures_medium = crunch_from_list(
            dirs_to_crunch_medium, n_workers=medium_number_workers
        )

    failures_large = False
    dirs_to_crunch_large = [
        {"fnames": f, "dpath": d} for d, f, n in dirs_to_crunch if n > medium_threshold
    ]
    logger.info(
        "Crunching %s directories with greater than or equal to %s million data points",
        len(dirs_to_crunch_large),
        medium_threshold,
    )
    if dirs_to_crunch_large:
        failures_large = crunch_from_list(dirs_to_crunch_large, n_workers=1)

    if (
        failures_calculating_data_points
        or failures_dir_finding
        or failures_small
        or failures_medium
        or failures_large
    ):
        raise click.ClickException(
            "Some files failed to process. See {} for more details".format(log_file)
        )


def _get_number_data_points_in_millions(dpath_h, files, helper):
    try:
        helper.load_data_in_directory(dpath_h, process_warnings=False)
    except Exception:  # pylint:disable=broad-except
        return dpath_h, files, None

    data_points = np.prod(helper.cube.shape) / 10 ** 6

    return dpath_h, files, data_points


def _crunch_files(  # pylint:disable=too-many-arguments,too-many-locals
    fnames,
    dpath,
    logger=None,
    drs=None,
    separator=None,
    output_prefix=None,
    out_dir=None,
    regions=None,
    force=None,
    existing_files=None,
    crunch_contact=None,
    force_lazy_threshold=None,
    cell_weights=None,
):
    logger.info("Attempting to process: %s", fnames)
    scmcube = _load_scm_cube(drs, dpath, fnames)

    out_filename = separator.join([output_prefix, scmcube.get_data_filename()])

    outfile_dir = scmcube.get_data_directory().replace(scmcube.root_dir, out_dir)
    out_filepath = os.path.join(outfile_dir, out_filename)

    _make_path_if_not_exists(outfile_dir)

    if not force and out_filepath in existing_files:
        logger.info("Skipped (already exists, not overwriting) %s", out_filepath)
        return None

    regions = regions.split(",")
    if scmcube.netcdf_scm_realm == "ocean":
        ocean_regions = [r for r in regions if "Land" not in r]
        if set(regions) - set(ocean_regions):
            regions = ocean_regions
            logger.warning(
                "Detected ocean data, dropping land related regions so regions "
                "to crunch are now: %s",
                regions,
            )

    elif scmcube.netcdf_scm_realm == "land":
        land_regions = [
            r for r in regions if not any([ss in r for ss in ("Ocean", "El Nino")])
        ]
        if set(regions) - set(land_regions):
            regions = land_regions
            logger.warning(
                "Detected land data, dropping ocean related regions so regions "
                "to crunch are now: %s",
                regions,
            )

    ndata_points = np.prod(scmcube.cube.shape) / 10 ** 6
    lazy = ndata_points > force_lazy_threshold
    if lazy:
        logger.info(
            "Data in %s has %s million data points which is above "
            "force-lazy-threshold of %s million data points hence processing lazily",
            dpath,
            ndata_points,
            force_lazy_threshold,
        )

    results = scmcube.get_scm_timeseries_cubes(
        regions=regions, lazy=lazy, cell_weights=cell_weights,
    )
    results = _set_crunch_contact_in_results(results, crunch_contact)

    return results, out_filepath, scmcube.info


def _translate_cli_weighting_args(land_surface_fraction_weights, netcdf_scm_realm):
    if land_surface_fraction_weights == "include":
        return True

    if land_surface_fraction_weights == "area-only":
        return False

    if land_surface_fraction_weights != "guess":  # pragma: no cover # emergency valve
        raise NotImplementedError(
            "Unrecognised land_surface_fraction_weights: {}".format(
                land_surface_fraction_weights
            )
        )

    if netcdf_scm_realm == "ocean":
        return False

    # anything else e.g. land or atmosphere
    return True
