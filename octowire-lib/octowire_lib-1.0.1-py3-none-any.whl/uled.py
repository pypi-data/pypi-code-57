# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import struct
from octowire.octowire import Octowire


class ULED(Octowire):
    """
    User LED class.
    """
    OPCODE = b"\x07"
    LED_OFF = 0
    LED_ON = 1

    def __init__(self, serial_instance):
        """
        Init function.
        :param serial_instance: Octowire Serial instance.
        """
        self.serial_instance = serial_instance
        self.uled_state = 0
        super().__init__(serial_instance=self.serial_instance)
        if not self.ensure_binary_mode():
            raise ValueError("Unable to enter binary mode.")

    @property
    def state(self):
        """
        Return current user LED state.
        :return: 0 if it is turned off, 1 otherwise.
        :rtype: int
        """
        return self.uled_state

    @state.setter
    def state(self, state):
        """
        Change the user LED state (0 for off, 1 for on).
        :param state: 0 or 1 to change the user LED state.
        """
        args_size = struct.pack("<H", 1)
        bstate = struct.pack("<?", state)
        self.serial_instance.write(args_size + self.OPCODE + bstate)
        self._read_response_code(operation_name="Change user led state")
        self.uled_state = state

    def toggle(self):
        """
        This function inverts the current state of the user LED.
        """
        self.state = 1 if self.state == 0 else 0
