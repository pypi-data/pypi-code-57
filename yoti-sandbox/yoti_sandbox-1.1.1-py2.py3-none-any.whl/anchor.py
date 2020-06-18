import datetime

from yoti_python_sdk.anchor import UNKNOWN_ANCHOR_TYPE


class SandboxAnchor(object):
    """
    Represents an anchor that can be used by the Profile
    sandbox service
    """

    def __init__(self, anchor_type=None, sub_type="", value="", timestamp=None):
        """
        :param anchor_type: the anchor type
        :type anchor_type: str or None
        :param sub_type: the sub type of the anchor
        :type sub_type: str
        :param value: the value of the anchor
        :type value: str
        :param timestamp: the timestamp of the anchor
        :type timestamp: long or None
        """
        if anchor_type is None:
            anchor_type = UNKNOWN_ANCHOR_TYPE

        self.__anchor_type = anchor_type
        self.__sub_type = sub_type
        self.__value = value
        self.__unix_microsecond_timestamp = timestamp

    @property
    def anchor_type(self):
        """
        Returns the anchor type

        :return: the type
        :rtype: str
        """
        return self.__anchor_type

    @property
    def sub_type(self):
        """
        Returns the anchor sub-type

        :return: the sub-type
        :rtype: str
        """
        return self.__sub_type

    @property
    def value(self):
        """
        Returns the anchor value

        :return: the value
        :rtype: str
        """
        return self.__value

    @property
    def timestamp(self):
        """
        Returns the microsecond unix anchor timestamp

        :return: the timestamp
        :rtype: long or None
        """
        return self.__unix_microsecond_timestamp

    def __dict__(self):
        return {
            "type": self.anchor_type,
            "value": self.value,
            "sub_type": self.sub_type,
            "timestamp": self.timestamp,
        }

    @staticmethod
    def builder():
        """
        Creates an instance of the sandbox anchor builder

        :return: instance of SandboxAnchorBuilder
        :rtype: SandboxAnchorBuilder
        """
        return SandboxAnchorBuilder()


class SandboxAnchorBuilder(object):
    """
    Builder to assist creation of Anchor objects that can
    be used by the Yoti Profile sandbox service
    """

    def __init__(self):
        self.__type = None
        self.__value = None
        self.__sub_type = None
        self.__unix_microsecond_timestamp = None

    def with_type(self, value):
        """
        Sets the type of the anchor on the builder

        :param str value: the anchor type
        :return: the updated builder
        :rtype: SandboxAnchorBuilder
        """
        self.__type = value
        return self

    def with_value(self, value):
        """
        Sets the value of the anchor on the builder

        :param str value: the anchor value
        :return: the updated builder
        :rtype: SandboxAnchorBuilder
        """
        self.__value = value
        return self

    def with_sub_type(self, sub_type):
        """
        Sets the sub type of the anchor on the builder

        :param str sub_type: the anchor sub type
        :return: the updated builder
        :rtype: SandboxAnchorBuilder
        """
        self.__sub_type = sub_type
        return self

    def with_timestamp(self, timestamp):
        """
        Sets the timestamp of the anchor on the builder

        :param datetime timestamp: the anchor timestamp
        :return: the updated builder
        :rtype: SandboxAnchorBuilder
        """

        if not isinstance(timestamp, datetime.datetime):
            raise TypeError("Provided timestamp must be of type 'datetime'")

        unix_seconds = timestamp.timestamp()
        self.__unix_microsecond_timestamp = int(unix_seconds * 1000000)
        return self

    def build(self):
        """
        Creates a SandboxAnchor using values supplied to the builder

        :return: the sandbox anchor
        :rtype: SandboxAnchor
        """
        return SandboxAnchor(
            self.__type,
            self.__sub_type,
            self.__value,
            self.__unix_microsecond_timestamp,
        )
