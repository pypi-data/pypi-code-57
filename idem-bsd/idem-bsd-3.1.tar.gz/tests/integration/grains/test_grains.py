import pytest


class TestCorn:
    @pytest.mark.asyncio
    async def test_grains(self, hub):
        """
        Verify that a standard set of grains have been defined
        """
        missing_grains = {
            "locale_info",
            "localhost",
            "manufacturer",
            "mem_total",
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
            "saltpath",
            "saltversion",
            "saltversioninfo",
            "shell",
            "SSDs",
            "swap_total",
            "serialnumber",
            "uid",
            "username",
        } - set(hub.grains.GRAINS.keys())
        assert not missing_grains

    @pytest.mark.asyncio
    async def test_grains_values(self, hub, subtests):
        """
        Verify that all grainss have values
        """
        for grain, value in hub.grains.GRAINS.items():
            with subtests.test(grain=grain):
                if value is None:
                    pytest.fail(f'"{grain}" was not assigned')
                elif not (value or isinstance(value, int) or isinstance(value, bool)):
                    pytest.skip(f'"{grain}" does not have a value')
