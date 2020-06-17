import idem_linux.grains.proc.group
import pytest
import grp
import mock


@pytest.mark.asyncio
async def test_load_group(mock_hub):
    ret = lambda: 0
    ret.gr_name = "test_groupname"
    with mock.patch.object(grp, "getgrgid", return_value=ret):
        await idem_linux.grains.proc.group.load_group(mock_hub)

    assert mock_hub.grains.GRAINS.groupname == "test_groupname"
