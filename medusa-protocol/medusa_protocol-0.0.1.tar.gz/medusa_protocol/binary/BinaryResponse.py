from .Abstract import BinaryProtocolAbstract
from ..exceptions import BinaryProtocolInvalidField


class BinaryResponse(BinaryProtocolAbstract):
    _code: int = 0

    @property
    def code(self) -> int:
        return self._code

    @code.setter
    def code(self, code):
        self._code = code

    def _decode_additional_attributes(self, content: dict) -> None:
        self._code = content['code']

    def _encode_attributes(self, data: dict) -> dict:
        if self._code == 0:
            raise BinaryProtocolInvalidField(" code must be comprised between 200 and 500")

        data['code'] = self._code
        return data
