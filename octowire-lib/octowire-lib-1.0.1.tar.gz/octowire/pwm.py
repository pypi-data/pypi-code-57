# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import struct
from octowire.octowire import Octowire


class PWM(Octowire):
    """
    PWM (Pulse Width Modulation) protocol class.
    """
    OPCODE = b"\x09"
    OPERATION_SET = b"\x01"

    PWM0 = 0
    PWM1 = 1
    PWM2 = 2
    PWM3 = 3

    def __init__(self, serial_instance, pwm_pin):
        """
        Init function.
        :param serial_instance: Octowire serial instance.
        :param pwm_pin: PWM pin number (0 (GPIO8) to 3 (GPIO11)).
        """
        self.serial_instance = serial_instance
        self.pwm_pin = pwm_pin
        super().__init__(serial_instance=self.serial_instance)
        if not pwm_pin and pwm_pin not in [0, 3]:
            raise ValueError('pwm_pin parameter should be between 0 and 3 '
                             '(corresponding to the GPIO 8 to 11 used for PWM).')
        if not self.ensure_binary_mode():
            raise ValueError("Unable to enter binary mode.")

    def set(self, frequency=1000000, duty_cycle=500):
        """
        Set the PWM.
        :param frequency: PWM frequency (2Hz to 100MHz).
        :param duty_cycle: Duty cycle in per mille  (0 to 1000‰).
        :return: 6 Bytes (4 bytes for effective frequency + 2 bytes for effective duty cycle).
        """
        if frequency not in range(2, 100000000):
            raise ValueError('PWM frequency should be defined between 2 and 100 000 000 (0Hz to 100MHz)')
        if duty_cycle not in range(0, 1000):
            raise ValueError('PWM duty cycle should be defined between 0 and 1000 per mille')
        frequency = struct.pack("<L", frequency)
        duty_cycle = struct.pack("<H", duty_cycle)
        args_size = struct.pack("<H", 8)
        self.serial_instance.write(args_size + self.OPCODE + bytes([self.pwm_pin]) + self.OPERATION_SET +
                                   frequency + duty_cycle)
        self._read_response_code(operation_name="PWM configure: response code", disable_timeout=True)
        return self._read_chunk(6, operation_name="PWM configure: receive response")

    def stop(self):
        """
        Stop the PWM mode.
        :return: Nothing.
        """
        self.set(duty_cycle=0)
