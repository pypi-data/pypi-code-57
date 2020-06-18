# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #

from .motion_lib_exception import MotionLibException


class CommandFailedException(MotionLibException):
    """
    Thrown when a device rejects a command.
    """
