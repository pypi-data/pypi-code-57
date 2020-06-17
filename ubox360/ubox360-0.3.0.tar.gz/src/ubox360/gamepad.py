import asyncio
import re

from evdev import ecodes, events

from .types import AbsPosition


class Gamepad:
    """Evdev Gamepad (real device)"""

    def __init__(self, devices, evdev_mappings):
        """Init the gamepad with events mapping facility

        Argument:
        devices -- list of InputDevice object (a game pad can have several
                   InputDevice object associated to it)
        evdev_mapping -- dictionnary of events (keys are real events and values
          are mapped events):
          {
            (event_type, event_code): (event_type, event_code, [AbsPosition]),
            ...
          }
        """
        self._devices = devices
        self._evdev_mappings = evdev_mappings

    def device_strings(self):
        """Return a list of devices strings"""
        str_list = []
        for d in self._devices:
            str_list.append(str(d))
        return str_list

    async def _read_events(self, device, write_xbox360_event,
                           write_xbox360_abs):
        async for event in device.async_read_loop():
            if (event.type, event.code) in self._evdev_mappings:
                e = self._evdev_mappings[(event.type, event.code)]
                if len(e) == 3:
                    if event.value == 0:
                        write_xbox360_abs(e[0], e[1], AbsPosition.CENTER)
                    else:
                        write_xbox360_abs(e[0], e[1], e[2])
                else:
                    write_xbox360_event(e[0], e[1], event.value)

    def create_asyncio_tasks(self, write_xbox360_event, write_xbox360_abs):
        tasks = []
        for d in self._devices:
            tasks.append(
                asyncio.create_task(
                    self._read_events(d, write_xbox360_event,
                                      write_xbox360_abs)
                )
            )
        return tasks


def gamepad_event(device_capabilities, controllerdb_key):
    """Return the evdev event equivalent of the real gamepad controllerdb event

    Argument:
    device_capabilities -- return of the InputDevice.capabilities() method
    controllerdb_key -- string (button b0, b1, b2, b3, ... or axes)
    Return one of these values:
    - a (event_type, event_code) for simple mapping
    - a ((event_type, event_code), (event_type, event_code)) tuple to represent
      an axis (obtained from 2 keys)
    - None if key is unknown
    """
    m = re.fullmatch(r"([ab])(\d+)|(\w+)(-(\w+))?", controllerdb_key)
    if m is None:
        return None
    elif m.group(1) == 'a':
        return (events.EV_ABS,
                device_capabilities[events.EV_ABS][int(m.group(2))][0])
    elif m.group(1) == 'b':
        return (events.EV_KEY,
                device_capabilities[events.EV_KEY][int(m.group(2))])
    elif (m.group(3) in ecodes.ecodes.keys() and
          m.group(5) is None):
        # Support keyboard mapping (non standard):
        return (events.EV_KEY, ecodes.ecodes[m.group(3)])
    elif (m.group(3) in ecodes.ecodes.keys() and
          m.group(5) in ecodes.ecodes.keys()):
        # Support axis mapping (non standard):
        return ((events.EV_KEY, ecodes.ecodes[m.group(3)]),
                (events.EV_KEY, ecodes.ecodes[m.group(5)]))
    else:
        return None
