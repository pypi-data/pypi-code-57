import ctypes

from loguru import logger

from .protocol import Protocol

SERVO_ID_ALL = 0xFE
SERVO_MOVE_TIME_WRITE = 1
SERVO_MOVE_TIME_READ = 2
SERVO_MOVE_TIME_WAIT_WRITE = 7
SERVO_MOVE_TIME_WAIT_READ = 8
SERVO_MOVE_START = 11
SERVO_MOVE_STOP = 12
SERVO_ID_WRITE = 13
SERVO_ID_READ = 14
SERVO_ANGLE_OFFSET_ADJUST = 17
SERVO_ANGLE_OFFSET_WRITE = 18
SERVO_ANGLE_OFFSET_READ = 19
SERVO_ANGLE_LIMIT_WRITE = 20
SERVO_ANGLE_LIMIT_READ = 21
SERVO_VIN_LIMIT_WRITE = 22
SERVO_VIN_LIMIT_READ = 23
SERVO_TEMP_MAX_LIMIT_WRITE = 24
SERVO_TEMP_MAX_LIMIT_READ = 25
SERVO_TEMP_READ = 26
SERVO_VIN_READ = 27
SERVO_POS_READ = 28
SERVO_OR_MOTOR_MODE_WRITE = 29
SERVO_OR_MOTOR_MODE_READ = 30
SERVO_LOAD_OR_UNLOAD_WRITE = 31
SERVO_LOAD_OR_UNLOAD_READ = 32
SERVO_LED_CTRL_WRITE = 33
SERVO_LED_CTRL_READ = 34
SERVO_LED_ERROR_WRITE = 35
SERVO_LED_ERROR_READ = 36
SERVO_ERROR_OVER_TEMPERATURE = 1
SERVO_ERROR_OVER_VOLTAGE = 2
SERVO_ERROR_LOCKED_ROTOR = 4


class Servo(object):
    def __init__(self, protocol: Protocol, servo_id: int = None) -> None:
        self.__protocol = protocol
        self.id = servo_id or self._get_servo_id()

    def _get_servo_id(self) -> int:
        logger.debug("Get servo ID")
        response = self.__protocol.query(SERVO_ID_ALL, SERVO_ID_READ)
        return response["id"]

    def get_position(self) -> int:
        logger.debug(f"Get position for servo {self.id}")
        response = self.__protocol.query(self.id, SERVO_POS_READ)
        return Servo.parse_value(response["data"])

    def set_position(self, position: int) -> None:
        logger.debug(f"Set servo {self.id} position to {position}")
        self.__protocol.command(self.id, SERVO_MOVE_TIME_WRITE, position)

    @staticmethod
    def parse_value(b: bytes) -> int:
        return ctypes.c_int16(int.from_bytes(b, byteorder="little")).value
