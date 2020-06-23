# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import struct
from octowire.octowire import Octowire


class GPIO(Octowire):
    """
    GPIO protocol class.
    """
    OPCODE = b"\x08"
    OPERATION_OUTPUT = b"\x01"
    OPERATION_INPUT = b"\x02"
    OPERATION_PULLUP = b"\x03"
    OPERATION_PULLDOWN = b"\x04"
    OPERATION_DEACTIVATE_PULL = b"\x05"
    OPERATION_SET_PIN_HIGH = b"\x06"
    OPERATION_SET_PIN_LOW = b"\x07"
    OPERATION_READ_PIN = b"\x08"

    OUTPUT = 0
    INPUT = 1

    PULL_UP = 0
    PULL_DOWN = 1
    PULL_DISABLE = None

    def __init__(self, serial_instance, gpio_pin):
        self.serial_instance = serial_instance
        self.gpio_pin = gpio_pin
        super().__init__(serial_instance=self.serial_instance)
        if not gpio_pin and gpio_pin not in [0, 15]:
            raise ValueError('gpio_pin parameter should be defined between 0 and 15.')
        if not self.ensure_binary_mode():
            raise ValueError("Unable to enter binary mode.")
        self.direction_status = None
        self.pull_status = None
        self.pin_status = 0

    def _send_operation_code(self, operation_code, operation_name=None, disable_timeout=False):
        """
        This function sends an operation code and handles the response code.
        :param operation_code: The operation code (byte).
        :return: Nothing
        """
        args_size = struct.pack("<H", 2)
        self.serial_instance.write(args_size + self.OPCODE + bytes([self.gpio_pin]) + operation_code)
        self._read_response_code(operation_name=operation_name, disable_timeout=disable_timeout)

    @property
    def direction(self):
        """
        GPIO pin direction getter.
        :return: The pin direction (0=output, 1=input).
        :rtype: int
        """
        return self.direction_status

    @direction.setter
    def direction(self, direction):
        """
        Configure GPIO pin direction (0 = output, 1 = input).
        """
        if direction not in [0, 1]:
            raise ValueError("Invalid pin direction, the value should be 0 for output or 1 for input.")
        # Configure GPIO pin as output
        if direction == 0:
            self._send_operation_code(operation_code=self.OPERATION_OUTPUT, operation_name="set GPIO pin as output")
            self.direction_status = 1
        # Configure pin as input
        else:
            self._send_operation_code(operation_code=self.OPERATION_INPUT, operation_name="set GPIO pin as input")
            self.direction_status = 0

    @property
    def pull(self):
        """
        Return the pull config (up, down or deactivated).
        :return: The current pull resistor status (0 for up, 1 for down, None for deactivated).
        """
        return self.pull_status

    @pull.setter
    def pull(self, value):
        """
        Configure the pull resistor (up, down or deactivated).
        """
        if value not in [self.PULL_UP, self.PULL_DOWN, self.PULL_DISABLE]:
            raise ValueError("Invalid pull value, the value should be 0 for pull-up,"
                             " 1 for pull-down or None for pull disabled.")
        # Deactivate pull resistors
        if value is None:
            self._send_operation_code(operation_code=self.OPERATION_DEACTIVATE_PULL, operation_name="GPIO pull disable")
            self.pull_status = None
        # Activate pull-up resistor
        if value == 0:
            self._send_operation_code(operation_code=self.OPERATION_PULLUP, operation_name="GPIO set pull-up")
            self.pull_status = 0
        # Activate pull-down resistor
        if value == 1:
            self._send_operation_code(operation_code=self.OPERATION_PULLDOWN, operation_name="GPIO set pull-down")
            self.pull_status = 1

    def _set_output_pin_high(self):
        """
        Set the GPIO output pin to high.
        """
        self._send_operation_code(operation_code=self.OPERATION_SET_PIN_HIGH, operation_name="Set GPIO pin to high",
                                  disable_timeout=True)
        self.pin_status = 1

    def _set_output_pin_low(self):
        """
        Set the GPIO output pin to low.
        """
        self._send_operation_code(operation_code=self.OPERATION_SET_PIN_LOW, operation_name="Set GPIO pin to low",
                                  disable_timeout=True)
        self.pin_status = 0

    @property
    def status(self):
        """
        Return the current output pin status.
        :return: Pin status (0 for low, 1 for high).
        :rtype: int
        """
        return self.pin_status

    @status.setter
    def status(self, value):
        """
        Set the GPIO output pin to low or high.
        """
        if value not in [0, 1]:
            raise ValueError("Invalid status value, the value should be 0 for low or 1 for high.")
        if value == 0:
            self._set_output_pin_low()
        elif value == 1:
            self._set_output_pin_high()

    def toggle(self):
        """
        Toggle the GPIO output pin (switch between low and high).
        """
        self.status = 1 if self.pin_status == 0 else 0

    def read(self):
        """
        Return the status of the input pin.
        :return: The status of the pin (0 for low, 1 for high).
        :rtype: int
        """
        self._send_operation_code(operation_code=self.OPERATION_READ_PIN, operation_name="GPIO read input pin")
        return self.serial_instance.read(1)
