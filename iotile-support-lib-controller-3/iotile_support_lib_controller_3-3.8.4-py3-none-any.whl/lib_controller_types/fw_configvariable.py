import struct
from iotile.core.exceptions import *
from .fw_tileselector import TileSelector


class ConfigDescriptor:
    ConfigMagic = 0xCACA
    BufferSize = 16

    def __init__(self, arg):
        if isinstance(arg, bytearray):
            if len(arg) != self.BufferSize:
                raise ValidationError("Invalid size for buffer containing a TileDescriptor", expected=self.BufferSize, actual=len(arg))

            self.raw_data = arg
            self._extract_info()
        else:
            raise ValidationError("You can only create a ConfigDescriptor from binary data")

    def _extract_info(self):
        magic, offset, length, match_info, valid, _ = struct.unpack("<HHH8sBB", self.raw_data)

        if magic != ConfigDescriptor.ConfigMagic:
            raise ValidationError("Invalid magic number in config variable", expected=ConfigDescriptor.ConfigMagic, actual=magic)

        self.data_offset = offset
        self.data_length = length
        self.target = TileSelector(bytearray(match_info))
        self.valid = bool(valid == 0xFF)

    def add_name(self, name):
        """Add the name/id of the config variable to the descriptor"""

        self.name = name

    def add_data(self, data):
        """Add the data of the config variable to the descriptor"""

        self.data = data

    def parse_descriptor(self):
        """Convert a config descriptor into a string descriptor.
    
        Returns:
            str: The corresponding string description of the config variable.
        """

        return "'{}' {} {}".format(self.target, self.name, self.data)

    def __str__(self):
        out = ""

        out += "Target: %s\n" % str(self.target)
        out += "Data Offset: %d\n" % self.data_offset
        out += "Data Length: %d\n" % self.data_length
        out += "Valid: %s" % str(self.valid)

        return out


def convert(arg):
    if isinstance(arg, ConfigDescriptor):
        return arg

    return ConfigDescriptor(arg)


# Formatting Functions
def default_formatter(arg, **kwargs):
    return str(arg)
