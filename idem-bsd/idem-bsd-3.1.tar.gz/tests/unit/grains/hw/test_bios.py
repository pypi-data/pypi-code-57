from dict_tools import data
import pytest
import mock


@pytest.mark.asyncio
async def test_load_bios_data_kenv(mock_hub, hub):
    mock_hub.exec.cmd.run.side_effect = [
        data.NamespaceDict({"stdout": "9999999"}),
        data.NamespaceDict({"stdout": "VMware"}),
        data.NamespaceDict({"stdout": "testserial"}),
        data.NamespaceDict({"stdout": "testproduct"}),
        data.NamespaceDict({"stdout": "01/01/0001"}),
        data.NamespaceDict({"stdout": "testuuid"}),
    ]

    with mock.patch("shutil.which", side_effect=[True, False]):
        mock_hub.grains.hw.bios.load_bios_data = hub.grains.hw.bios.load_bios_data
        await mock_hub.grains.hw.bios.load_bios_data()

    assert mock_hub.grains.GRAINS.biosversion == "9999999"
    assert mock_hub.grains.GRAINS.manufacturer == "VMware"
    assert mock_hub.grains.GRAINS.serialnumber == "testserial"
    assert mock_hub.grains.GRAINS.productname == "testproduct"
    assert mock_hub.grains.GRAINS.biosreleasedate == "01/01/0001"
    assert mock_hub.grains.GRAINS.uuid == "testuuid"


@pytest.mark.asyncio
async def test_load_bios_sysctl_openbsd(mock_hub, hub):
    mock_hub.exec.cmd.run.side_effect = [
        data.NamespaceDict({"stdout": "9999999"}),
        data.NamespaceDict({"stdout": "VMware"}),
        data.NamespaceDict({"stdout": "testserial"}),
        data.NamespaceDict({"stdout": "testproduct"}),
        data.NamespaceDict({"stdout": ""}),
        data.NamespaceDict({"stdout": "testuuid"}),
    ]

    with mock.patch("shutil.which", side_effect=[False, True]):
        mock_hub.grains.hw.bios.load_bios_data = hub.grains.hw.bios.load_bios_data
        await mock_hub.grains.hw.bios.load_bios_data()

    assert mock_hub.grains.GRAINS.biosversion == "9999999"
    assert mock_hub.grains.GRAINS.manufacturer == "VMware"
    assert mock_hub.grains.GRAINS.serialnumber == "testserial"
    assert mock_hub.grains.GRAINS.productname == "testproduct"
    assert mock_hub.grains.GRAINS.biosreleasedate is None
    assert mock_hub.grains.GRAINS.uuid == "testuuid"


@pytest.mark.asyncio
async def test_load_bios_sysctl_netbsd(mock_hub, hub):
    mock_hub.exec.cmd.run.side_effect = [
        data.NamespaceDict({"stdout": ""}),
        data.NamespaceDict({"stdout": "9999999"}),
        data.NamespaceDict({"stdout": ""}),
        data.NamespaceDict({"stdout": "VMware"}),
        data.NamespaceDict({"stdout": ""}),
        data.NamespaceDict({"stdout": "testserial"}),
        data.NamespaceDict({"stdout": ""}),
        data.NamespaceDict({"stdout": "testproduct"}),
        data.NamespaceDict({"stdout": "01/01/0001"}),
        data.NamespaceDict({"stdout": ""}),
        data.NamespaceDict({"stdout": "testuuid"}),
    ]

    with mock.patch("shutil.which", side_effect=[False, True]):
        mock_hub.grains.hw.bios.load_bios_data = hub.grains.hw.bios.load_bios_data
        await mock_hub.grains.hw.bios.load_bios_data()

    assert mock_hub.grains.GRAINS.biosversion == "9999999"
    assert mock_hub.grains.GRAINS.manufacturer == "VMware"
    assert mock_hub.grains.GRAINS.serialnumber == "testserial"
    assert mock_hub.grains.GRAINS.productname == "testproduct"
    assert mock_hub.grains.GRAINS.biosreleasedate == "01/01/0001"
    assert mock_hub.grains.GRAINS.uuid == "testuuid"
