import idem_linux.grains.net.realm
import pytest
import shutil
import mock
from dict_tools import data


@pytest.mark.asyncio
async def test_load_windows_domain(mock_hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict(
        {"stdout": "TESTDOMAIN\nOTHERDOMAIN"}
    )

    with mock.patch.object(shutil, "which", return_value=True):
        await idem_linux.grains.net.realm.load_windows_domain(mock_hub)

    assert mock_hub.grains.GRAINS.windowsdomain == "TESTDOMAIN"
    assert mock_hub.grains.GRAINS.windowsdomaintype == "Domain"
