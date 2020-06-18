from enum import Enum


class LambdaStates(Enum):
    TIMED_OUT = "Lambda timed out."
    SUCCEEDED = "Lambda process succeeded."
    FAILED = "Lambda process failed."


class EventTypes(Enum):
    STREAM = "stream_event"
    TASK = "task_event"
    SCHEDULER = "scheduler_event"
    GENERIC = "generic_event"
