from xCore import xCore

GESTURE_THRESHOLD_OUT = 10
GESTURE_SENSITIVITY_1 = 50
GESTURE_SENSITIVITY_2 = 20

ERROR = 0xFF

APDS9960_ID_1 = 0xAB
APDS9960_ID_2 = 0x9C

FIFO_PAUSE_TIME = 30

APDS9960_ENABLE = 0x80
APDS9960_ATIME = 0x81
APDS9960_WTIME = 0x83
APDS9960_AILTL = 0x84
APDS9960_AILTH = 0x85
APDS9960_AIHTL = 0x86
APDS9960_AIHTH = 0x87
APDS9960_PILT = 0x89
APDS9960_PIHT = 0x8B
APDS9960_PERS = 0x8C
APDS9960_CONFIG1 = 0x8D
APDS9960_PPULSE = 0x8E
APDS9960_CONTROL = 0x8F
APDS9960_CONFIG2 = 0x90
APDS9960_ID = 0x92
APDS9960_STATUS = 0x93
APDS9960_CDATAL = 0x94
APDS9960_CDATAH = 0x95
APDS9960_RDATAL = 0x96
APDS9960_RDATAH = 0x97
APDS9960_GDATAL = 0x98
APDS9960_GDATAH = 0x99
APDS9960_BDATAL = 0x9A
APDS9960_BDATAH = 0x9B
APDS9960_PDATA = 0x9C
APDS9960_POFFSET_UR = 0x9D
APDS9960_POFFSET_DL = 0x9E
APDS9960_CONFIG3 = 0x9F
APDS9960_GPENTH = 0xA0
APDS9960_GEXTH = 0xA1
APDS9960_GCONF1 = 0xA2
APDS9960_GCONF2 = 0xA3
APDS9960_GOFFSET_U = 0xA4
APDS9960_GOFFSET_D = 0xA5
APDS9960_GOFFSET_L = 0xA7
APDS9960_GOFFSET_R = 0xA9
APDS9960_GPULSE = 0xA6
APDS9960_GCONF3 = 0xAA
APDS9960_GCONF4 = 0xAB
APDS9960_GFLVL = 0xAE
APDS9960_GSTATUS = 0xAF
APDS9960_IFORCE = 0xE4
APDS9960_PICLEAR = 0xE5
APDS9960_CICLEAR = 0xE6
APDS9960_AICLEAR = 0xE7
APDS9960_GFIFO_U = 0xFC
APDS9960_GFIFO_D = 0xFD
APDS9960_GFIFO_L = 0xFE
APDS9960_GFIFO_R = 0xFF


APDS9960_PON = 0b00000001
APDS9960_AEN = 0b00000010
APDS9960_PEN = 0b00000100
APDS9960_WEN = 0b00001000
APSD9960_AIEN = 0b00010000
APDS9960_PIEN = 0b00100000
APDS9960_GEN = 0b01000000
APDS9960_GVALID = 0b00000001

OFF = 0
ON = 1

POWER = 0
AMBIENT_LIGHT = 1
PROXIMITY = 2
WAIT = 3
AMBIENT_LIGHT_INT = 4
PROXIMITY_INT = 5
GESTURE = 6
ALL = 7

LED_DRIVE_100MA = 0
LED_DRIVE_50MA = 1
LED_DRIVE_25MA = 2
LED_DRIVE_12_5MA = 3

PGAIN_1X = 0
PGAIN_2X = 1
PGAIN_4X = 2
PGAIN_8X = 3

AGAIN_1X = 0
AGAIN_4X = 1
AGAIN_16X = 2
AGAIN_64X = 3

GGAIN_1X = 0
GGAIN_2X = 1
GGAIN_4X = 2
GGAIN_8X = 3

LED_BOOST_100 = 0
LED_BOOST_150 = 1
LED_BOOST_200 = 2
LED_BOOST_300 = 3

GWTIME_0MS = 0
GWTIME_2_8MS = 1
GWTIME_5_6MS = 2
GWTIME_8_4MS = 3
GWTIME_14_0MS = 4
GWTIME_22_4MS = 5
GWTIME_30_8MS = 6
GWTIME_39_2MS = 7

