import pytest


@pytest.mark.asyncio
async def test_grains(hub):
    """
    Verify that a standard set of grains have been defined
    """
    missing_grains = {
        "locale_info",
        "localhost",
        "manufacturer",
        "mem_total",
        # "model_name",
        "nodename",
        "num_cpus",
        "num_gpus",
        "os",
        "os_family",
        "osarch",
        "osbuild",
        "oscodename",
        "osfinger",
        "osfullname",
        "osmajorrelease",
        "osrelease",
        "osrelease_info",
        "path",
        "pid",
        "productname",
        "ps",
        "pythonexecutable",
        "pythonpath",
        "pythonversion",
        "requirement_versions",
        "shell",
        "SSDs",
        "swap_total",
        # "serialnumber",
        "uid",
        "username",
        "virtual",
        "virtual_subtype",
    } - set(hub.grains.GRAINS.keys())
    assert not missing_grains


@pytest.mark.asyncio
async def test_grains_values(hub, subtests):
    """
    Verify that all grainss have values
    """
    for grain, value in hub.grains.GRAINS.items():
        with subtests.test(grain=grain):
            if value is None:
                pytest.skip(f'"{grain}" was not assigned')
            elif not (value or isinstance(value, int) or isinstance(value, bool)):
                pytest.skip(f'"{grain}" does not have a value')
