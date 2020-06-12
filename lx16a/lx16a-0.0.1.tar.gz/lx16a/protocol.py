import construct
from loguru import logger
import serial

command_fmt = construct.Struct(
    "header" / construct.Const(b"\x55\x55"),
    "id" / construct.Byte,
    "length" / construct.Byte,  # Length of the data + 3
    "command" / construct.Byte,
    "data" / construct.Bytes(construct.this.length - 3),
    "checksum" / construct.Byte,
)


class Protocol(object):
    def __init__(self, serial: serial.SerialBase) -> None:
        self.serial = serial

    def command(self, servo_id: int, command: int, *data) -> None:
        data_bytes = b"".join(
            [int.to_bytes(d, length=2, byteorder="little") for d in data]
        )
        p = Protocol.build_packet(servo_id, command, data_bytes)
        logger.debug(f"Command: {p}")
        self.serial.write(p)

    def query(self, servo_id: int, command: int) -> construct.Container:
        self.command(servo_id, command)
        response = self.serial.read(10)
        parsed_response = Protocol.parse_packet(response)
        logger.debug(f"Response: {parsed_response}")
        return parsed_response

    @staticmethod
    def build_packet(id: int, command: int, data: bytes = bytes()) -> bytes:
        data_length = Protocol.length(data)
        return command_fmt.build(
            dict(
                id=id,
                length=data_length,
                command=command,
                data=data,
                checksum=Protocol.checksum(id, data_length, command, data),
            )
        )

    @staticmethod
    def checksum(id: int, length: int, command: int, data: bytes) -> int:
        return 255 - ((id + length + command + sum(data)) % 256)

    @staticmethod
    def length(data: bytes) -> int:
        return 3 + len(data)

    @staticmethod
    def parse_packet(response: bytes) -> construct.Container:
        return command_fmt.parse(response)
