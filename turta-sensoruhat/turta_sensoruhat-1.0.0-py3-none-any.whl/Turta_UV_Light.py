# Turta Sensor uHAT Helper for Raspberry Pi OS.
# Distributed under the terms of the MIT license.

# Python Library for Silicon Labs Si1133 UV Index & Ambient Light Sensor.
# Version 1.0.0
# Released: June 14th, 2020

# Visit https://docs.turta.io for documentation.

from enum import IntEnum
import RPi.GPIO as GPIO
from smbus import SMBus
from time import sleep

#Enumerations

#MODES: Operational Modes
class MODES(IntEnum):
    OFF = 0
    INITIALIZATION = 1
    STAND_BY = 2
    FORCED_CONVERSATION = 3
    AUTONOMOUS = 4

class UVAmbientLightSensor:
    """Si1133 UV Index & Ambient Light Sensor"""

    #I2C Slave Address
    I2C_ADDRESS = 0x52

    #Registers
    PART_ID = 0x00
    HW_ID = 0x01
    REV_ID = 0x02
    INFO0 = 0x03
    INFO1 = 0x04
    HOSTIN0 = 0x0A
    HOSTIN1 = 0x09
    HOSTIN2 = 0x08
    HOSTIN3 = 0x07
    COMMAND = 0x0B
    RESET = 0x0F
    RESPONSE1 = 0x10
    RESPONSE0 = 0x11
    IRQ_STATUS = 0x12
    HOSTOUT0 = 0x13
    HOSTOUT1 = 0x14
    HOSTOUT2 = 0x15
    HOSTOUT3 = 0x16
    HOSTOUT4 = 0x17
    HOSTOUT5 = 0x18
    HOSTOUT6 = 0x19
    HOSTOUT7 = 0x1A
    HOSTOUT8 = 0x1B
    HOSTOUT9 = 0x1C
    HOSTOUT10 = 0x1D
    HOSTOUT11 = 0x1E
    HOSTOUT12 = 0x1F
    HOSTOUT13 = 0x20
    HOSTOUT14 = 0x21
    HOSTOUT15 = 0x22
    HOSTOUT16 = 0x23
    HOSTOUT17 = 0x24
    HOSTOUT18 = 0x25
    HOSTOUT19 = 0x26
    HOSTOUT20 = 0x27
    HOSTOUT21 = 0x28
    HOSTOUT22 = 0x29
    HOSTOUT23 = 0x2A
    HOSTOUT24 = 0x2B
    HOSTOUT25 = 0x2C

    #Parameters
    I2CADDR = 0X00
    CHLIST = 0X01
    ADCCONFIG0 = 0X02
    ADCSENS0 = 0X03
    ADCPSOT0 = 0x04
    MEASCONFIG0 = 0x05
    ADCCONFIG1 = 0x06
    ADCSENS1 = 0x07
    ADCPSOT1 = 0x08
    MEASCONFIG1 = 0x09
    ADCCONFIG20 = 0x0A
    ADCSENS2 = 0x0B
    ADCPSOT2 = 0x0C
    MEASCONFIG2 = 0x0D
    ADCCONFIG3 = 0x0E
    ADCSENS3 = 0x0F
    ADCPSOT3 = 0x10
    MEASCONFIG3 = 0x11
    ADCCONFIG4 = 0x12
    ADCSENS4 = 0x13
    ADCPSOT4 = 0x14
    MEASCONFIG4 = 0x15
    ADCCONFIG5 = 0x16
    ADCSENS5 = 0x17
    ADCPSOT5 = 0x18
    MEASCONFIG5 = 0x19
    MEASRATEH = 0x1A
    MEASRATEL = 0x1B
    MEASCOUNT0 = 0x1C
    MEASCOUNT1 = 0x1D
    MEASCOUNT2 = 0x1E
    THRESHOLD0_H = 0x25
    THRESHOLD0_L = 0x26  
    THRESHOLD1_H = 0x27
    THRESHOLD1_L = 0x28
    THRESHOLD2_H = 0x29
    THRESHOLD2_L = 0x2A
    BURST = 0x2B

    #Commands
    RESET_CMD_CTR = 0x00
    RESET_SW = 0x01
    FORCE = 0x11
    PAUSE = 0x12
    START = 0x13
    PARAM_QUERY = 0x40
    PARAM_SET = 0x80

    #Variables
    COUNT0 = 0x40
    COUNT1 = 0x80
    BITS_16 = 0x40
    BITS_24 = 0x00

    #I2C Config
    bus = SMBus(1)

    #Interrupt Pin
    si1133_int = 6

    #I2C Communication

    def _write_register(self, reg_addr, data):
        """Writes data to the I2C device.

        Parameters:
        reg_addr (byte): Write register address
        data (byte): Data to be written to the device"""

        self.bus.write_i2c_block_data(self.I2C_ADDRESS, reg_addr, [ data & 0xFF ])

    def _read_register_1ubyte(self, reg_addr):
        """Reads data from the I2C device.

        Parameters:
        reg_addr (byte): Read register address

        Returns:
        byte: Response from the device"""

        buffer = self.bus.read_i2c_block_data(self.I2C_ADDRESS, reg_addr, 1)
        return buffer[0]

    def _read_2bytes_lsbf(self, reg_addr):
        """Reads data from the I2C device.

        Parameters:
        reg_addr (byte): Read register address

        Returns:
        int: Response from the device, LSB first"""

        buffer = self.bus.read_i2c_block_data(self.I2C_ADDRESS, reg_addr, 2)
        return buffer[0] + (buffer[1] << 8)

    def _read_array(self, reg_addr, cnt):
        """Reads data from the I2C device.

        Parameters:
        reg_addr (byte): Read register start address
        cnt (byte): Read register address

        Returns:
        byte array: Response from the device"""

        return self.bus.read_i2c_block_data(self.I2C_ADDRESS, reg_addr, cnt)

    def _write_parameter(self, parameter, value):
        """Writes value to the parameter register.

        Parameters:
        parameter (byte): Parameter to be updated
        value (byte): Value of the parameter
        
        Returns:
        byte: Response from the device"""

        self._write_register(self.HOSTIN0, value)
        self._write_register(self.COMMAND, (parameter | self.PARAM_SET))
        return self._read_register_1ubyte(self.RESPONSE1)

    def _read_parameter(self, parameter):
        """Reads value from the parameter.

        Parameters:
        parameter (byte): Parameter to be read

        Returns:
        byte: Value of the parameter"""

        self._write_register(self.COMMAND, (parameter | self.PARAM_QUERY))
        return self._read_register_1ubyte(self.RESPONSE1)

    #Initialization

    def __init__(self):
        """Initiates the SI1133 sensor to get light and UV Index data."""

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.si1133_int, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        
        #Reset
        self._reset()
        
        self._set_initial_settings()

        self.is_initialized = True
        sleep(0.5)

    #Sensor Configuration

    def _reset(self):
        """Resets the sensor."""

        self._write_register(self.COMMAND, self.RESET_SW)
        sleep(0.01)
        return

    def _set_initial_settings(self):
        """Writes the initial settings to the sensor."""

        self._write_parameter(self.CHLIST, 0x01)
        self._write_parameter(self.ADCCONFIG0, 0x78)
        self._write_parameter(self.ADCSENS0, 0x09)
        self._write_parameter(self.ADCPSOT0, 0x00)
        self._write_parameter(self.MEASCONFIG0, self.COUNT0)
        self._write_register(self.COMMAND, self.START)
        return

    #Sensor Read Methods

    def read_uv(self):
        """Reads the UV Index value.

        Returns:
        double: UV Index"""

        r1 = self._read_register_1ubyte(self.HOSTOUT0)
        r2 = self._read_register_1ubyte(self.HOSTOUT1)

        uvi = (r1 << 8) | r2

        if (uvi > 545):
            return 14
        else:
            return 0.0082 * (0.00391 * uvi * uvi + uvi)

    def read_ir(self):
        """Reads the IR value.

        Returns:
        int: Raw IR value"""

        r1 = self._read_register_1ubyte(self.HOSTOUT2)
        r2 = self._read_register_1ubyte(self.HOSTOUT3)
        r3 = self._read_register_1ubyte(self.HOSTOUT4)

        ir = (r1 << 16) | (r2 << 8) | r3
        return ir

    #Disposal

    def __del__(self):
        """Releases the resources."""

        try:
            if self.is_initialized:
                self._write_register(self.COMMAND, self.PAUSE)
                del self.is_initialized
        except:
            pass
