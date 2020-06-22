from xCore import xCore
import math

PCA9685_I2C_ADDR = 0x78
PCA9685_PRESCALE = 0xFE
PCA9685_MODE_1 = 0x00
PCA9685_MODE_1_DEF = 0x01
PCA9685_MODE_2 = 0x01
PCA9685_MODE_2_DEF = 0x04
PCA9685_SLEEP = PCA9685_MODE_1_DEF | 0x10
PCA9685_WAKE = PCA9685_MODE_1_DEF & 0xEF
PCA9685_RESTART = PCA9685_WAKE | 0x80
PCA9685_ALL_LED_ON_L = 0xFA
PCA9685_ALL_LED_ON_H = 0xFB
PCA9685_ALL_LED_OFF_L = 0xFC
PCA9685_ALL_LED_OFF_H = 0xFD
PinRegDistance = 4
PCA9685_LED8_ON_L = 0x26
PCA9685_LED8_ON_H = 0x27
PCA9685_LED8_OFF_L = 0x28
PCA9685_LED8_OFF_H = 0x29

class xOC05:
    def __init__(self, addr=PCA9685_I2C_ADDR):
        self.addr = addr
        self.i2c = xCore()
        self.frequency = 0

    def init(self, outFreq=60):
        if outFreq > 1000:
            self.frequency = 1000
        elif outFreq < 40:
            self.frequency = 40
        else:
            self.frequency = outFreq
        prescaler = self.calcFreqPrescaler(self.frequency)
        try:
            self.i2c.write_bytes(self.addr, PCA9685_MODE_1, PCA9685_SLEEP)
            self.i2c.write_bytes(self.addr, PCA9685_PRESCALE, prescaler)
            self.i2c.write_bytes(self.addr, PCA9685_LED8_ON_L, 0x00)
            self.i2c.write_bytes(self.addr, PCA9685_LED8_ON_H, 0x00)
            self.i2c.write_bytes(self.addr, PCA9685_LED8_OFF_L, 0x00)
            self.i2c.write_bytes(self.addr, PCA9685_LED8_OFF_H, 0x00)
            self.i2c.write_bytes(self.addr, PCA9685_MODE_1, PCA9685_WAKE)
            self.i2c.sleep(1000)
            self.i2c.write_bytes(self.addr, PCA9685_MODE_1, PCA9685_RESTART)
        except Exception as e:
            print(e)

    def setServoPosition(self, channelNum, degrees):
        channelNum = max(1, min(8, channelNum))
        degrees = max(0, min(180, degrees))
        pwm = self.degrees180ToPWM(self.frequency, degrees, 5, 25)

        return self.setPinPulseRange(channelNum, 0, pwm)

    def setPinPulseRange(self, pinNum, onStep=0, offStep=2048):
        pinNumber = max(1, min(8, pinNum))
        pinOffset = (PinRegDistance * (pinNumber - 1))
        onStep = max(0, min(4095, onStep))
        offStep = max(0, min(4095, offStep))
        try:
            # Low byte of onStep
            self.i2c.write_bytes(self.addr, pinOffset + PCA9685_LED8_ON_L, onStep & 0xFF)

            # High byte of onStep
            self.i2c.write_bytes(self.addr, pinOffset + PCA9685_LED8_ON_H, (onStep >> 8))

            # Low byte of offStep
            self.i2c.write_bytes(self.addr, pinOffset + PCA9685_LED8_OFF_L, offStep & 0xFF)

            # High byte of offStep
            self.i2c.write_bytes(self.addr, pinOffset + PCA9685_LED8_OFF_H, (offStep >> 8))
        except Exception as e:
            print(e)

    def setCRServoPosition(self, channelNum, speed):
        isReverse = False
        pwm = 0
        channelnum = max(1, min(8, channelNum))
        offsetStart = self.calcFreqOffset(self.frequency, 5)
        offsetMid = self.calcFreqOffset(self.frequency, 15)
        offsetEnd = self.calcFreqOffset(self.frequency, 25)
        if speed == 0:
            return self.setPinPulseRange(channelnum, 0, offsetMid)

        if speed < 0:
            isReverse = True
        if isReverse:
            spread = offsetMid - offsetStart
        else:
            spread = offsetEnd - offsetMid

        speed = math.abs(speed)
        calcOffset = ((speed * spread) / 100)

        if isReverse:
            pwm = offsetMid - calcOffset
        else:
            pwm = offsetMid + calcOffset
        return self.setPinPulseRange(channelnum, 0, pwm)

    def calcFreqPrescaler(self, freq):
        return int(math.floor((25000000 / (freq * 4096))) - 1)

    def calcFreqOffset(self, freq, offset):
        return ((offset * 1000) / (1000 / freq) * 4096) / 10000

    def degrees180ToPWM(self, freq, degrees, offsetStart, offsetEnd):
        offsetEnd = self.calcFreqOffset(freq, offsetEnd)
        offsetStart = self.calcFreqOffset(freq, offsetStart)
        spread = offsetEnd - offsetStart
        calcOffset = ((degrees * spread) / 180) + offsetStart
        return int(max(offsetStart, min(offsetEnd, calcOffset)))