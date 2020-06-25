import time
from _ctypes import byref
from ctypes import create_string_buffer, c_uint32, CDLL, c_uint16, c_int, c_int8, c_uint8, c_char

import bidict
import numpy as np

from kamzik3 import DeviceError
from kamzik3.constants import *
from kamzik3.devices.deviceChannel import DeviceChannel
from kamzik3.devices.deviceOsLibrary import DeviceOsLibrary

MODE_PROFILE_POSITION = 1
MODE_PROFILE_VELOCITY = 3
MODE_HOMING = 6
MODE_POSITION = 8
MODE_VELOCITY = 9
MODE_CURRENT = 10


class DeviceEpos(DeviceOsLibrary):

    def __init__(self, library, device_name, protocol, interface, port, device_id=None, config=None):
        self.device_name = create_string_buffer(device_name.encode())
        self.protocol = create_string_buffer(protocol.encode())
        self.interface = create_string_buffer(interface.encode())
        self.port = create_string_buffer(port.encode())
        self.handle = 0
        self.pError = c_uint32()
        DeviceOsLibrary.__init__(self, library, device_id, config)

    def handle_configuration(self):
        start_at = time.time()

        def _finish_configuration(*_, **__):
            self._config_commands()
            self._config_attributes()
            self.start_polling()
            self.set_status(STATUS_IDLE)
            self.logger.info(u"Device configuration took {} sec.".format(time.time() - start_at))

        self.connected = True
        _finish_configuration()

    def connect(self, *args):
        """
        Call only this function to connect devices to port / socket / library / ...
        :param args: connect attributes
        """
        self.connecting = True
        self.handle_configuration_event()
        try:
            self.lib = CDLL(self.os_library)
            self.handle = self.check_error(
                self.lib.VCS_OpenDevice(byref(self.device_name), byref(self.protocol), byref(self.interface),
                                        byref(self.port), byref(self.pError)))
        except OSError as e:
            raise DeviceError("Error loading library {}. {}".format(self.os_library, e))
        self.connected = True
        self.connecting = False
        self.set_status(STATUS_IDLE)

    def check_error(self, error_code, raise_exception=True):
        """
        Check error response for executed command.
        :param error_code: error code response
        :param raise_exception: raise exception if True
        :return:
        """
        if error_code == 0:
            error_message = "Error: %s" % self.get_error()
            if raise_exception:
                raise DeviceError(error_message)
        return error_code

    def get_error(self, pError=None):
        """
        Get error description of given code.
        :param pError: error code
        :return:
        """
        if pError is None:
            pError = self.pError
        pErrorInfo = create_string_buffer(255)
        if self.lib.VCS_GetErrorInfo(pError, byref(pErrorInfo), 255) != 0:
            return "Code: %s, %s" % (pError.value, pErrorInfo.value)
        else:
            return "Code: %s, %s" % (pError.value, "Unknown error")

    def disconnect(self):
        self.lib.VCS_CloseDevice(self.handle, byref(self.pError))
        return super().disconnect()


class DeviceEposLinux(DeviceEpos):

    def __init__(self, device_name, protocol, interface, port, device_id=None, config=None):
        DeviceEpos.__init__(self, "libEposCmd.so", device_name, protocol, interface, port, device_id, config)


