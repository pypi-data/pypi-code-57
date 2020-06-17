from evdev import UInput, AbsInfo, ecodes, events

from .types import AbsPosition


EVENTS_XBOX2EVDEV = {
    'a':             (events.EV_KEY, ecodes.BTN_A),
    'b':             (events.EV_KEY, ecodes.BTN_B),
    'x':             (events.EV_KEY, ecodes.BTN_X),
    'y':             (events.EV_KEY, ecodes.BTN_Y),
    'back':          (events.EV_KEY, ecodes.BTN_SELECT),
    'start':         (events.EV_KEY, ecodes.BTN_START),
    'leftshoulder':  (events.EV_KEY, ecodes.BTN_TL),
    'rightshoulder': (events.EV_KEY, ecodes.BTN_TR),
    'leftx':         (events.EV_ABS, ecodes.ABS_X),
    'lefty':         (events.EV_ABS, ecodes.ABS_Y),
    'rightx':        (events.EV_ABS, ecodes.ABS_RX),
    'righty':        (events.EV_ABS, ecodes.ABS_RY),
    'lefttrigger':   (events.EV_ABS, ecodes.ABS_Z),
    'righttrigger':  (events.EV_ABS, ecodes.ABS_RZ),
}


def xbox_event(controllerdb_key):
    """Return the evdev event equivalent of the Xbox controllerdb event

    Argument:
    controllerdb_key -- string (button a, b, x, y, ... or axes)
    Return:
    - a couple (event_type, event_code)
    - or None if key is unknown
    """
    if controllerdb_key in EVENTS_XBOX2EVDEV:
        return EVENTS_XBOX2EVDEV[controllerdb_key]
    else:
        return None


class Ubox360:
    """User space Gamepad (virtual device)"""

    def __init__(self):
        supported_events = {
            ecodes.EV_KEY: [
                ecodes.BTN_A,
                ecodes.BTN_B,
                ecodes.BTN_X,
                ecodes.BTN_Y,
                ecodes.BTN_TL,
                ecodes.BTN_TR,
                ecodes.BTN_SELECT,
                ecodes.BTN_START,
                ecodes.BTN_MODE,
                ecodes.BTN_THUMBL,
                ecodes.BTN_THUMBR],
            ecodes.EV_ABS: [
                (ecodes.ABS_X,     AbsInfo(value=0, min=0, max=255,
                                           fuzz=0, flat=15, resolution=0)),
                (ecodes.ABS_Y,     AbsInfo(value=0, min=0, max=255,
                                           fuzz=0, flat=15, resolution=0)),
                (ecodes.ABS_Z,     AbsInfo(value=0, min=0, max=1,
                                           fuzz=0, flat=0,  resolution=0)),
                (ecodes.ABS_RX,    AbsInfo(value=0, min=0, max=255,
                                           fuzz=0, flat=15, resolution=0)),
                (ecodes.ABS_RY,    AbsInfo(value=0, min=0, max=255,
                                           fuzz=0, flat=15, resolution=0)),
                (ecodes.ABS_RZ,    AbsInfo(value=0, min=0, max=1,
                                           fuzz=0, flat=0,  resolution=0)),
                (ecodes.ABS_HAT0X, AbsInfo(value=0, min=0, max=255,
                                           fuzz=0, flat=15, resolution=0)),
                (ecodes.ABS_HAT0Y, AbsInfo(value=0, min=0, max=255,
                                           fuzz=0, flat=15, resolution=0))]
        }
        self._udevice = UInput(supported_events, name="ubox360")

    def device_string(self):
        return str(self._udevice.device)

    def write_event(self, event_type, event_code, event_value):
        self._udevice.write(event_type, event_code, event_value)
        self._udevice.syn()

    def write_abs(self, event_type, event_code, abs_position):
        abs_info_list = self._udevice.device.capabilities()[event_type]
        abs_info = None
        for a in abs_info_list:
            if a[0] == event_code:
                abs_info = a[1]
        if abs_info is None:
            return
        if abs_position == AbsPosition.MIN:
            self._udevice.write(event_type, event_code, abs_info.min)
        elif abs_position == AbsPosition.MAX:
            self._udevice.write(event_type, event_code, abs_info.max)
        elif abs_position == AbsPosition.CENTER:
            event_value = (abs_info.max - abs_info.min) // 2
            self._udevice.write(event_type, event_code, event_value)
        self._udevice.syn()
