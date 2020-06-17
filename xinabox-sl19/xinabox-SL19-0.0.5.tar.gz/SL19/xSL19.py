from xCore import xCore

MLX90614_REG_RAWIR1 = 0x04
MLX90614_REG_RAWIR2 = 0x05
MLX90614_REG_TA 	= 0x06
MLX90614_REG_TOBJ1 	= 0x07
MLX90614_REG_TOBJ2 	= 0x08
MLX90614_REG_TOMAX 	= 0x20
MLX90614_REG_TOMIN 	= 0x21
MLX90614_REG_PWMCTRL = 0x22
MLX90614_REG_TARANGE = 0x23
MLX90614_REG_EMISS 	= 0x24
MLX90614_REG_CONFIG = 0x25
MLX90614_REG_ADDR 	= 0x0E
MLX90614_REG_ID1 	= 0x3C
MLX90614_REG_ID2 	= 0x3D
MLX90614_REG_ID3 	= 0x3E
MLX90614_REG_ID4 	= 0x3F

class xSL19:
	def __init__(self):
		self.addr = 0x5A
		self.i2c = xCore()

	def init(self):
		return True

	def getAmbientTempC(self):
		return self.readAmbient()

	def getAmbientTempF(self):
		return ((self.readAmbient() * 1.8) + 32)

	def getObjectTempC(self):
		return self.readObject()

	def getObjectTempF(self):
		return ((self.readObject() * 1.8) + 32)

	def readAmbient(self):
		tempData = self.readTemp(MLX90614_REG_TA)
		tempData = tempData * 0.02
		tempData = tempData - 273.15
		ambient_temp = tempData
		return ambient_temp

	def readObject(self):
		tempData = self.readTemp(MLX90614_REG_TOBJ1)
		tempData = tempData * 0.02
		tempData = tempData - 273.15
		object_temp = tempData
		return object_temp

	def readTemp(self, reg):
		data = self.i2c.write_read(self.addr, reg, 3)
		data = (data[0] + ((data[1] & 0x7F) << 8))
		return data