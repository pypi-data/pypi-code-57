import smbus
import time

class ImageHat():

    # MCP23008 Register
    __IODIR       = 0x00 # I/O DIRECTION (IODIR) REGISTER
    __IPOL        = 0x01 # INPUT POLARITY (IPOL) REGISTER
    __GPINTEN     = 0x02 # INTERRUPT-ON-CHANGE CONTROL (GPINTEN) REGISTER
    __DEFVAL      = 0x03 # DEFAULT COMPARE (DEFVAL) REGISTER FOR INTERRUPT-ONCHANGE
    __INTCON      = 0x04 # INTERRUPT CONTROL (INTCON) REGISTER
    __IOCON       = 0x05 # CONFIGURATION (IOCON) REGISTER
    __GPPU        = 0x06 # PULL-UP RESISTOR CONFIGURATION (GPPU) REGISTER
    __INTF        = 0x07 # INTERRUPT FLAG (INTF) REGISTER
    __INTCAP      = 0x08 # INTERRUPT CAPTURE (INTCAP) REGISTER (Read-only)
    __GPIO        = 0x09 # PORT (GPIO) REGISTER
    __OLAT        = 0x0A # OUTPUT LATCH REGISTER (OLAT)

    # IO Mapping
    __EXT_OUT1    = 0x01 # GPIO0 OUT External output
    __USB3_S      = 0x02 # GPIO1 OUT USB 3.0 host selection
    __USB3_OE     = 0x04 # GPIO2 OUT USB 3.0 switch enable
    __EXT_IN1     = 0x08 # GPIO3 IN  External input
    __USB2_S      = 0x10 # GPIO4 OUT USB 2.0 host selection
    __USB2_OE     = 0x20 # GPIO5 OUT USB 2.0 switch enable
    __VUSB_EN     = 0x40 # GPIP6 OUT USB device power supply enable
    __VHOST2_IN   = 0x80 # GPIO7 IN  Host 2 power state

    def __init__(self, address: int = 0x20):
        if address < 0x20 or address > 0x27:
            raise ValueError("I2C address should be in range [0x20, 0x27]")
        self.__address = address
        self.__smbus = smbus.SMBus(1)
        self.__smbus.write_byte_data(self.__address, self.__IODIR,   0x88)
        self.__smbus.write_byte_data(self.__address, self.__IPOL,    0xFF)
        self.__smbus.write_byte_data(self.__address, self.__GPINTEN, 0x00)
        self.__smbus.write_byte_data(self.__address, self.__DEFVAL,  0x00)
        self.__smbus.write_byte_data(self.__address, self.__INTCON,  0x00)
        self.__smbus.write_byte_data(self.__address, self.__IOCON,   0x00)
        self.__smbus.write_byte_data(self.__address, self.__GPPU,    0xFF)
        self.__smbus.write_byte_data(self.__address, self.__INTF,    0x00)
        # self.__smbus.write_byte_data(self.__address, self.__GPIO,    0x00)
        # self.__smbus.write_byte_data(self.__address, self.__OLAT,    0x00)


    def __eq__(self, other):
        return self.__address == other.__address


    def __str__(self):
        return "{}".format(self.__address)


    def __get_usb_s(self):
        return self.__USB2_S | self.__USB3_S

    __usb_s = property(__get_usb_s)


    def __get_usb_oe(self):
        return self.__USB2_OE | self.__USB3_OE

    __usb_oe = property(__get_usb_oe)


    # HOST2 Power
    def __get_host2_power(self):
        return int(self.__smbus.read_byte_data(self.__address, self.__GPIO) & self.__VHOST2_IN == self.__VHOST2_IN)

    host2_power = property(__get_host2_power)


    # EXT IN1
    def __get_ext_in(self):
        return int(self.__smbus.read_byte_data(self.__address, self.__GPIO) & self.__EXT_IN1 == self.__EXT_IN1)

    ext_in = property(__get_ext_in)


    # EXT OUT1
    def __get_ext_out(self):
        return int(self.__smbus.read_byte_data(self.__address, self.__GPIO) & self.__EXT_OUT1 == self.__EXT_OUT1)

    def __set_ext_out(self, value):
        current_state = self.__smbus.read_byte_data(self.__address, self.__GPIO)
        if value == False:
            new_state = current_state & ~self.__EXT_OUT1
        else:
            new_state = current_state | self.__EXT_OUT1
        if current_state != new_state:
            self.__smbus.write_byte_data(self.__address, self.__GPIO, new_state)

    ext_out = property(__get_ext_out, __set_ext_out)


    # USB Power
    def __get_usb_power(self):
        return int(self.__smbus.read_byte_data(self.__address, self.__GPIO) & self.__VUSB_EN == self.__VUSB_EN)

    def __set_usb_power(self, value):
        current_state = self.__smbus.read_byte_data(self.__address, self.__GPIO)
        if value == False:
           new_state = current_state & ~self.__VUSB_EN
        else:
           new_state = current_state | self.__VUSB_EN
        if current_state != new_state:
            self.__smbus.write_byte_data(self.__address, self.__GPIO, new_state)

    usb_power = property(__get_usb_power, __set_usb_power)


    # USB Host
    def __get_host(self):

        current_state = self.__smbus.read_byte_data(self.__address, self.__GPIO)

        if current_state & self.__usb_oe == self.__usb_oe:
            pass
        elif current_state & self.__usb_oe == 0:
            return 0
        else:
            raise ValueError("Invalid USB OE state")

        if current_state & self.__usb_s == self.__usb_s:
            return 2
        elif current_state & self.__usb_s == 0:
            return 1
        else:
            raise ValueError("Invalid USB S state")

    def __set_host(self, value):

        if value < 0 or value > 2:
            raise ValueError("Host value should be in range [0, 2]")

        current_state = self.__smbus.read_byte_data(self.__address, self.__GPIO)

        # Disconnect data lines
        new_state = current_state & ~self.__usb_oe

        if current_state != new_state:
            self.__smbus.write_byte_data(self.__address, self.__GPIO, new_state)
            current_state = new_state
            time.sleep(0.5)

        # Disconnect USB power supply
        new_state = current_state & ~self.__VUSB_EN

        if current_state != new_state:
            self.__smbus.write_byte_data(self.__address, self.__GPIO, new_state)
            current_state = new_state
            time.sleep(1.0)

        # Select host
        if value == 0:
            return
        elif value == 1:
            new_state = current_state & ~self.__usb_s
        else:
            new_state = current_state | self.__usb_s

        if current_state != new_state:
            self.__smbus.write_byte_data(self.__address, self.__GPIO, new_state)
            current_state = new_state
            time.sleep(0.5)

        # Connect USB power supply
        new_state = current_state | self.__VUSB_EN

        if current_state != new_state:
            self.__smbus.write_byte_data(self.__address, self.__GPIO, new_state)
            current_state = new_state
            time.sleep(1.0)

        # Connect data lines
        new_state = current_state | self.__usb_oe

        if current_state != new_state:
            self.__smbus.write_byte_data(self.__address, self.__GPIO, new_state)
            current_state = new_state
            time.sleep(0.5)

    host = property(__get_host, __set_host)
