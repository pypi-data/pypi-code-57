from crownstone_core.protocol.BlePackets import ControlPacket, FactoryResetPacket
from crownstone_core.protocol.BluenetTypes import ControlType
from crownstone_core.util.Conversion import Conversion


class ControlPacketsGenerator:

	@staticmethod
	def getFactoryResetPacket():
		return Conversion.uint32_to_uint8_array(0xdeadbeef)


	@staticmethod
	def getCommandFactoryResetPacket():
		return FactoryResetPacket().getPacket()

	@staticmethod
	def getSwitchStatePacket(switchState):
		"""
		:param switchState: number [0..1]
		"""

		convertedSwitchState = int(min(1,max(0,switchState))*100)

		return ControlPacket(ControlType.SWITCH).loadUInt8(convertedSwitchState).getPacket()

	@staticmethod
	def getResetPacket():
		return ControlPacket(ControlType.RESET).getPacket()

	@staticmethod
	def getPutInDFUPacket():
		return ControlPacket(ControlType.GOTO_DFU).getPacket()

	@staticmethod
	def getDisconnectPacket():
		return ControlPacket(ControlType.DISCONNECT).getPacket()

	@staticmethod
	def getRelaySwitchPacket(state):
		"""
		:param state: 0 or 1
		"""
		return ControlPacket(ControlType.RELAY).loadUInt8(state).getPacket()

	@staticmethod
	def getPwmSwitchPacket(switchState):
		"""
		:param switchState: number [0..1]
		:return:
		"""
		convertedSwitchState = int(min(1, max(0, switchState)) * 100)

		return ControlPacket(ControlType.PWM).loadUInt8(convertedSwitchState).getPacket()


	@staticmethod
	def getResetErrorPacket(errorMask):
		return ControlPacket(ControlType.RESET_ERRORS).loadUInt32(errorMask).getPacket()

	@staticmethod
	def getSetTimePacket(time):
		"""
		This is a LOCAL timestamp since epoch in seconds

		so if you live in GMT + 1 add 3600 to the timestamp
		:param time:
		:return:
		"""
		return ControlPacket(ControlType.SET_TIME).loadUInt32(time).getPacket()

	@staticmethod
	def getAllowDimmingPacket(allow):
		"""

		:param allow: bool
		:return:
		"""

		allowByte = 0
		if allow:
			allowByte = 1

		return ControlPacket(ControlType.ALLOW_DIMMING).loadUInt8(allowByte).getPacket()

	@staticmethod
	def getLockSwitchPacket(lock):
		"""
		:param lock: bool
		:return:
		"""

		lockByte = 0
		if lock:
			lockByte = 1

		return ControlPacket(ControlType.LOCK_SWITCH).loadUInt8(lockByte).getPacket()
	

	@staticmethod
	def getSetupPacket(
		crownstoneId,
		sphereId,
		adminKey,
		memberKey,
		basicKey,
		serviceDataKey,
		localizationKey,
		meshDeviceKey,
		meshAppKey,
		meshNetworkKey,
		ibeaconUUID,
		ibeaconMajor,
		ibeaconMinor
	):
		"""
		:param crownstoneId:  		uint8 number
		:param sphereId:  	     	uint8 number
		:param adminKey:      		byteString (no conversion required)
		:param memberKey:     		byteString (no conversion required)
		:param basicKey:      		byteString (no conversion required)
		:param serviceDataKey: 	    byteString (no conversion required)
		:param localizationKey: 	byteString (no conversion required)
		:param meshDeviceKey: 	    byteString (no conversion required)
		:param meshAppKey: 	        byteString (no conversion required)
		:param meshNetworkKey: 	    byteString (no conversion required)
		:param ibeaconUUID: 		string  (ie. "1843423e-e175-4af0-a2e4-31e32f729a8a")
		:param ibeaconMajor:        uint16 number
		:param ibeaconMinor:        uint16 number
		:return:
		"""
		data = []
		data.append(crownstoneId)
		data.append(sphereId)

		data += list(adminKey)
		data += list(memberKey)
		data += list(basicKey)
		data += list(serviceDataKey)
		data += list(localizationKey)

		MDKey = meshDeviceKey
		if type(meshDeviceKey) is str:
			MDKey = Conversion.ascii_or_hex_string_to_16_byte_array(meshDeviceKey)

		data += list(MDKey)
		data += list(meshAppKey)
		data += list(meshNetworkKey)

		data += Conversion.ibeaconUUIDString_to_reversed_uint8_array(ibeaconUUID)
		data += Conversion.uint16_to_uint8_array(ibeaconMajor)
		data += Conversion.uint16_to_uint8_array(ibeaconMinor)

		return ControlPacket(ControlType.SETUP).loadByteArray(data).getPacket()


	@staticmethod
	def getIBeaconConfigIdPacket(id, timestamp, interval):
		data = []
		data.append(id)
		data += Conversion.uint32_to_uint8_array(timestamp)
		data += Conversion.uint16_to_uint8_array(interval)

		return ControlPacket(ControlType.SET_IBEACON_CONFIG_ID).loadByteArray(data).getPacket()


