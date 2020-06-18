from .anchor import SandboxAnchor  # noqa: F401


class SandboxAttribute(object):
    def __init__(self, name="", value="", anchors=None, derivation=""):
        """
        :param name: the name of the attribute
        :type name: str
        :param value: the value of the attribute
        :type value: str
        :param anchors: the anchors for the attribute
        :type anchors: list[SandboxAnchor]
        :param derivation: the attribute derivation
        :type derivation: str
        """
        if anchors is None:
            anchors = []

        self.__name = name
        self.__value = value
        self.__anchors = anchors
        self.__derivation = derivation

    @property
    def name(self):
        """
        Returns the name of the attribute

        :return: the name
        :rtype: str
        """
        return self.__name

    @property
    def value(self):
        """
        Returns the value of the attribute

        :return: the value
        :rtype: str
        """
        return self.__value

    @property
    def anchors(self):
        """
        Returns the anchors associated with the attribute

        :return: the anchors
        :rtype: list[SandboxAnchor]
        """
        return self.__anchors

    @property
    def derivation(self):
        """
        Returns the derivation of the attribute

        :return: the derivation
        :rtype: str
        """
        return self.__derivation

    def __dict__(self):
        return {
            "name": self.name,
            "value": self.value,
            "anchors": self.anchors,
            "derivation": self.derivation,
        }

    @staticmethod
    def builder():
        """
        Creates an instance of the sandbox attribute builder

        :return: the sandbox attribute builder
        :rtype: SandboxAttributeBuilder
        """
        return SandboxAttributeBuilder()


class SandboxAttributeBuilder(object):
    def __init__(self):
        self.__name = None
        self.__value = None
        self.__anchors = None
        self.__derivation = None

    def with_name(self, name):
        """
        Sets the name of the attribute on the builder

        :param name: the name of the attribute
        :type name: str
        :return: the updated builder
        :rtype: SandboxAttributeBuilder
        """
        self.__name = name
        return self

    def with_value(self, value):
        """
        Sets the value of the attribute on the builder

        :param value: the value of the attribute
        :return: the updated builder
        :rtype: SandboxAttributeBuilder
        """
        self.__value = value
        return self

    def with_anchors(self, anchors):
        """
        Sets the list of anchors associated with the attribute

        :param list[SandboxAnchor] anchors: the associated anchors
        :return:
        """
        self.__anchors = anchors
        return self

    def with_derivation(self, derivation):
        """
        Sets the derivation of the attribute on the builder

        :param str derivation: the derivation
        :return: the updated builder
        """
        self.__derivation = derivation
        return self

    def build(self):
        """
        Create an instance of SandboxAttribute using values supplied to the builder

        :return: instance of SandboxAttribute
        """
        return SandboxAttribute(
            self.__name, self.__value, self.__anchors, self.__derivation
        )
