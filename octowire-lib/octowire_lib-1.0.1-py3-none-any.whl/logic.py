# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import struct
from octowire.octowire import Octowire


class Logic(Octowire):
    """
    Logic analyzer class.
    """
    OPCODE = b"\x08"
    OPERATION_SNIFF = b"\x09"

    def __init__(self, serial_instance):
        self.serial_instance = serial_instance
        super().__init__(serial_instance=self.serial_instance)
        if not self.ensure_binary_mode():
            raise ValueError("Unable to enter binary mode.")

    def sniff(self, trigger_gpio_pin, samples, samplerate):
        """
        Collect samples from IO8 to IO15 when PIN changes.
        :param trigger_gpio_pin: GPIO trigger pin. Start sniffing when a change is detected on GPIO port.
        Setting it to an invalid pin number (16 or higher) will start the sniffing process immediately,
        without waiting for any I/O change.
        :param samples: The number of samples.
        :param samplerate: The sample rate (speed in Hz). 1 000 000 = 1MHz.
        :return: bytearray of samples.
        """
        if not isinstance(samples, int):
            raise ValueError("'samples' parameter is not an integer.")
        if not isinstance(trigger_gpio_pin, int):
            raise ValueError("'trigger_gpio_pin' parameter is not an integer.")
        args_size = struct.pack("<H", 10)
        b_samples = struct.pack("<L", samples)
        b_samplerate = struct.pack("<L", samplerate)
        self.serial_instance.write(args_size + self.OPCODE + bytes([trigger_gpio_pin]) + self.OPERATION_SNIFF
                                   + b_samples + b_samplerate)
        self._read_response_code(operation_name="Logic analyzer sampling", disable_timeout=True)
        effective_samplerate = struct.unpack("<L", self.serial_instance.read(4))[0]
        if effective_samplerate != samplerate:
            self.logger.handle("Invalid samplerate value, sniffing at {}...".format(
                effective_samplerate), self.logger.WARNING)
        return self._read_data(expected_size=samples, operation_name="Logic analyzer sampling")