DEFAULT_ATIME = 219
DEFAULT_WTIME = 246
DEFAULT_PROX_PPULSE = 0x87
DEFAULT_GESTURE_PPULSE = 0x89
DEFAULT_POFFSET_UR = 0
DEFAULT_POFFSET_DL = 0
DEFAULT_CONFIG1 = 0x60
DEFAULT_LDRIVE = LED_DRIVE_100MA
DEFAULT_PGAIN = PGAIN_4X
DEFAULT_AGAIN = AGAIN_4X
DEFAULT_PILT = 0
DEFAULT_PIHT = 50
DEFAULT_AILT = 0xFFFF
DEFAULT_AIHT = 0
DEFAULT_PERS = 0x11
DEFAULT_CONFIG2 = 0x01
DEFAULT_CONFIG3 = 0
DEFAULT_GPENTH = 40
DEFAULT_GEXTH = 30
DEFAULT_GCONF1 = 0x40
DEFAULT_GGAIN = GGAIN_4X
DEFAULT_GLDRIVE = LED_DRIVE_100MA
DEFAULT_GWTIME = GWTIME_2_8MS
DEFAULT_GOFFSET = 0
DEFAULT_GPULSE = 0xC9
DEFAULT_GCONF3 = 0
DEFAULT_GIEN = 0


DIR_NONE = 'none'
DIR_LEFT = 'left'
DIR_RIGHT = 'right'
DIR_UP = 'up'
DIR_DOWN = 'down'
DIR_NEAR = 'near'
DIR_FAR = 'far'
DIR_ALL = 'all'

NA_STATE1 = 'na_state1'
NEAR_STATE1 = 'near_state1'
FAR_STATE1 = 'far_state1'
ALL_STATE1 = 'all_state1'

#new_exception(InvalidIdError, ValueError, 'Device ID invalid')


class gestureDataType():
    def __init__(self):
        self.u_data = [0 for x in range(32)]
        self.d_data = [0 for x in range(32)]
        self.l_data = [0 for x in range(32)]
        self.r_data = [0 for x in range(32)]
        self.index = 0
        self.total_gestures = 0
        self.in_threshold = 0
        self.out_threshold = 0


