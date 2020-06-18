# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #

from .motion_lib_exception import MotionLibException


class StreamMovementInterruptedException(MotionLibException):
    """
    Thrown when ongoing stream movement is interrupted by another command or user input.
    """
