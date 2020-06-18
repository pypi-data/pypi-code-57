import distro
import idem_linux.grains.os.os
import pytest
import mock


@pytest.mark.asyncio
async def test_load_majorrelease(mock_hub):
    pass


@pytest.mark.asyncio
async def test_load_manufacturer(mock_hub):
    pass


@pytest.mark.asyncio
async def test_load_linux_distribution(mock_hub):
    class Distribution:
        def build_number(self):
            return "testbuild"

        def codename(self):
            return "testcodename"

        def name(self):
            return "testname"

        def version(self):
            return "999.999.999"

        def major_version(self):
            return "10"

    with mock.patch.object(distro, "LinuxDistribution", return_value=Distribution()):
        await idem_linux.grains.os.os.load_linux_distribution(mock_hub)

    assert mock_hub.grains.GRAINS.osbuild == "testbuild"
    assert mock_hub.grains.GRAINS.oscodename == "testcodename"
    assert mock_hub.grains.GRAINS.osfullname == "testname"
    assert mock_hub.grains.GRAINS.osrelease == "999.999.999"
    assert mock_hub.grains.GRAINS.os == "testname"
    assert mock_hub.grains.GRAINS.osrelease_info == (999, 999, 999)
    assert mock_hub.grains.GRAINS.osmajorrelease == 10
    assert mock_hub.grains.GRAINS.osfinger == "testname-999"
