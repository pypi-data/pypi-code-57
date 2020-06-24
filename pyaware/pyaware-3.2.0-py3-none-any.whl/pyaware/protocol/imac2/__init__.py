from enum import IntEnum


class ModuleStatus(IntEnum):
    ONLINE = 0
    SYSTEM = 1
    OFFLINE = 2
    CLASH = 3
    NEVER_ONLINE = 4
    SYSTEM_ONLINE = 5
