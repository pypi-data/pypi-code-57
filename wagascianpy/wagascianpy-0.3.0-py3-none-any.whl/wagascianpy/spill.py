from array import array
import abc
from collections import namedtuple

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})

_NON_PHYSICAL_VALUE = -1

WAGASCI_SPILL_BEAM_MODE = 1
WAGASCI_SPILL_NO_BEAM_MODE = 0
IS_GOOD_SPILL = 1
NOT_GOOD_SPILL = 0


class VirtualSpill(ABC):
    def are_all_defined(self):
        for key, value in self.__dict__.items():
            assert (value != _NON_PHYSICAL_VALUE), "instance variable {} is still not initialized".format(key)
        return True

    def pretty_print(self):
        for key, value in self.__dict__.items():
            print("%s = %s" % (key, value))

    def _get_type_char(self, var_name):
        assert (hasattr(self, var_name)), \
            "object {} has not an attribute named {}".format(type(self).__name__, var_name)
        var = getattr(self, var_name)
        assert (isinstance(var, float) or isinstance(var, int)), \
            "type of variable {} is not supported : {}".format(var_name, type(var_name).__name__)
        type_char = 'i' if isinstance(var, int) else 'd'
        return type_char

    def _get_type_str(self, var_name):
        type_char = self._get_type_char(var_name)
        return '{}/{}'.format(var_name, type_char.upper())

    def _get_array(self, var_name):
        return array(self._get_type_char(var_name), [0])

    def _set_array(self, array_info):
        assert (hasattr(self, array_info.name)), \
            "object {} has not an attribute named {}".format(type(self).__name__, array_info.name)
        array_info.array[0] = getattr(self, array_info.name)

    def get_array_list(self):
        ArrayInfo = namedtuple('ArrayInfo', ['name', 'array', 'type_char', 'type_str'])
        array_list = []
        for key, value in self.__dict__.items():
            array_info = ArrayInfo(key, self._get_array(key), self._get_type_char(key), self._get_type_str(key))
            array_list.append(array_info)
        return array_list

    def set_array_list(self, array_list):
        for array_info in array_list:
            self._set_array(array_info)


class BsdSpill(VirtualSpill):
    def __init__(self):
        self.bsd_spill_number = _NON_PHYSICAL_VALUE
        self.converted_spill_number = _NON_PHYSICAL_VALUE
        self.pot = float(_NON_PHYSICAL_VALUE)
        self.timestamp = float(_NON_PHYSICAL_VALUE)
        self.bsd_good_spill_flag = _NON_PHYSICAL_VALUE


class WagasciSpill(VirtualSpill):
    def __init__(self):
        self.spill_count = _NON_PHYSICAL_VALUE
        self.spill_number = _NON_PHYSICAL_VALUE
        self.converted_spill_number = _NON_PHYSICAL_VALUE
        self.spill_mode = _NON_PHYSICAL_VALUE
        self.good_spill_flag = _NON_PHYSICAL_VALUE


class WagasciBsdSpill(VirtualSpill):
    def __init__(self):
        self.spill_count = _NON_PHYSICAL_VALUE
        self.spill_number = _NON_PHYSICAL_VALUE
        self.fixed_spill_number = _NON_PHYSICAL_VALUE
        self.converted_spill_number = _NON_PHYSICAL_VALUE
        self.spill_mode = _NON_PHYSICAL_VALUE
        self.good_spill_flag = _NON_PHYSICAL_VALUE
        self.bsd_spill_number = _NON_PHYSICAL_VALUE
        self.pot = float(_NON_PHYSICAL_VALUE)
        self.timestamp = float(_NON_PHYSICAL_VALUE)
        self.bsd_good_spill_flag = _NON_PHYSICAL_VALUE


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
