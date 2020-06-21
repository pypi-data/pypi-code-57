from xCore import xCore

CAP_TOUCH_GENERAL_STATUS = 0x02
CAP_TOUCH_SENSOR_INPUT_STATUS = 0x03

class xSH01:
    def __init__(self, addr=0x28):
        self.addr = addr
        self.i2c = xCore()
        self.init()

    def init(self):
        self.i2c.write_bytes(self.addr, 0x27, 0x00)
        self.i2c.write_bytes(self.addr, 0x21, 0x39)
        self.i2c.write_bytes(self.addr, 0x00, 0x00)

    def touched(self):
        anyButtonTouched = self.i2c.write_read(self.addr, CAP_TOUCH_GENERAL_STATUS, 1)[0]
        #print(anyButtonTouched)
        response = '0'
        if anyButtonTouched == 33:
            #print(anyButtonTouched)
            button = self.i2c.write_read(self.addr, CAP_TOUCH_SENSOR_INPUT_STATUS, 1)[0]
            if button == 0x01:
                #print(button)
                response = 'triangle'
            if button == 0x20:
                #print(button)
                response = 'circle'
            if button == 0x08:
                #print(button)
                response = 'cross'
            if button == 0x10:
                #print(button)
                response = 'square'
            xCore.sleep(100)
            self.i2c.write_bytes(self.addr, 0x00, 0x00)
        else:
            pass
            #print('no touch detected')

        return response