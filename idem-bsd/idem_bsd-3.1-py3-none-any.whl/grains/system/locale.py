import dateutil.tz
import locale
import datetime
import sys


async def load_info(hub):
    """
    Provides
        defaultlanguage
        defaultencoding
    """
    try:
        (
            hub.grains.GRAINS.locale_info.defaultlanguage,
            hub.grains.GRAINS.locale_info.defaultencoding,
        ) = locale.getdefaultlocale()
    except Exception:  # pylint: disable=broad-except
        # locale.getdefaultlocale can ValueError!! Catch anything else it
        # might do, per #2205
        hub.grains.GRAINS.locale_info.defaultlanguage = "unknown"
        hub.grains.GRAINS.locale_info.defaultencoding = "unknown"
    hub.grains.GRAINS.locale_info.detectedencoding = sys.getdefaultencoding() or "ascii"


async def load_timezone(hub):
    hub.grains.GRAINS.locale_info.timezone = datetime.datetime.now(
        dateutil.tz.tzlocal()
    ).tzname()
