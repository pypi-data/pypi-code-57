# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #

from .motion_lib_exception import MotionLibException


class InvalidResponseException(MotionLibException):
    """
    Thrown when a device sends a response with unexpected type or data.
    """
