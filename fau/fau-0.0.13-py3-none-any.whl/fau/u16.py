from .unsigned_integer_array import UnsignedIntegerArray


class U16(UnsignedIntegerArray):
    @property
    def _type_code(self) -> str:
        return 'H'
