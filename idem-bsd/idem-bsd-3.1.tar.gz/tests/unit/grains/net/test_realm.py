from dict_tools import data
import pytest
import mock


@pytest.mark.asyncio
async def test_load_windows_domain(mock_hub, hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict(
        {"stdout": "TESTDOMAIN\nOTHERDOMAIN"}
    )

    with mock.patch("shutil.which", return_value=True):
        mock_hub.grains.net.realm.load_windows_domain = (
            hub.grains.net.realm.load_windows_domain
        )
        await mock_hub.grains.net.realm.load_windows_domain()

    assert mock_hub.grains.GRAINS.windowsdomain == "TESTDOMAIN"
    assert mock_hub.grains.GRAINS.windowsdomaintype == "Domain"
