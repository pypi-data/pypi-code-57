from yoti_python_sdk import config

from .anchor import SandboxAnchor  # noqa: F401
from .attribute import SandboxAttribute


class SandboxAgeVerification(object):
    """
    Represents an Age Verification attribute that can be
    used by the Yoti Profile Sandbox service
    """

    def __init__(self, date_of_birth, supported_age_derivation, anchors=None):
        """
        :param date_of_birth: the date birth
        :type date_of_birth: str
        :param supported_age_derivation: the age derivation
        :type supported_age_derivation: str
        :param anchors: the list of anchors
        :type anchors: list[SandboxAnchor]
        """
        if anchors is None:
            anchors = []

        self.__date_of_birth = date_of_birth
        self.__supported_age_derivation = supported_age_derivation
        self.__anchors = anchors

    def to_attribute(self):
        """
        Converts the age verification object into an Attribute

        :return: Instance of SandboxAttribute
        :rtype: SandboxAttribute
        """
        return (
            SandboxAttribute.builder()
            .with_name(config.ATTRIBUTE_DATE_OF_BIRTH)
            .with_value(self.__date_of_birth)
            .with_derivation(self.__supported_age_derivation)
            .with_anchors(self.__anchors)
            .build()
        )

    @staticmethod
    def builder():
        """
        Creates a sandbox age verification builder

        :return: Instance of SandboxAgeVerificationBuilder
        :rtype: SandboxAgeVerificationBuilder
        """
        return SandboxAgeVerificationBuilder()


class SandboxAgeVerificationBuilder(object):
    def __init__(self):
        self.__date_of_birth = None
        self.__derivation = None
        self.__anchors = None

    def with_date_of_birth(self, date_of_birth):
        """
        Set the date of birth on the builder

        :param date_of_birth: the date of birth
        :type date_of_birth: str
        :return: the updated builder
        :rtype: SandboxAgeVerificationBuilder
        """
        self.__date_of_birth = date_of_birth
        return self

    def with_derivation(self, derivation):
        """
        Set the derivation of the age verification

        :param derivation: the derivation
        :type derivation: str
        :return: the updated builder
        :rtype: SandboxAgeVerificationBuilder
        """
        self.__derivation = derivation
        return self

    def with_age_over(self, age_over):
        """
        Set the age over value of the age verification

        :param age_over: the age over value
        :type age_over: int
        :return: the updated builder
        :rtype: SandboxAgeVerificationBuilder
        """
        return self.with_derivation(config.ATTRIBUTE_AGE_OVER + str(age_over))

    def with_age_under(self, age_under):
        """
        Set the age under value of the age verification

        :param age_under:
        :type age_under: int
        :return: the updated builder
        :rtype: SandboxAgeVerificationBuilder
        """
        return self.with_derivation(config.ATTRIBUTE_AGE_UNDER + str(age_under))

    def with_anchors(self, anchors):
        """
        Set the anchors for the age verification

        :param anchors: the list of anchors
        :type anchors: list[SandboxAnchor]
        :return: the updated builder
        :rtype: SandboxAgeVerificationBuilder
        """
        self.__anchors = anchors
        return self

    def build(self):
        """
        Build the age verification object with the supplied values

        :return: the age verification
        :rtype: SandboxAgeVerification
        """
        return SandboxAgeVerification(
            self.__date_of_birth, self.__derivation, self.__anchors
        )
