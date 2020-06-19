import pytest
import mock


@pytest.mark.asyncio
async def test_load_group(mock_hub, hub):
    ret = lambda: 0
    ret.gr_name = "test_groupname"
    with mock.patch("grp.getgrgid", return_value=ret):
        mock_hub.grains.proc.group.load_group = hub.grains.proc.group.load_group
        await mock_hub.grains.proc.group.load_group()

    assert mock_hub.grains.GRAINS.groupname == "test_groupname"
