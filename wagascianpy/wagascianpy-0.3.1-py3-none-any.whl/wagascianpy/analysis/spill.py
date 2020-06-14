import numpy
import abc
from collections import namedtuple

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})

_NON_INITIALIZED_VALUE = -2

WAGASCI_SPILL_BEAM_MODE = 1
WAGASCI_SPILL_NO_BEAM_MODE = 0
IS_GOOD_SPILL = 1
NOT_GOOD_SPILL = 0
WAGASCI_MINIMUM_SPILL = 32768
WAGASCI_MAXIMUM_SPILL = 65535

SpillArrayInfo = namedtuple('SpillArrayInfo', ['name', 'array', 'type_char', 'type_str'])


class VirtualSpill(ABC):
    def are_all_defined(self):
        for key, value in self.__dict__.items():
            assert (value != _NON_INITIALIZED_VALUE), "instance variable {} is still not initialized".format(key)
        return True

    def pretty_print(self):
        for key, value in self.__dict__.items():
            print("%s = %s" % (key, value))

    def _get_type_char(self, var_name):
        assert (hasattr(self, var_name)), \
            "object {} has not an attribute named {}".format(type(self).__name__, var_name)
        var = getattr(self, var_name)
        assert (isinstance(var, float) or isinstance(var, int) or isinstance(var, bool)), \
            "type of variable {} is not supported : {}".format(var_name, type(var_name).__name__)
        if isinstance(var, bool):
            type_char = 'o'
        elif isinstance(var, int):
            type_char = 'i'
        elif isinstance(var, float):
            type_char = 'd'
        else:
            raise NotImplementedError("Type not recognized")
        return type_char

    def _get_numpy_type(self, var_name):
        type_char = self._get_type_char(var_name)
        if type_char == 'i':
            type_string = numpy.int32
        elif type_char == 'd':
            type_string = numpy.float64
        elif type_char == 'o':
            type_string = numpy.bool
        else:
            raise NotImplementedError("Type character not recognized : %s" % type_char)
        return type_string

    def _get_type_str(self, var_name):
        type_char = self._get_type_char(var_name)
        return '{}/{}'.format(var_name.strip('_'), type_char.upper())

    def _get_array(self, var_name):
        assert (hasattr(self, var_name)), \
            "object {} has not an attribute named {}".format(type(self).__name__, var_name)
        return numpy.array([getattr(self, var_name)], dtype=self._get_numpy_type(var_name))

    def _set_array(self, array_info):
        assert (hasattr(self, array_info.name)), \
            "object {} has not an attribute named {}".format(type(self).__name__, array_info.name)
        array_info.array[0] = getattr(self, array_info.name)

    def get_array_list(self):
        array_list = []
        for key in self.__dict__:
            array_info = SpillArrayInfo(name=key.strip('_'),
                                        array=self._get_array(key),
                                        type_char=self._get_type_char(key),
                                        type_str=self._get_type_str(key))
            array_list.append(array_info)
        return array_list

    def set_array_list(self, array_list):
        for array_info in array_list:
            self._set_array(array_info)


class BsdSpill(VirtualSpill):
    def __init__(self):
        self._bsd_spill_number = int(_NON_INITIALIZED_VALUE)
        self._converted_spill_number = int(_NON_INITIALIZED_VALUE)
        self._pot = float(_NON_INITIALIZED_VALUE)
        self._timestamp = float(_NON_INITIALIZED_VALUE)
        self._bsd_good_spill_flag = int(_NON_INITIALIZED_VALUE)

    @property
    def bsd_spill_number(self):
        return self._bsd_spill_number

    @bsd_spill_number.setter
    def bsd_spill_number(self, bsd_spill_number):
        self._bsd_spill_number = int(bsd_spill_number)

    @property
    def converted_spill_number(self):
        return self._converted_spill_number

    @converted_spill_number.setter
    def converted_spill_number(self, converted_spill_number):
        self._converted_spill_number = int(converted_spill_number)

    @property
    def pot(self):
        return self._pot

    @pot.setter
    def pot(self, pot):
        self._pot = float(pot)

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        self._timestamp = float(timestamp)

    @property
    def bsd_good_spill_flag(self):
        return self._bsd_good_spill_flag

    @bsd_good_spill_flag.setter
    def bsd_good_spill_flag(self, bsd_good_spill_flag):
        self._bsd_good_spill_flag = int(bsd_good_spill_flag)


class WagasciSpill(VirtualSpill):
    def __init__(self):
        self._spill_count = int(_NON_INITIALIZED_VALUE)
        self._spill_number = int(_NON_INITIALIZED_VALUE)
        self._converted_spill_number = int(_NON_INITIALIZED_VALUE)
        self._spill_mode = int(_NON_INITIALIZED_VALUE)
        self._good_spill_flag = bool(_NON_INITIALIZED_VALUE)
        self._temperature = 0.
        self._humidity = 0.

    @property
    def spill_count(self):
        return self._spill_count

    @spill_count.setter
    def spill_count(self, spill_count):
        self._spill_count = int(spill_count)

    @property
    def spill_number(self):
        return self._spill_number

    @spill_number.setter
    def spill_number(self, spill_number):
        self._spill_number = int(spill_number)

    @property
    def spill_mode(self):
        return self._spill_mode

    @spill_mode.setter
    def spill_mode(self, spill_mode):
        self._spill_mode = int(spill_mode)

    @property
    def converted_spill_number(self):
        return self._converted_spill_number

    @converted_spill_number.setter
    def converted_spill_number(self, converted_spill_number):
        self._converted_spill_number = int(converted_spill_number)

    @property
    def good_spill_flag(self):
        return self._good_spill_flag

    @good_spill_flag.setter
    def good_spill_flag(self, good_spill_flag):
        assert good_spill_flag in [0, 1, False, True, "0", "1", "False", "True", "false", "true"], \
            "Invalid value of good spill flag"
        self._good_spill_flag = bool(good_spill_flag)

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, temperature):
        self._temperature = float(temperature)

    @property
    def humidity(self):
        return self._humidity

    @humidity.setter
    def humidity(self, humidity):
        self._humidity = float(humidity)


class WagasciBsdSpill(WagasciSpill, BsdSpill):
    def __init__(self):
        super(WagasciSpill, self).__init__()
        super(BsdSpill, self).__init__()


class SpillFactory:
    def __init__(self):
        pass

    @staticmethod
    def get_spill(type_of_spill):
        if type_of_spill.lower() == "wagasci":
            return WagasciSpill()
        elif type_of_spill.lower() == "bsd":
            return BsdSpill()
        elif type_of_spill.lower().replace('_', '').replace(' ', '').replace('-', '') == "wagascibsd":
            return WagasciBsdSpill()
        else:
            raise ValueError("spill type not recognized : {}".format(type_of_spill))
