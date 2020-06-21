from .Abstract import BinaryProtocolAbstract
from ..exceptions import BinaryProtocolInvalidField


class BinaryRequest(BinaryProtocolAbstract):
    _signature: str = ""
    _hash: str = ""
    _action: str = ""

    @property
    def action(self):
        """
        Breda HEADERS Action Protocol Getter
        :return:
        """
        return self._action

    @action.setter
    def action(self, action):
        """
        Breda HEADERS Action Protocol Setter
        :return:
        """
        self._action = action

    def _decode_additional_attributes(self, content: dict) -> None:
        self._action = content['headers']['action']

    def _encode_attributes(self, data: dict) -> dict:
        if len(self._action) == 0:
            raise BinaryProtocolInvalidField("Action or Namespace values are mandatory")

        data['headers'] = {
            'signature': self._signature,
            'hash': self._hash,
            'action': self._action,
        }
        return data
