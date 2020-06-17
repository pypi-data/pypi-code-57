import idem_linux.grains.system.selinux
import pytest
import shutil
import mock
from dict_tools import data


@pytest.mark.asyncio
async def test_load_selinux(mock_hub):
    mock_hub.exec.cmd.run.side_effect = [
        data.NamespaceDict({"retcode": 0}),
        data.NamespaceDict({"stdout": "Enabled"}),
    ]
    with mock.patch.object(shutil, "which", return_value=True):
        await idem_linux.grains.system.selinux.load_selinux(mock_hub)
    assert mock_hub.grains.GRAINS.selinux.enabled is True
    assert mock_hub.grains.GRAINS.selinux.enforced == "Enabled"
