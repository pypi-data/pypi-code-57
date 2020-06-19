import datetime
import dateutil.tz as tz
import locale
import sys

try:
    import dateutil.tz  # pylint: disable=import-error

    _DATEUTIL_TZ = True
except ImportError:
    _DATEUTIL_TZ = False


async def load_locale(hub):
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

    # TODO this value should be the abbreviated name to match other OSes
    hub.grains.GRAINS.locale_info.timezone = datetime.datetime.now(
        tz.tzlocal()
    ).tzname()
