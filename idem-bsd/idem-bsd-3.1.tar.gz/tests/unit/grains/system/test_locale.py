import pytest
import time
import mock


@pytest.mark.asyncio
async def test_load_info(mock_hub, hub):
    with mock.patch("locale.getdefaultlocale", return_value=("testlang", "testenc")):
        with mock.patch("sys.getdefaultencoding", return_value="testdetectenc"):
            mock_hub.grains.system.locale.load_info = hub.grains.system.locale.load_info
            await mock_hub.grains.system.locale.load_info()
    assert mock_hub.grains.GRAINS.locale_info.defaultlanguage == "testlang"
    assert mock_hub.grains.GRAINS.locale_info.defaultencoding == "testenc"
    assert mock_hub.grains.GRAINS.locale_info.detectedencoding == "testdetectenc"


@pytest.mark.asyncio
async def test_load_timezone(mock_hub, hub):
    val = time.tzname
    time.tzname = ("ZZZ", "ZZZ")
    mock_hub.grains.system.locale.load_timezone = hub.grains.system.locale.load_timezone
    await mock_hub.grains.system.locale.load_timezone()
    time.tzname = val

    assert mock_hub.grains.GRAINS.locale_info.timezone == "ZZZ"
