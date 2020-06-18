# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #

from .motion_lib_exception import MotionLibException


class MovementFailedException(MotionLibException):
    """
    Thrown when a device registers a fault during movement.
    """
