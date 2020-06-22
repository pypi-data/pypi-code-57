from random import randrange

import msgpack


class BinaryProtocolAbstract(object):
    """
    Abstract class for Binary protocol
    """
    _headers: dict = {}

    _body: str = ""
    _unpacker = msgpack.Unpacker(raw=False)
    _packer = msgpack.Packer(use_bin_type=True)
    _id: int = randrange(999999)
    _version: str = "Medusa Protocol V1"

    @property
    def id(self):
        """
        Getter for the id protocol parameter
        :return:
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        setter for the id protocol parameter
        in general this parameter is generate in a randomized way
        :param id: integer
        :return: None
        """
        self._id = id

    @property
    def body(self) -> str:
        """
        Breda Body Protocol Getter
        :return:
        """
        return self._body

    @body.setter
    def body(self, content: str) -> None:
        """
        Breda Body Protocol Setter
        :param content:
        :return:
        """
        self._body = content

    def decode(self, bytes) -> None:
        """
        decode the bytes msgpack to dictionary
        the decoding create two main objects
        HEADERS
        BODY

        the headers object get all the information about the handler to call
        the body is the content of the request/response
        :param bytes:
        :return:
        """
        self._unpacker.feed(bytes)
        content: dict = self._unpacker.unpack()
        self._decode_attributes(content)
        self._decode_additional_attributes(content)

    def encode(self) -> bytes:
        """
        get encoded binary data
        :return:
        """
        data_to_encode: dict = {
            "version": self._version,
            "id": self._id,
            "payload": self._body
        }
        data_to_encode = self._encode_attributes(data_to_encode)
        return self._packer.pack(data_to_encode)

    def _encode_attributes(self, data: dict) -> dict:
        return data

    def _decode_attributes(self, content: dict) -> None:
        self._id = content['id']
        self._version = content['version']
        self._body = content['payload']

    def _decode_additional_attributes(self, content: dict) -> None:
        pass