class DeviceEposChannel(DeviceChannel):
    operation_modes = bidict.frozenbidict({
        MODE_PROFILE_POSITION: u"Profile position",
        MODE_PROFILE_VELOCITY: u"Profile velocity",
        MODE_HOMING: u"Homing",
        MODE_POSITION: u"Position",
        MODE_VELOCITY: u"Velocity",
        MODE_CURRENT: u"Current",
    })
    velocity_units = bidict.frozenbidict({
        u"Standard": 0,
        u"Deci": -1,
        u"Centi": -2,
        u"Milli": -3,
    })

    def _init_attributes(self):
        DeviceChannel._init_attributes(self)

        self.create_attribute(ATTR_HARDWARE_VERSION, default_value=None, readonly=True, default_type=np.uint16)
        self.create_attribute(ATTR_SOFTWARE_VERSION, default_value=None, readonly=True, default_type=np.uint16)
        self.create_attribute(ATTR_APPLICATION_NUMBER, default_value=None, readonly=True, default_type=np.uint16)
        self.create_attribute(ATTR_APPLICATION_VERSION, default_value=None, readonly=True, default_type=np.uint32)
        self.create_attribute(ATTR_OPERATION_MODE, default_value=None, readonly=True,
                              default_type=self.operation_modes.inverse.keys(), set_function=self.set_operation_mode)
        self.create_attribute(ATTR_MOTOR_EXCITATION, default_value=False, default_type=bool,
                              set_function=self.set_motor_enabled)
        self.create_attribute(ATTR_VELOCITY_UNITS, default_value=None, readonly=True,
                              default_type=self.velocity_units.keys(), set_function=self.set_velocity_units)

    def handle_configuration(self):
        if self.configured:
            return

        start_at = time.time()

        def _finish_configuration(*_, **__):
            self._config_commands()
            self._config_attributes()
            self.configured = True
            self.start_polling()
            self.set_status(STATUS_CONFIGURED)
            self.logger.info(u"Device configuration took {} sec.".format(time.time() - start_at))

        self.get_device_firmware_version()
        self.get_operation_mode()
        self.get_enabled_state()
        self.get_velocity_units()
        self.set_motor_enabled(True)
        _finish_configuration()

    def get_device_firmware_version(self):
        '''
        VCS_GetVersion(HANDLE
        KeyHandle, WORD
        NodeId, WORD * pHardwareVersion, WORD *
        pSoftwareVersion, WORD * pApplicationNumber, WORD * pApplicationVersion, DWORD * pErrorCode)
        '''
        hw_version = c_uint16()
        sw_version = c_uint16()
        app_number = c_uint16()
        app_version = c_uint32()
        self.device.check_error(
            self.device.lib.VCS_GetVersion(self.device.handle, self.channel, byref(hw_version), byref(sw_version),
                                           byref(app_number),
                                           byref(app_version), byref(self.device.pError)))
        self.set_value(ATTR_HARDWARE_VERSION, hw_version.value)
        self.set_value(ATTR_SOFTWARE_VERSION, sw_version.value)
        self.set_value(ATTR_APPLICATION_NUMBER, app_number.value)
        self.set_value(ATTR_APPLICATION_VERSION, app_version.value)

    def get_movement_state(self):
        state = c_int()
        self.device.check_error(
            self.device.lib.VCS_GetMovementState(self.device.handle, self.channel, byref(state),
                                                 byref(self.device.pError))
        )
        return state.value

    def get_state(self):
        state = c_uint32()
        self.device.check_error(
            self.device.lib.VCS_GetState(self.device.handle, self.channel, byref(state), byref(self.device.pError))
        )
        return state.value

    def get_enabled_state(self):
        state = c_int8()
        self.device.check_error(
            self.device.lib.VCS_GetEnableState(self.device.handle, self.channel, byref(state),
                                               byref(self.device.pError))
        )
        self.set_raw_value(ATTR_MOTOR_EXCITATION, state.value)
        return state.value

    def get_operation_mode(self):
        operation_mode = c_uint32()
        self.device.check_error(
            self.device.lib.VCS_GetOperationMode(self.device.handle, self.channel, byref(operation_mode),
                                                 byref(self.device.pError))
        )
        self.set_raw_value(ATTR_OPERATION_MODE, self.operation_modes.get(operation_mode.value, None))
        return operation_mode.value

    def get_velocity_units(self):
        dimension = c_uint8()
        notation = c_int8()
        self.device.check_error(
            self.device.lib.VCS_GetVelocityUnits(self.device.handle, self.channel, byref(dimension), byref(notation),
                                                 byref(self.device.pError))
        )
        self.set_raw_value(ATTR_VELOCITY_UNITS, self.velocity_units.inverse.get(notation.value))
        return self.velocity_units.inverse.get(notation.value)

    def set_operation_mode(self, value):
        operation_mode = self.operation_modes.inverse[value]
        self.device.check_error(
            self.device.lib.VCS_SetOperationMode(self.device.handle, self.channel, c_int8(operation_mode),
                                                 byref(self.device.pError))
        )

    def set_velocity(self, velocity):
        self.set_motor_enabled(True)
        self.set_operation_mode(MODE_VELOCITY)
        # self.device.check_error(
        #     self.device.lib.VCS_Mo
        # )

    def set_motor_enabled(self, value):
        '''
        Enable motor for remote control
        @param value: enable flag (0 - Off, 1 - On)
        @type value: int
        '''
        if value:
            self.logger.info("Motor enabled")
            self.device.check_error(
                self.device.lib.VCS_SetEnableState(self.device.handle, self.channel, byref(self.device.pError)))
        else:
            self.logger.info("Motor disabled")
            self.device.check_error(
                self.device.lib.VCS_SetDisableState(self.device.handle, self.channel, byref(self.device.pError)))

    def set_velocity_units(self, value):
        self.set_motor_enabled(False)
        dimension = c_uint8()
        notation = c_int8()
        self.device.check_error(
            self.device.lib.VCS_GetVelocityUnits(self.device.handle, self.channel, byref(dimension), byref(notation),
                                                 byref(self.device.pError))
        )
        notation = c_int8(self.velocity_units.get(value, 0))
        self.device.check_error(
            self.device.lib.VCS_SetVelocityUnits(self.device.handle, self.channel, dimension, notation,
                                                 byref(self.device.pError))
        )
        self.set_motor_enabled(True)

    def stop(self):
        self.device.check_error(
            self.lib.VCS_HaltVelocityMovement(self.device.handle, self.channel, byref(self.device.pError))
        )
