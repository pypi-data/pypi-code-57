"""
Module for wrangling netCDF-SCM netCDF files into other formats
"""
import os
import re

import click
import pandas as pd
from scmdata import ScmDataFrame, df_append

from .cli_parallel import _apply_func
from .cli_utils import (
    _find_dirs_meeting_func,
    _get_openscmdf_metadata_header,
    _get_outfile_dir,
    _write_ascii_file,
)
from .io import get_scmcube_helper, load_scmdataframe
from .wranglers import convert_scmdf_to_tuningstruc


def _tuningstrucs_blended_model_wrangling(  # pylint:disable=too-many-arguments
    logger, src, dst, regexp, force, drs, prefix
):
    regexp_compiled = re.compile(regexp)
    considered_regexps = []
    for dirpath, _, filenames in os.walk(src):
        if filenames:
            if not regexp_compiled.match(dirpath):
                continue

            if considered_regexps:
                if any([r.match(dirpath) for r in considered_regexps]):
                    continue

            regexp_here = _get_blended_model_regexp(drs, dirpath)
            logger.info("Wrangling %s", regexp_here)

            _tuningstrucs_blended_model_wrangling_inner_loop(
                src, regexp_here, dst, force, prefix
            )
            considered_regexps.append(regexp_here)


def _get_blended_model_regexp(drs, dirpath):
    scmcube = get_scmcube_helper(drs)
    ids = {
        k: v
        if any(
            [s in k for s in ["variable", "experiment", "activity", "mip", "member_id"]]
        )
        else ".*"
        for k, v in scmcube.process_path(dirpath).items()
    }
    for name, value in ids.items():
        setattr(scmcube, name, value)

    return re.compile("{}.*".format(scmcube.get_data_directory()))


def _tuningstrucs_blended_model_wrangling_inner_loop(
    src, regexp_inner, dst, force, prefix
):
    collected = []
    for dirpath_inner, _, filenames_inner in os.walk(src):
        if filenames_inner:
            if not regexp_inner.match(dirpath_inner):
                continue

            openscmdf = df_append(
                [
                    load_scmdataframe(os.path.join(dirpath_inner, f))
                    for f in filenames_inner
                ]
            )
            tmp_ts = openscmdf.timeseries().reset_index()
            tmp_ts["unit"] = tmp_ts["unit"].astype(str)
            openscmdf = ScmDataFrame(tmp_ts)

            collected.append(openscmdf)

    convert_scmdf_to_tuningstruc(df_append(collected), dst, force=force, prefix=prefix)


def _do_wrangling(  # pylint:disable=too-many-arguments
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
):
    regexp_compiled = re.compile(regexp)
    if target_units_specs is not None:
        target_units_specs = pd.read_csv(target_units_specs)

    if out_format in (
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
    ):
        _do_magicc_wrangling(
            logger,
            src,
            dst,
            regexp_compiled,
            out_format,
            force,
            wrangle_contact,
            drs,
            number_workers,
            target_units_specs,
        )
    else:  # pragma: no cover # emergency valve (should be caught by click on call)
        raise ValueError("Unsupported format: {}".format(out_format))


def _do_magicc_wrangling(  # pylint:disable=too-many-arguments,too-many-locals
    logger,
    src,
    dst,
    regexp_compiled,
    out_format,
    force,
    wrangle_contact,
    drs,
    number_workers,
    target_units_specs,
):
    crunch_list, failures_dir_finding = _find_dirs_meeting_func(
        src, regexp_compiled.match
    )

    if out_format in (
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
    ):
        failures_wrangling = _apply_func(
            logger,
            _wrangle_magicc_files,
            [{"fnames": f, "dpath": d} for d, f in crunch_list],
            common_kwarglist={
                "logger": logger,
                "dst": dst,
                "force": force,
                "out_format": out_format,
                "target_units_specs": target_units_specs,
                "wrangle_contact": wrangle_contact,
                "drs": drs,
            },
            n_workers=number_workers,
            style="processes",
        )

    else:  # pragma: no cover # emergency valve
        raise AssertionError(
            "how did we get here, click should have prevented the --out-format "
            "option..."
        )

    if failures_dir_finding or failures_wrangling:
        raise click.ClickException(
            "Some files failed to process. See the logs for more details"
        )


def _wrangle_magicc_files(  # pylint:disable=too-many-arguments
    logger,
    fnames,
    dpath,
    dst,
    force,
    out_format,
    target_units_specs,
    wrangle_contact,
    drs,
):
    logger.info("Attempting to process: %s", fnames)
    openscmdf, metadata, header = _get_openscmdf_metadata_header(
        fnames, dpath, target_units_specs, wrangle_contact, out_format
    )

    outfile_dir = _get_outfile_dir(dpath, drs, dst)

    _write_ascii_file(
        openscmdf, metadata, header, outfile_dir, fnames, force, out_format, drs,
    )
