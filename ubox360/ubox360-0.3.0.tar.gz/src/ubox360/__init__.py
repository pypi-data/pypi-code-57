import evdev
import re

from .gamepad import Gamepad, gamepad_event
from .types import AbsPosition
from .ubox360 import Ubox360, xbox_event


def swap16b(val):
    return (((val & 0x00ff) << 8) |
            ((val & 0xff00) >> 8))


def parse_gamecontrollerdb(gamecontrollerdb_file):
    """Parse the gamecontrollerdb.txt file

    Argument:
    gamecontrollerdb_file -- path of the gamecontrollerdb.txt file to load
    Return:
    dict = [
      (vendor, product): [
        (control1, binding1),
        (control2, binding2),
        ...
        ]
      ...
    ]
    """
    controllerdb = {}
    pattern = re.compile(r"""                # Gamepad GUID:
                             ([0-9a-f]{4})   # - Device bus type (swapped)
                             0000
                             ([0-9a-f]{4})   # - Device vendor (swapped)
                             0000
                             ([0-9a-f]{4})   # - Device product (swapped)
                             0000
                             ([0-9a-f]{4})   # - version
                             0000,
                             ([^,]*),        # Gamepad name
                             (.*),           # key mappings + platform
                          """,
                         re.X)
    f = open(gamecontrollerdb_file)
    line = f.readline()
    while line:
        line = line.strip()
        m = pattern.fullmatch(line)
        if m:
            bus_type = swap16b(int(m.group(1), 16))  # noqa: F841
            vendor = swap16b(int(m.group(2), 16))
            product = swap16b(int(m.group(3), 16))
            version = swap16b(int(m.group(4), 16))   # noqa: F841
            gamepad_name = m.group(5)                # noqa: F841
            bindings = []
            for it in m.group(6).split(","):
                bindings.append(it.split(":"))
            controllerdb[(vendor, product)] = bindings
        line = f.readline()
    f.close()
    return controllerdb


def print_gamepad_addition(gamepad, ubox):
    print("Info: Adding a new gamepad mapping:")
    gamepad_strings = gamepad.device_strings()
    if len(gamepad_strings) > 1:
        size = len(gamepad_strings)
        end = size - 1
        half = end // 2
        for i in range(0, size):
            g = gamepad_strings[i]
            line_start = list("  | ")
            if i == 0:
                line_start[2:4] = ",-"
            elif i == end:
                line_start[2:4] = "'-"
            if i == half:
                if size % 2 == 0:
                    line_start[0:2] = " _"
                else:
                    line_start[0:2] = ",-"
            elif i > half:
                line_start[0] = "|"
            print("  %s%s" % ("".join(line_start), g))
    else:
        print("  ,-- %s" % (gamepad_strings[0]))
    print("  '-> %s" % (ubox.device_string()))


def create_devices(gamecontrollerdb, devices_path=None):
    """Return a list of (Gamepad, Ubox360) couples

    Argument:
    gamecontrollerdb -- result parse_gamecontrollerdb()
    devices_path -- if not None, only use devices from this list
    Return:
    list = [
      (Gamepad, Ubox360),
      ...
    ]
    """
    gamepads_list = []
    if devices_path is None:
        devices_path = evdev.list_devices()
    input_devices = [evdev.InputDevice(path) for path in devices_path]
    phys_devices = {}

    for d in input_devices:
        if (d.info.vendor, d.info.product) in gamecontrollerdb.keys():
            key = d.phys
            if "/" in key:
                key = key.split("/")[0]
            if key in phys_devices.keys():
                phys_devices[key].append(d)
            else:
                phys_devices[key] = [d]

    for gamepad_devices in phys_devices.values():
        d = gamepad_devices[0]
        evdev_mappings = {}
        for (key, value) in gamecontrollerdb[(d.info.vendor, d.info.product)]:
            if (key == "platform"):
                continue
            x_event = xbox_event(key)
            if (x_event is None):
                print("Warning: %s is an unknown Xbox event" % key)
                continue
            g_event = gamepad_event(d.capabilities(), value)
            if (g_event is None):
                print("Warning: %s is an unknown Gamepad event" % value)
                continue
            if all((type(e) == tuple) for e in g_event):
                evdev_mappings[g_event[0]] = x_event + (AbsPosition.MIN,)
                evdev_mappings[g_event[1]] = x_event + (AbsPosition.MAX,)
            else:
                evdev_mappings[g_event] = x_event
        g = Gamepad(gamepad_devices, evdev_mappings)
        u = Ubox360()
        print_gamepad_addition(g, u)
        gamepads_list.append((g, u))
    return gamepads_list
