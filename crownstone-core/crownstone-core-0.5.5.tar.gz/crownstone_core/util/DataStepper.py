from crownstone_core.Exceptions import CrownstoneError
from crownstone_core.util.Conversion import Conversion


class DataStepper :
    def __init__(self, data):
        self.data = data
        self.length = len(self.data)

        self.position = 0
        self.markPosition = 0


    def getUInt8(self):
        return self._request(1)[0]

    def getUInt16(self):
        return Conversion.uint8_array_to_uint16(self._request(2))

    def getUInt32(self):
        return Conversion.uint8_array_to_uint32(self._request(4))

    def getInt32(self):
        return Conversion.uint8_array_to_int32(self._request(4))

    def getUInt64(self):
        return Conversion.uint8_array_to_uint64(self._request(8))

    def skip(self, count=1):
        self._request(count)

    def getAmountOfBytes(self, amount):
        return self._request(amount)

    def mark(self):
        self.markPosition = self.position


    def reset(self):
        self.position = self.markPosition


    def _request(self, size):
        if self.position + size <= self.length:
            start = self.position
            self.position += size
            return self.data[start:self.position]
        else:
            raise CrownstoneError.INVALID_DATA_LENGTH




