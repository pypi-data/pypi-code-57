from os.path import join

import pytest
from click.testing import CliRunner

from netcdf_scm.cli import crunch_data


@pytest.mark.parametrize("table_id", ["Amon", "Omon", "Lmon", "Emon"])
def test_crunching(
    tmpdir,
    update_expected_files,
    test_data_cmip6output_dir,
    test_cmip6_crunch_output,
    run_crunching_comparison,
    table_id,
):
    input_dir = test_data_cmip6output_dir
    output_dir = str(tmpdir)
    regions_to_get = [
        "World",
        "World|Northern Hemisphere",
        "World|Southern Hemisphere",
        "World|Land",
        "World|Ocean",
        "World|Northern Hemisphere|Land",
        "World|Southern Hemisphere|Land",
        "World|Northern Hemisphere|Ocean",
        "World|Southern Hemisphere|Ocean",
        "World|North Atlantic Ocean",
        "World|El Nino N3.4",
    ]

    runner = CliRunner()
    result = runner.invoke(
        crunch_data,
        [
            input_dir,
            output_dir,
            "cmip6output crunching regression test",
            "--drs",
            "CMIP6Output",
            "-f",
            "--small-number-workers",
            1,
            "--regions",
            ",".join(regions_to_get),
            "--regexp",
            ".*{}.*".format(table_id),
        ],
    )
    assert result.exit_code == 0, result.output
    run_crunching_comparison(
        join(output_dir, "netcdf-scm-crunched", "CMIP6"),
        join(test_cmip6_crunch_output, table_id, "CMIP6"),
        update=update_expected_files,
    )
