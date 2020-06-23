from xCore import xCore

PCA9554A_REG_INPUT_PORT = 0x00
PCA9554A_REG_OUTPUT_PORT = 0x01
PCA9554A_REG_POL_INVERSION = 0x02
PCA9554A_REG_CONFIG = 0x03

PCA9554A_CONF_OUTPUT = 0x00
PCA9554A_CONF_INPUT = 0xFF

PCA9554A_ALL_OUTPUTS_OFF = 0x00

class xOC03:
    def __init__(self, addr=0x38):
        self.addr = addr
        self.i2c = xCore()

    def init(self, state=PCA9554A_ALL_OUTPUTS_OFF):
        self.writePin(state)
        self.i2c.write_bytes(self.addr, PCA9554A_REG_CONFIG, PCA9554A_CONF_OUTPUT)
        return True

    def writePin(self, state):
        if state is True:
            self.i2c.write_bytes(self.addr, PCA9554A_REG_OUTPUT_PORT, 0x01)
        elif state is False:
            self.i2c.write_bytes(self.addr, PCA9554A_REG_OUTPUT_PORT, 0x00)

    def getStatus(self):
        pin_state = self.i2c.write_read(self.addr, PCA9554A_REG_OUTPUT_PORT, 1)
        return bool(int(pin_state[0]) & 1)
