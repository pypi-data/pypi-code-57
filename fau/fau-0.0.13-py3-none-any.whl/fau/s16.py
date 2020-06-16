from .signed_integer_array import SignedIntegerArray


class S16(SignedIntegerArray):
    @property
    def _type_code(self) -> str:
        return 'h'
