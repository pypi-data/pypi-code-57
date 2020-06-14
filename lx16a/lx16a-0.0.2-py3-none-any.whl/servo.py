import ctypes

from loguru import logger

from . import constants
from .protocol import Protocol
import time


class Servo(object):
    def __init__(self, protocol: Protocol, servo_id: int = None) -> None:
        self.__protocol = protocol
        self.id = servo_id or self._get_servo_id()

    def _get_servo_id(self) -> int:
        logger.debug("Get servo ID")
        response = self.__protocol.query(
            constants.SERVO_ID_ALL, constants.SERVO_ID_READ
        )
        return response["id"]

    def set_servo_id(self, id: int) -> None:
        logger.debug(f"Set servo {self.id} ID to {id}")
        self.__protocol.command(self.id, constants.SERVO_ID_WRITE, id)
        self.id = id

    def get_position(self) -> int:
        logger.debug(f"Get position for servo {self.id}")
        response = self.__protocol.query(self.id, constants.SERVO_POS_READ)
        return Servo.parse_value(response["data"])

    def set_position(self, position: int) -> None:
        logger.debug(f"Set servo {self.id} position to {position}")
        self.__protocol.command(self.id, constants.SERVO_MOVE_TIME_WRITE, position)

    def set_position_blocking(self, position: int, threshold=10) -> None:
        def delta() -> float:
            current_position = self.get_position()
            d = ((current_position - position) ** 2) ** 0.5
            logger.debug(
                f"Desired position: {position}, current: {current_position}, delta: {d}"
            )
            return d

        d = delta()
        while d > threshold:
            self.set_position(position)
            time.sleep(0.5)
            d = delta()

    @staticmethod
    def parse_value(b: bytes) -> int:
        return ctypes.c_int16(int.from_bytes(b, byteorder="little")).value

    def prepare_position(self, position: int) -> None:
        logger.debug(f"Prepare servo {self.id} position for {position}")
        self.__protocol.command(self.id, constants.SERVO_MOVE_TIME_WAIT_WRITE, position)

    def start(self) -> None:
        logger.debug(f"Starting prepared moves for servo {self.id}")
        self.__protocol.command(self.id, constants.SERVO_MOVE_START)

    def stop(self) -> None:
        logger.debug(f"Stopping {self.id}")
        self.__protocol.command(self.id, constants.SERVO_MOVE_STOP)


class ServoCollection(object):
    def __init__(self, protocol: Protocol) -> None:
        self.__protocol = protocol

    def start_all(self) -> None:
        logger.debug(f"Starting prepared moves for all servos")
        self.__protocol.command(constants.SERVO_ID_ALL, constants.SERVO_MOVE_START)

    def stop_all(self) -> None:
        logger.debug(f"Stopping all servos")
        self.__protocol.command(constants.SERVO_ID_ALL, constants.SERVO_MOVE_STOP)
