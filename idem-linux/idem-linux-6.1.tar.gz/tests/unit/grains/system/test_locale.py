import idem_linux.grains.system.locale
import pytest
import locale
import sys
import time
import mock


@pytest.mark.asyncio
async def test_load_info(mock_hub):
    with mock.patch.object(
        locale, "getdefaultlocale", return_value=("testlang", "testenc")
    ):
        with mock.patch.object(sys, "getdefaultencoding", return_value="testdetectenc"):
            await idem_linux.grains.system.locale.load_info(mock_hub)
    assert mock_hub.grains.GRAINS.locale_info.defaultlanguage == "testlang"
    assert mock_hub.grains.GRAINS.locale_info.defaultencoding == "testenc"
    assert mock_hub.grains.GRAINS.locale_info.detectedencoding == "testdetectenc"


@pytest.mark.asyncio
async def test_load_timezone(mock_hub):
    val = time.tzname
    time.tzname = ("ZZZ", "ZZZ")
    await idem_linux.grains.system.locale.load_timezone(mock_hub)
    time.tzname = val

    assert mock_hub.grains.GRAINS.locale_info.timezone == "ZZZ"
