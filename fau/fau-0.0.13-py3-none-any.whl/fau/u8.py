from .unsigned_integer_array import UnsignedIntegerArray


class U8(UnsignedIntegerArray):
    @property
    def _type_code(self) -> str:
        return 'B'
