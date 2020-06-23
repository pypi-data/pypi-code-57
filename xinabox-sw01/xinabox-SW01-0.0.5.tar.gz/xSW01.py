from xCore import xCore

def _tc(v, n_bit=16):
    mask = 2**(n_bit - 1)
    return -(v & mask) + (v & ~mask)

class xSW01:
    def __init__(self, addr=0x76):
        self.i2c = xCore()
        self.addr = addr
        self._read_coeff()
        self.setup()

    def setup(self, mode = 3, os_t = 1, os_h = 1, os_p = 1, t_sb = 6, filter = 1):
        mode = mode & 3

        os_t = os_t & 7
        os_h = os_h & 7
        os_p = os_p & 7

        t_sb = t_sb & 7

        filter = filter & 7

        self.i2c.write_bytes(self.addr, 0xF2, os_h)
        self.i2c.write_bytes(self.addr, 0xF4, (os_t << 5) | (os_p << 2) | mode )
        self.i2c.write_bytes(self.addr, 0xF5, (t_sb << 5) | (filter << 2) )

    def _read_coeff(self):
        dig_T1 = self.i2c.write_read(self.addr, 0x88,2)
        dig_T2 = self.i2c.write_read(self.addr, 0x8A,2)
        dig_T3 = self.i2c.write_read(self.addr, 0x8C,2)

        self.dig_T1 = dig_T1[0] | (dig_T1[1]<<8)
        self.dig_T2 = _tc(dig_T2[0] | (dig_T2[1]<<8))
        self.dig_T3 = _tc(dig_T3[0] | (dig_T3[1]<<8))


        dig_P1 = self.i2c.write_read(self.addr, 0x8E,2)
        dig_P2 = self.i2c.write_read(self.addr, 0x90,2)
        dig_P3 = self.i2c.write_read(self.addr, 0x92,2)
        dig_P4 = self.i2c.write_read(self.addr, 0x94,2)
        dig_P5 = self.i2c.write_read(self.addr, 0x96,2)
        dig_P6 = self.i2c.write_read(self.addr, 0x98,2)
        dig_P7 = self.i2c.write_read(self.addr, 0x9A,2)
        dig_P8 = self.i2c.write_read(self.addr, 0x9C,2)
        dig_P9 = self.i2c.write_read(self.addr, 0x9E,2)

        self.dig_P1 = dig_P1[0] | (dig_P1[1]<<8)
        self.dig_P2 = _tc(dig_P2[0] | (dig_P2[1]<<8))
        self.dig_P3 = _tc(dig_P3[0] | (dig_P3[1]<<8))
        self.dig_P4 = _tc(dig_P4[0] | (dig_P4[1]<<8))
        self.dig_P5 = _tc(dig_P5[0] | (dig_P5[1]<<8))
        self.dig_P6 = _tc(dig_P6[0] | (dig_P6[1]<<8))
        self.dig_P7 = _tc(dig_P7[0] | (dig_P7[1]<<8))
        self.dig_P8 = _tc(dig_P8[0] | (dig_P8[1]<<8))
        self.dig_P9 = _tc(dig_P9[0] | (dig_P9[1]<<8))


        dig_H1 = self.i2c.write_read(self.addr, 0xA1,1)
        dig_H2 = self.i2c.write_read(self.addr, 0xE1,2)
        dig_H3 = self.i2c.write_read(self.addr, 0xE3,1)
        dig_H4 = self.i2c.write_read(self.addr, 0xE4,2)
        dig_H5 = self.i2c.write_read(self.addr, 0xE5,2)
        dig_H6 = self.i2c.write_read(self.addr, 0xE7,1)

        self.dig_H1 = dig_H1[0]
        self.dig_H2 = _tc(dig_H2[0] | (dig_H2[1]<<8))
        self.dig_H3 = dig_H3[0]
        self.dig_H4 = _tc((dig_H4[0] << 4) | (dig_H4[1] & 0xF))
        self.dig_H5 = _tc((dig_H5[1] << 4) | (dig_H5[0] >> 4))
        self.dig_H6 = _tc(dig_H6[0],8)

    def _calc_temp(self,adc_t):
        if adc_t == 0x80000:
            return 0
        var1 = (((adc_t>>3) - (self.dig_T1 <<1)) * self.dig_T2) >> 11
        var2 = (((((adc_t>>4) - (self.dig_T1)) * ((adc_t>>4) - (self.dig_T1))) >> 12) * (self.dig_T3)) >> 14

        t_fine = var1 + var2;
        self.t_fine = t_fine
        T = (t_fine * 5 + 128) >> 8
        return T/100

    def _calc_hum(self,adc_h):
        if adc_h == 0x8000:
            return 0

        v_x1_u32r = self.t_fine - 76800
        v_x1_u32r = (((((adc_h << 14) - (self.dig_H4 << 20) -
                        (self.dig_H5 * v_x1_u32r)) + 16384) >> 15) *
                     (((((((v_x1_u32r * self.dig_H6) >> 10) *
                          (((v_x1_u32r * self.dig_H3) >> 11) + 32768)) >> 10) +
                        2097152) * self.dig_H2 + 8192) >> 14))

        v_x1_u32r = (v_x1_u32r - (((((v_x1_u32r >> 15) * (v_x1_u32r >> 15)) >> 7) *
                                   self.dig_H1) >> 4))

        v_x1_u32r = 0 if v_x1_u32r <0 else v_x1_u32r
        v_x1_u32r = 419430400 if v_x1_u32r >419430400 else v_x1_u32r

        h = (v_x1_u32r>>12)
        return h / 1024.0

    def _calc_pres(self,adc_p):
        if adc_p == 0x80000:
            return 0

        var1 = (self.t_fine >> 1) - 64000

        var2 = (((var1>>2) * (var1>>2)) >> 11 ) * self.dig_P6
        var2 = var2 + ((var1*self.dig_P5)<<1)
        var2 = (var2>>2)+(self.dig_P4<<16)

        var1 = (((self.dig_P3 * (((var1>>2) * (var1>>2)) >> 13 )) >> 3) + ((self.dig_P2 * var1)>>1))>>18
        var1 = ((32768+var1)*(self.dig_P1))>>15

        if var1 == 0:
            return 0 # avoid exception caused by division by zero

        p = (((1048576-adc_p)-(var2>>12)))*3125
        p = (p //var1 ) << 1

        var1 = (self.dig_P9 * (((p>>3) * (p>>3))>>13)) >> 12
        var2 = ((p>>2) * self.dig_P8) >> 13

        p = p + ((var1 + var2 + self.dig_P7) >> 4)

        return p/100

    def get_raw_temp(self):
        r = self.i2c.write_read(self.addr, 0xFA,3)
        adc_t = (r[0]<<16) | (r[1] <<8) | r[2]
        adc_t = adc_t>>4
        return adc_t

    def get_raw_hum(self):
        r = self.i2c.write_read(self.addr, 0xFD,2)
        adc_h = (r[0]<<8) | r[1]
        return adc_h

    def get_raw_pres(self):
        r = self.i2c.write_read(self.addr, 0xF7,3)
        adc_p = (r[0] << 16) | (r[1] << 8) | r[2]
        adc_p = adc_p >> 4
        return adc_p

    def values(self):
        r = self.i2c.write_read(self.addr, 0xF7,8)

        adc_t = (r[3]<<16) | (r[4] <<8) | r[5]
        adc_t = adc_t>>4

        adc_h = (r[6]<<8) | r[7]

        adc_p = (r[0] << 16) | (r[1] << 8) | r[2]
        adc_p = adc_p >> 4

        return (self._calc_temp(adc_t), self._calc_hum(adc_h), self._calc_pres(adc_p))