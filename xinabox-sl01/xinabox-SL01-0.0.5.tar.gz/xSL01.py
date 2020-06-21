from xCore import xCore

class xSL01:
    def __init__(self):
        self.i2c = xCore()
        self.addrVE = 0x10
        self.addrTS = 0x29
        self.__UVAintensity = 0.0
        self.__UVBintensity = 0.0
        self.__UVindex = 0.0
        self.__rawUVA = 0
        self.__rawUVB = 0
        self.__UVcomp1 = 0
        self.__UVcomp2 = 0
        self.__LUX = 0.0
        self.initTS()
        self.initVE()

    def initVE(self):
        try:
            self.i2c.write_bytes(self.addrVE, 0x00, 0x10)
            self.i2c.write_bytes(self.addrVE, 0x00)
        except Exception as e:
            print(e)

    def getUVA(self):
        self.GET_VEML()
        return self.__UVAintensity

    def getUVB(self):
        self.GET_VEML()
        return self.__UVBintensity

    def getUVIndex(self):
        self.GET_VEML()
        self.calculateIndex()
        return self.__UVindex

    def GET_VEML(self):
        self.readUVdata()
        self.__UVAintensity = float(self.__rawUVA)
        self.__UVBintensity = float(self.__rawUVB)
        self.__UVAintensity -= (2.22 * self.__UVcomp1) - (1.33 * self.__UVcomp2)
        self.__UVBintensity -= (2.95 * self.__UVcomp1) - (1.74 * self.__UVcomp2)

    def readUVdata(self):
        self.__rawUVA = self.readVEML(0x07)
        self.__rawUVB = self.readVEML(0x09)
        self.__UVcomp1 = self.readVEML(0x0A)
        self.__UVcomp2 = self.readVEML(0x0B)

    def calculateIndex(self):
        UVAComp = 0
        UVBComp = 0
        UVAComp = (self.__UVAintensity * (1.0 / 684.46))
        UVBComp = (self.__UVBintensity * (1.0 / 385.95))
        self.__UVindex = (UVAComp + UVBComp)/2.0

    def readVEML(self, reg):
        raw=self.i2c.write_read(self.addrVE, reg, 2)
        value = raw[1]*256 + raw[0]
        return value

    def initTS(self):
        try:
            self.i2c.write_bytes(self.addrTS, (0x80 | 0x00), 0x03)
            self.i2c.write_bytes(self.addrTS, (0x80 | 0x01), 0x02)
        except Exception as e:
            print(e)

    def getLUX(self):
        self.GET_TSL()
        return self.__LUX

    def GET_TSL(self):
        multi = int(4)
        raw_LUX_H = self.i2c.write_read(self.addrTS, (0x80 | 0x05), 1)[0]
        raw_LUX_L = self.i2c.write_read(self.addrTS, (0x80 | 0x04), 1)[0]
        data = ((raw_LUX_H << 8)|(raw_LUX_L))
        self.__LUX = multi*data