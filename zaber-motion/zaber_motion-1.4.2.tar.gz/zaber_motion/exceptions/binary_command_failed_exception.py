# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #

from .motion_lib_exception import MotionLibException


class BinaryCommandFailedException(MotionLibException):
    """
    Thrown when a device rejects a binary command with an error.
    """
