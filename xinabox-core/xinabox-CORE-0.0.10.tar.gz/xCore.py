import sys

def geti2c():
    if sys.platform == "linux":
        import smbus2 as smbus
        return smbus.SMBus(1)

    elif sys.platform == "esp8266":
        from machine import I2C, Pin
        scl=14
        sda=2
        return I2C(scl=Pin(scl), sda=Pin(sda), freq=100000)

    elif sys.platform == "esp32":
        from machine import I2C, Pin
        scl=22
        sda=21
        return I2C(scl=Pin(scl), sda=Pin(sda), freq=100000)

    elif sys.platform == "Atmel SAMD21":
        import board
        import busio
        return busio.I2C(board.SCL, board.SDA)

    elif sys.platform == "microbit":
        from microbit import i2c
        return i2c

class xCore:
    def __init__(self):
        self.i2c=geti2c()

    def write_bytes(self, addr, *args):
        if sys.platform == "linux":
            self.i2c.write_i2c_block_data(addr, args[0], args[1:len(args)])
        elif sys.platform == "esp8266" or sys.platform == "esp32":
            self.i2c.writeto(addr, bytes(args))
        elif sys.platform == "Atmel SAMD21":
            from adafruit_bus_device.i2c_device import I2CDevice
            device = I2CDevice(self.i2c, addr)
            while not self.i2c.try_lock():
                pass
            try:
                device.write(bytearray(args))
            finally:
                self.i2c.unlock()
        elif sys.platform == "microbit":
            self.i2c.write(addr, bytearray(args))

    def write_read(self, addr, reg, length):
        if sys.platform == "linux":
            return self.i2c.read_i2c_block_data(addr, reg, length)
        elif sys.platform == "esp8266" or sys.platform == "esp32":
            self.i2c.writeto(addr, bytearray([reg]))
            return self.i2c.readfrom(addr, length)

        elif sys.platform == "Atmel SAMD21":
            from adafruit_bus_device.i2c_device import I2CDevice
            device = I2CDevice(self.i2c, addr)
            while not self.i2c.try_lock():
                pass
            try:
                device.write(bytearray([reg]))
                buf = bytearray(length)
                device.readinto(buf)
            finally:
                self.i2c.unlock()
            return buf
        elif sys.platform == "microbit":
            self.i2c.write(addr, bytearray([reg]))
            return self.i2c.read(addr, length)

    def write(self):
        pass

    def read(self):
        pass

    def sleep(time_):
        if sys.platform == "microbit":
            import microbit
            microbit.sleep(time_)
        else:
            import time
            time.sleep(time_/1000)
