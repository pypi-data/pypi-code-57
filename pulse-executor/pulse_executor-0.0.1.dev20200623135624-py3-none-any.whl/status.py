import enum


class Program(enum.Enum):
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    ERROR = "ERROR"
    CANCELLED = "CANCELLED"


class Executor(enum.Enum):
    SMART_STOP = "SMART_STOP"
    ACTIVE = "ACTIVE"