class xSL06:
    def __init__(self, addr=0x39):
        self.i2c = xCore()
        self.addr = addr
        self.gesture_ud_delta_ = 0
        self.gesture_lr_delta_ = 0
        self.gesture_ud_count_ = 0
        self.gesture_lr_count_ = 0
        self.gesture_near_count_ = 0
        self.gesture_far_count_ = 0
        self.gesture_state_ = 0
        self.gesture_motion_ = DIR_NONE
        self.gesture_data_ = gestureDataType()

    def init(self):
        id = self.i2c.write_read(self.addr,APDS9960_ID, 1)[0]
        if not (id == APDS9960_ID_1 or id == APDS9960_ID_2):
            pass
            #raise InvalidIdError

        try:
            self.setMode(ALL, OFF)
            self.i2c.write_bytes(self.addr,APDS9960_WTIME, DEFAULT_WTIME)
            self.i2c.write_bytes(self.addr,APDS9960_PPULSE, DEFAULT_PROX_PPULSE)
            self.i2c.write_bytes(self.addr,APDS9960_POFFSET_UR, DEFAULT_POFFSET_UR)
            self.i2c.write_bytes(self.addr,APDS9960_POFFSET_DL, DEFAULT_POFFSET_DL)
            self.i2c.write_bytes(self.addr,APDS9960_CONFIG1, DEFAULT_CONFIG1)
            self.setLEDDrive(DEFAULT_LDRIVE)
            self.setProximityGain(DEFAULT_PGAIN)
            self.setAmbientLightGain(DEFAULT_AGAIN)
            self.setProxIntLowThresh(DEFAULT_PILT)
            self.setProxIntHighThresh(DEFAULT_PIHT)
            self.setLightIntLowThreshold(DEFAULT_AILT)
            self.setLightIntHighThreshold(DEFAULT_AIHT)
            self.i2c.write_bytes(self.addr,APDS9960_PERS, DEFAULT_PERS)
            self.i2c.write_bytes(self.addr,APDS9960_CONFIG2, DEFAULT_CONFIG2)
            self.i2c.write_bytes(self.addr,APDS9960_CONFIG3, DEFAULT_CONFIG3)
            self.setGestureEnterThresh(DEFAULT_GPENTH)
            self.setGestureExitThresh(DEFAULT_GEXTH)
            self.i2c.write_bytes(self.addr,APDS9960_GCONF1, DEFAULT_GCONF1)
            self.setGestureGain(DEFAULT_GGAIN)
            self.setGestureLEDDrive(DEFAULT_GLDRIVE)
            self.setGestureWaitTime(DEFAULT_GWTIME)
            self.i2c.write_bytes(self.addr,APDS9960_GOFFSET_U, DEFAULT_GOFFSET)
            self.i2c.write_bytes(self.addr,APDS9960_GOFFSET_D, DEFAULT_GOFFSET)
            self.i2c.write_bytes(self.addr,APDS9960_GOFFSET_L, DEFAULT_GOFFSET)
            self.i2c.write_bytes(self.addr,APDS9960_GOFFSET_R, DEFAULT_GOFFSET)
            self.i2c.write_bytes(self.addr,APDS9960_GPULSE, DEFAULT_GPULSE)
            self.i2c.write_bytes(self.addr,APDS9960_GCONF3, DEFAULT_GCONF3)
            self.setGestureIntEnable(DEFAULT_GIEN)

        except Exception as e:
            print(e)
            #raise e
            pass
        return True

    def getMode(self):
        enable_value = 0
        try:
            enable_value = self.i2c.write_read(self.addr,APDS9960_ENABLE, 1)[0]
        except:
            return ERROR
        return enable_value

    def setMode(self, mode, enable):
        reg_val = self.getMode()
        if reg_val == ERROR:
            raise ValueError

        enable = enable & 0x01

        if mode >= 0 and mode <= 6:
            if enable == 1:
                reg_val = reg_val | (1 << mode)
            else:
                reg_val = reg_val & ~(1 << mode)

        elif mode == ALL:
            if enable == 1:
                reg_val = 0x7F
            else:
                reg_val = 0x00

        try:
            self.i2c.write_bytes(self.addr,APDS9960_ENABLE, reg_val)
        except Exception as e:
            #raise e
            pass

        return True

    def enableLightSensor(self, interrupts=False):
        self.setAmbientLightGain(DEFAULT_AGAIN)
        if interrupts == True:
            self.setAmbientLightIntEnable(1)
        else:
            self.setAmbientLightIntEnable(0)

        self.enablePower()
        self.setMode(AMBIENT_LIGHT, 1)

    def disableLightSensor(self):
        self.setAmbientLightIntEnable(0)
        self.setmode(AMBIENT_LIGHT, 0)

    def enableProximitySensor(self, interrupts=False):
        self.setProximityGain(DEFAULT_PGAIN)
        self.setLEDDrive(DEFAULT_LDRIVE)
        if interrupts == True:
            self.setProximityIntEnable(1)
        else:
            self.setProximityIntEnable(0)
        self.enablePower()
        self.setMode(PROXIMITY, 1)

    def disableProximitySensor(self):
        self.setProximityIntEnable(0)
        self.setMode(PROXIMITY, 0)

    def enableGestureSensor(self, interrupts=False):
        try:
            self.resetGestureParameters()
            self.i2c.write_bytes(self.addr,APDS9960_WTIME, 0xFF)
            self.setLEDBoost(LED_BOOST_300)
            if interrupts == True:
                self.setGestureIntEnable(1)
            else:
                self.setGestureIntEnable(0)
            self.setGestureMode(1)
            self.enablePower()
            self.setMode(WAIT, 1)
            self.setMode(PROXIMITY, 1)
            self.setMode(GESTURE, 1)
        except Exception as e:
            #raise e
            pass

    def disableGestureSensor(self):
        try:
            self.resetGestureParameters()
            self.setGestureIntEnable(0)
            self.setGestureMode(0)
            self.setMode(GESTURE, 0)
        except Exception as e:
            #raise e
            pass

    def isGestureAvailable(self):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_GSTATUS, 1)[0]
        except:
            return ERROR
        val &= APDS9960_GVALID

        if val == 1:
            return True
        else:
            return False

    def getGesture(self):
        fifo_level = 0
        fifo_data = []

        mode = self.getMode() & 0b01000001
        if not self.isGestureAvailable() or not mode:
            return DIR_NONE

        while True:

            xCore.sleep(FIFO_PAUSE_TIME)

            try:
                gstatus = self.i2c.write_read(self.addr,APDS9960_GSTATUS, 1)[0]
            except Exception as e:
                #raise e
                pass

            if (gstatus & APDS9960_GVALID) == APDS9960_GVALID:

                try:
                    fifo_level = self.i2c.write_read(self.addr,APDS9960_GFLVL, 1)[0]
                except Exception as e:
                    #raise e
                    pass

                if fifo_level > 0:

                    try:
                        fifo_data = self.i2c.write_read(self.addr,
                            APDS9960_GFIFO_U, fifo_level * 4)
                    except Exception as e:
                        #raise e
                        pass
                    if len(fifo_data) >= 4:
                        for i in range(0, len(fifo_data), 4):
                            self.gesture_data_.u_data[self.gesture_data_.index] = fifo_data[i + 0]
                            self.gesture_data_.d_data[self.gesture_data_.index] = fifo_data[i + 1]
                            self.gesture_data_.l_data[self.gesture_data_.index] = fifo_data[i + 2]
                            self.gesture_data_.r_data[self.gesture_data_.index] = fifo_data[i + 3]
                            self.gesture_data_.index += 1
                            self.gesture_data_.total_gestures += 1

                        if self.processGestureData():
                            if self.decodeGesture():
                                pass

                        self.gesture_data_.index = 0
                        self.gesture_data_.total_gestures = 0
            else:

                xCore.sleep(FIFO_PAUSE_TIME)
                if not self.decodeGesture():
                    pass

                motion = self.gesture_motion_

                self.resetGestureParameters()
                return motion

    def enablePower(self):
        self.setMode(POWER, 1)

    def disablePower(self):
        self.setMode(POWER, 0)

    def getAmbientLight(self):
        try:
            val_l = self.i2c.write_read(self.addr,APDS9960_CDATAL, 1)[0]
            val_h = self.i2c.write_read(self.addr,APDS9960_CDATAH, 1)[0]
        except Exception as e:
            #raise e
            pass

        return val_l + (val_h << 8)

    def getRedLight(self):

        try:
            val_l = self.i2c.write_read(self.addr,APDS9960_RDATAL, 1)[0]
            val_h = self.i2c.write_read(self.addr,APDS9960_RDATAH, 1)[0]
        except Exception as e:
            #raise e
            pass

        return val_l + (val_h << 8)

    def getBlueLight(self):
        try:
            val_l = self.i2c.write_read(self.addr,APDS9960_GDATAL, 1)[0]
            val_h = self.i2c.write_read(self.addr,APDS9960_GDATAH, 1)[0]
        except Exception as e:
            #raise e
            pass

        return val_l + (val_h << 8)

    def getGreenLight(self):
        try:
            val_l = self.i2c.write_read(self.addr,APDS9960_BDATAL, 1)[0]
            val_h = self.i2c.write_read(self.addr,APDS9960_BDATAH, 1)[0]
        except Exception as e:
            #raise e
            pass

        return val_l + (val_h << 8)

    def getProximity(self):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_PDATA, 1)[0]
        except Exception as e:
            #raise e
            pass

        return val

    def resetGestureParameters(self):

        self.gesture_data_.index = 0
        self.gesture_data_.total_gestures = 0

        self.gesture_ud_delta_ = 0
        self.gesture_lr_delta_ = 0

        self.gesture_ud_count_ = 0
        self.gesture_lr_count_ = 0

        self.gesture_near_count_ = 0
        self.gesture_far_count_ = 0

        self.gesture_state_ = 0
        self.gesture_motion_ = DIR_NONE

    def processGestureData(self):

        u_first = 0
        d_first = 0
        l_first = 0
        r_first = 0
        u_last = 0
        d_last = 0
        l_last = 0
        r_last = 0

        if self.gesture_data_.total_gestures <= 4:
            return False

        if self.gesture_data_.total_gestures <= 32 and self.gesture_data_.total_gestures > 0:

            for i in range(0, self.gesture_data_.total_gestures):

                if (self.gesture_data_.u_data[i] > GESTURE_THRESHOLD_OUT) and (self.gesture_data_.d_data[i] > GESTURE_THRESHOLD_OUT) and (self.gesture_data_.l_data[i] > GESTURE_THRESHOLD_OUT) and (self.gesture_data_.r_data[i] > GESTURE_THRESHOLD_OUT):
                    u_first = self.gesture_data_.u_data[i]
                    d_first = self.gesture_data_.d_data[i]
                    l_first = self.gesture_data_.l_data[i]
                    r_first = self.gesture_data_.r_data[i]
                    break

            if (u_first == 0) or (d_first == 0) or (l_first == 0) or (r_first == 0):
                return False
            l = range(self.gesture_data_.total_gestures)
            l = l[::-1]
            for i in l:
                if (self.gesture_data_.u_data[i] > GESTURE_THRESHOLD_OUT) and (self.gesture_data_.d_data[i] > GESTURE_THRESHOLD_OUT) and (self.gesture_data_.l_data[i] > GESTURE_THRESHOLD_OUT) and (self.gesture_data_.r_data[i] > GESTURE_THRESHOLD_OUT):

                    u_last = self.gesture_data_.u_data[i]
                    d_last = self.gesture_data_.d_data[i]
                    l_last = self.gesture_data_.l_data[i]
                    r_last = self.gesture_data_.r_data[i]

                    break

        ud_ratio_first = ((u_first - d_first) * 100) / (u_first + d_first)
        lr_ratio_first = ((l_first - r_first) * 100) / (l_first + r_first)
        ud_ratio_last = ((u_last - d_last) * 100) / (u_last + d_last)
        lr_ratio_last = ((l_last - r_last) * 100) / (l_last + r_last)
        ud_delta = ud_ratio_last - ud_ratio_first
        lr_delta = lr_ratio_last - lr_ratio_first

        self.gesture_ud_delta_ += ud_delta
        self.gesture_lr_delta_ += lr_delta

        if self.gesture_ud_delta_ >= GESTURE_SENSITIVITY_1:
            self.gesture_ud_count_ = 1
        elif self.gesture_ud_delta_ <= -GESTURE_SENSITIVITY_1:
            self.gesture_ud_count_ = -1
        else:
            self.gesture_ud_count_ = 0

        if self.gesture_lr_delta_ >= GESTURE_SENSITIVITY_1:
            self.gesture_lr_count_ = 1
        elif self.gesture_lr_delta_ <= -GESTURE_SENSITIVITY_1:
            self.gesture_lr_count_ = -1
        else:
            self.gesture_lr_count_ = 0

        if (self.gesture_ud_count_ == 0) and (self.gesture_lr_count_ == 0):
            if (abs(ud_delta) < GESTURE_SENSITIVITY_2) and (abs(lr_delta) < GESTURE_SENSITIVITY_2):

                if (ud_delta == 0) and (lr_delta == 0):
                    self.gesture_near_count_ += 1
                elif ud_delta != 0 or lr_delta != 0:
                    self.gesture_far_count_ += 1

                if (self.gesture_near_count_ >= 10) and (self.gesture_far_count_ >= 2):
                    if (ud_delta == 0) and (lr_delta == 0):
                        self.gesture_state_ = NEAR_STATE1
                    elif ud_delta != 0 and lr_delta != 0:
                        self.gesture_state_ = FAR_STATE1

                    return True

        else:
            if (abs(ud_delta) < GESTURE_SENSITIVITY_2) and (abs(lr_delta) < GESTURE_SENSITIVITY_2):

                if (ud_delta == 0) and (lr_delta == 0):
                    self.gesture_near_count_ += 1

                if self.gesture_near_count_ >= 10:
                    self.gesture_ud_count_ = 0
                    self.gesture_lr_count_ = 0
                    self.gesture_ud_delta_ = 0
                    self.gesture_lr_delta_ = 0

        return False

    def decodeGesture(self):
        try:

            if self.gesture_state_ == NEAR_STATE1:
                self.gesture_motion_ = DIR_NEAR
                return True
            elif self.gesture_state_ == FAR_STATE1:
                self.gesture_motion_ = DIR_FAR
                return True

            if (self.gesture_ud_count_ == -1) and (self.gesture_lr_count_ == 0):
                self.gesture_motion_ = DIR_UP
            elif (self.gesture_ud_count_ == 1) and (self.gesture_lr_count_ == 0):
                self.gesture_motion_ = DIR_DOWN
            elif (self.gesture_ud_count_ == 0) and (self.gesture_lr_count_ == 1):
                self.gesture_motion_ = DIR_RIGHT
            elif (self.gesture_ud_count_ == 0) and (self.gesture_lr_count_ == -1):
                self.gesture_motion_ = DIR_LEFT
            elif (self.gesture_ud_count_ == -1) and (self.gesture_lr_count_ == 1):
                if abs(self.gesture_ud_delta_) > abs(self.gesture_lr_delta_):
                    self.gesture_motion_ = DIR_UP
                else:
                    self.gesture_motion_ = DIR_RIGHT

            elif (self.gesture_ud_count_ == 1) and (self.gesture_lr_count_ == -1):
                if abs(self.gesture_ud_delta_) > abs(self.gesture_lr_delta_):
                    self.gesture_motion_ = DIR_DOWN
                else:
                    self.gesture_motion_ = DIR_LEFT

            elif (self.gesture_ud_count_ == -1) and (self.gesture_lr_count_ == -1):
                if abs(self.gesture_ud_delta_) > abs(self.gesture_lr_delta_):
                    self.gesture_motion_ = DIR_UP
                else:
                    self.gesture_motion_ = DIR_LEFT

            elif (self.gesture_ud_count_ == 1) and (self.gesture_lr_count_ == 1):
                if abs(self.gesture_ud_delta_) > abs(self.gesture_lr_delta_):
                    self.gesture_motion_ = DIR_DOWN
                else:
                    self.gesture_motion_ = DIR_RIGHT

            else:
                self.gesture_motion_ = DIR_NONE
                return False

            return True

        except Exception as e:
            print(e)
            return False

    def getProxIntLowThresh(self):
        val = 0
        try:
            self.i2c.write_read(self.addr,APDS9960_PILT, 1)[0]
        except Exception as e:
            #raise e
            pass

        return val

    def setProxIntLowThresh(self, threshold):
        try:
            self.i2c.write_bytes(self.addr,APDS9960_PILT, threshold)
        except Exception as e:
            #raise e
            pass

        return True

    def getProxIntHighThresh(self):
        try:
            val = self.i2c.write_read(self.addr,APDS9960_PIHT, 1)[0]
        except Exception as e:
            #raise e
            pass

        return val

    def setProxIntHighThresh(self, threshold):
        try:
            self.i2c.write_bytes(self.addr,APDS9960_PIHT, threshold)
        except Exception as e:
            #raise e
            pass

        return True

    def getLEDDrive(self):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_CONTROL, 1)[0]
        except:
            return ERROR

        return (val >> 6) & 0b00000011

    def setLEDDrive(self, drive):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_CONTROL, 1)[0]
        except PeripheralError as e:
            #raise e
            pass

        drive = drive & 0b00000011
        drive = drive << 6
        val = val & 0b00111111
        val = val | drive

        try:
            self.i2c.write_bytes(self.addr,APDS9960_CONTROL, val)
        except PeripheralError as e:
            #raise e
            pass

        return True

    def getProximityGain(self):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_CONTROL, 1)[0]
        except Exception as e:
            #raise e
            pass

        val = (val >> 2) & 0b00000011

        return val

    def setProximityGain(self, drive):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_CONTROL, 1)[0]
        except PeripheralError as e:
            #raise e
            pass

        drive = drive & 0b00000011
        drive = drive << 2
        val = val & 0b11110011
        val = val | drive

        try:
            self.i2c.write_bytes(self.addr,APDS9960_CONTROL, val)
        except PeripheralError as e:
            #raise e
            pass

        return True

    def getAmbientLightGain(self):
        try:
            val = self.i2c.write_read(self.addr,APDS9960_CONTROL, 1)[0]
        except Exception as e:
            #raise e
            pass

        val &= 0b00000011

        return val

    def setAmbientLightGain(self, drive):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_CONTROL, 1)[0]
        except PeripheralError as e:
            #raise e
            pass

        drive = drive & 0b00000011
        val = val & 0b11111100
        val = val | drive

        try:
            self.i2c.write_bytes(self.addr,APDS9960_CONTROL, val)
        except Exception as e:
            #raise e
            pass

        return True

    def getLEDBoost(self):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_CONFIG2, 1)[0]
        except Exception as e:
            #raise e
            pass

        val = (val >> 4) & 0b00000011
        return val

    def setLEDBoost(self, boost):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_CONFIG2, 1)[0]
        except Exception as e:
            #raise e
            pass

        boost &= 0b00000011
        boost = boost << 4
        val &= 0b11001111
        val |= boost

        try:
            self.i2c.write_bytes(self.addr,APDS9960_CONFIG2, val)
        except Exception as e:
            #raise e
            pass

    def getProxGainCompEnable(self):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_CONFIG3, 1)[0]
        except Exception as e:
            #raise e
            pass

        val = (val >> 5) & 0b00000001

        return val

        def setProxIntLowThresh(self, threshold):
            try:
                self.i2c.write_bytes(self.addr,APDS9960_PILT, threshold)
            except PeripheralError as e:
                #raise e
                pass

            return True

    def setProxGainCompEnable(self, enable):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_CONFIG3, 1)[0]
        except Exception as e:
            #raise e
            pass

        enable &= 0b00000001
        enable = enable << 5
        val &= 0b11011111
        val |= enable

        try:
            self.i2c.write_bytes(self.addr,APDS9960_CONFIG3, val)
        except Exception as e:
            #raise e
            pass

    def getProxPhotoMask(self):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_CONFIG3, 1)[0]
        except Exception as e:
            #raise e
            pass

        val &= 0b00001111

        return val

    def setProxPhotoMask(self, mask):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_CONFIG3, 1)[0]
        except Exception as e:
            #raise e
            pass

        mask &= 0b00001111
        val &= 0b11110000
        val |= mask

        try:
            self.i2c.write_bytes(self.addr,APDS9960_CONFIG3, val)
        except Exception as e:
            #raise e
            pass

    def getGestureEnterThresh(self):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_GPENTH, 1)[0]
        except Exception as e:
            #raise e
            pass

        return val

    def setGestureEnterThresh(self, threshold):

        try:
            self.i2c.write_bytes(self.addr,APDS9960_GPENTH, threshold)
        except Exception as e:
            #raise e
            pass

    def getGestureExitThresh(self):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_GEXTH, 1)[0]
        except Exception as e:
            #raise e
            pass

        return val

    def setGestureExitThresh(self, threshold):
        try:
            self.i2c.write_bytes(self.addr,APDS9960_GEXTH, threshold)
        except Exception as e:
            #raise e
            pass

    def getGestureGain(self):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_GCONF2, 1)
        except Exception as e:
            #raise e
            pass

        val = (val >> 5) & 0b00000011

        return val

    def setGestureGain(self, gain):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_GCONF2, 1)[0]
        except Exception as e:
            #raise e
            pass

        gain &= 0b00000011
        gain = gain << 5
        val &= 0b10011111
        val |= gain
        try:
            self.i2c.write_bytes(self.addr,APDS9960_GCONF2, val)

        except Exception as e:
            #raise e
            pass

    def getGestureLEDDrive(self):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_GCONF2, 1)[0]
        except Exception as e:
            #raise e
            pass

        val = (val >> 3) & 0b00000011

        return val

    def setGestureLEDDrive(self, drive):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_GCONF2, 1)[0]
        except Exception as e:
            #raise e
            pass

        drive &= 0b00000011
        drive = drive << 3
        val &= 0b11100111
        val |= drive
        try:
            self.i2c.write_bytes(self.addr,APDS9960_GCONF2, val)
        except Exception as e:
            #raise e
            pass

    def getGestureWaitTime(self):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_GCONF2, 1)[0]
        except Exception as e:
            #raise e
            pass

        val &= 0b00000111

        return val

    def setGestureWaitTime(self, time):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_GCONF2, 1)[0]
        except Exception as e:
            #raise e
            pass

        time &= 0b00000111
        val &= 0b11111000
        val |= time

        try:
            self.i2c.write_bytes(self.addr,APDS9960_GCONF2, val)
        except Exception as e:
            #raise e
            pass

    def getLightIntLowThreshold(self):
        valLow = 0
        try:
            val_low = self.i2c.write_read(self.addr,APDS9960_AILTL, 1)[0]
            val_high = self.i2c.write_read(self.addr,APDS9960_AILTH, 1)[0]
        except Exception as e:
            #raise e
            pass

        return val_low + (val_high << 8)

    def setLightIntLowThreshold(self, threshold):
        val_low = 0
        val_high = 0
        val_low = threshold & 0x00FF
        val_high = (threshold & 0xFF00) >> 8

        try:
            self.i2c.write_bytes(self.addr,APDS9960_AILTL, val_low)
            self.i2c.write_bytes(self.addr,APDS9960_AILTH, val_high)
        except PeripheralError as e:
            #raise e
            pass

            return True

    def getLightIntHighThreshold(self):
        val_low = 0
        val_high = 0
        try:
            val_low = self.i2c.write_read(self.addr,APDS9960_AIHTL, 1)[0]
            val_high = self.i2c.write_read(self.addr,APDS9960_AIHTH, 1)[0]
        except Exception as e:
            #raise e
            pass

        return val_low + (val_high << 8)

    def setLightIntHighThreshold(self, threshold):
        val_low = 0
        val_high = 0
        val_low = threshold & 0x00FF
        val_high = (threshold & 0xFF00) >> 8

        try:
            self.i2c.write_bytes(self.addr,APDS9960_AIHTL, val_low)
            self.i2c.write_bytes(self.addr,APDS9960_AIHTH, val_high)
        except Exception as e:
            #raise e
            pass

        return True

    def getProximityIntLowThreshold(self, threshold):
        try:
            threshold = self.i2c.write_read(self.addr,APDS9960_PILT, 1)[0]
        except Exception as e:
            #raise e
            pass
        return True

    def setProximityIntLowThreshold(self, threshold):
        try:
            self.i2c.write_bytes(self.addr,APDS9960_PILT, threshold)
        except Exception as e:
            #raise e
            pass
        return True

    def getProximityIntHighThreshold(self, threshold):
        try:
            threshold = self.i2c.write_read(self.addr,APDS9960_PIHT, 1)[0]
        except PeripheralError as e:
            #raise e
            pass
        return True

    def setProximityIntHighThreshold(self, threshold):
        try:
            self.i2c.write_bytes(self.addr,APDS9960_PIHT, threshold)
        except PeripheralError as e:
            #raise e
            pass
        return True

    def getAmbientLightIntEnable(self):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_ENABLE, 1)[0]
        except:
            return ERROR

        val = (val >> 4) & 0b00000001
        return val

    def setAmbientLightIntEnable(self, enable):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_ENABLE, 1)[0]
        except Exception as e:
            #raise e
            pass

        enable = enable & 0b00000001
        enable = enable << 4
        val = val & 0b11101111
        val = val | enable

        try:
            self.i2c.write_bytes(self.addr,APDS9960_ENABLE, val)
        except Exception as e:
            #raise e
            pass

        return True

    def getProximityIntEnable(self):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_ENABLE, 1)[0]
        except:
            return ERROR
        val = (val >> 5) & 0b00000001
        return val

    def setProximityIntEnable(self, enable):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_ENABLE, 1)[0]
        except Exception as e:
            #raise e
            pass

        enable = enable & 0b00000001
        enable = enable << 5
        val = val & 0b11011111
        val = val | enable

        try:
            self.i2c.write_bytes(self.addr,APDS9960_ENABLE, val)
        except Exception as e:
            #raise e
            pass

        return True

    def getGestureIntEnable(self):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_GCONF4, 1)[0]
        except:
            return ERROR

        val = (val >> 1) & 0b00000001
        return val

    def setGestureIntEnable(self, enable):
        val = 0
        try:
            self.i2c.write_read(self.addr,APDS9960_GCONF4, 1)[0]
        except Exception as e:
            #raise e
            pass

        enable = enable & 0b00000001
        enable = enable << 1
        val = val & 0b11111101
        val = val | enable

        try:
            self.i2c.write_bytes(self.addr,APDS9960_GCONF4, val)
        except Exception as e:
            #raise e
            pass

        return True

    def clearAmbientLightInt(self):
        throwaway = 0
        try:
            throwaway = self.i2c.write_read(self.addr,APDS9960_AICLEAR, 1)[0]
        except Exception as e:
            #raise e
            pass
        return True

    def clearProximityInt(self):
        throwaway = 0
        try:
            throwaway = self.i2c.write_read(self.addr,APDS9960_PICLEAR, 1)[0]
        except Exception as e:
            #raise e
            pass
        return True

    def getGestureMode(self, mode):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_GCONF4, 1)[0]
        except:
            return ERROR
        val &= 0b00000001
        return val

    def setGestureMode(self, mode):
        val = 0
        try:
            val = self.i2c.write_read(self.addr,APDS9960_GCONF4, 1)[0]
        except Exception as e:
            #raise e
            pass

        mode = mode & 0b00000001
        val = val & 0b11111110
        val = val | mode

        try:
            self.i2c.write_bytes(self.addr,APDS9960_GCONF4, val)
        except Exception as e:
            #raise e
            pass

        return True
