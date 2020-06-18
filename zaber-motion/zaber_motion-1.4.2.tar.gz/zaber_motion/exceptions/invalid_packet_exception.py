# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #

from .motion_lib_exception import MotionLibException


class InvalidPacketException(MotionLibException):
    """
    Thrown when a packet from a device cannot be parsed.
    """
