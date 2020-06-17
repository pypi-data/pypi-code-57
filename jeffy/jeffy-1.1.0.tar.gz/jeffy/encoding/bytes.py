from jeffy.encoding import Encoding


class BytesEncoding(Encoding):
    """Bytes encoding class."""

    def encode(self, payload: bytes) -> bytes:
        """
        Encode to bytes.

        Parameters
        ----------
        payload: bytes

        Returns
        -------
        payload : bytes
        """
        return payload

    def decode(self, payload: bytes) -> bytes:
        """
        Decode from bytes.

        Parameters
        ----------
        payload: bytes

        Returns
        -------
        payload : Any
        """
        return payload
