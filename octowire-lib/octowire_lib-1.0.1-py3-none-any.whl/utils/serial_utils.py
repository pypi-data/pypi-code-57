# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import serial
from datetime import datetime
from octowire.utils.Logger import Logger
from octowire.time import Time
from serial.tools import list_ports


def detect_octowire(verbose=True):
    """
    Iterate over serial devices to find the Octowire, returning the serial port.
    :return: Octowire port or None.
    """
    ports_list = list_ports.comports(include_links=True)
    for port in ports_list:
        if port.vid == 0xc0de and port.pid == 0x0c70:
            if verbose:
                Logger().handle("Octowire found: {}".format(port.device), Logger.RESULT)
            return port.device
        if port.vid == 0xc0de and port.pid == 0xb007:
            if verbose:
                Logger().handle("Octowire found in bootloader mode, please press the reset button and retry...",
                                Logger.ERROR)
            return None
    if verbose:
        Logger().handle("Octowire not found...", Logger.ERROR)
    return None


def octowire_serial(serial_name):
    """
    Connect to the Octowire with the correct baudrate value and set the current datetime.
    :param serial_name: Octowire serial port.
    :return: Serial instance or None if error.
    """
    try:
        s_octowire = serial.Serial(serial_name, 7372800, timeout=1)
        t_octowire = Time(s_octowire)
        now = datetime.now()
        octo_str_date = t_octowire.get_time()
        if (datetime.strptime(octo_str_date.decode(), "%Y/%m/%d %H:%M:%S") - now).seconds > 60:
            t_octowire.set_time(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute,
                                second=now.second)
        return s_octowire
    except serial.SerialException as err:
        Logger().handle("Connection error: {}".format(err), Logger.ERROR)
        return None


def detect_and_connect():
    """
    This function tries to find the Octowire port and automatically connects to it.
    :return: Serial instance or None if error
    """
    serial_name = detect_octowire()
    if serial_name is not None:
        return octowire_serial(serial_name)
    return None
