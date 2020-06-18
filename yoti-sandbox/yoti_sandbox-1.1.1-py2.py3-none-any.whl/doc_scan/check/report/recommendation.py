from yoti_python_sdk.utils import YotiSerializable


class SandboxRecommendation(YotiSerializable):
    def __init__(self, value, reason, recovery_suggestion):
        """
        :type value: str
        :type reason: str
        :type recovery_suggestion: str
        """
        self.__value = value
        self.__reason = reason
        self.__recovery_suggestion = recovery_suggestion

    @property
    def value(self):
        return self.__value

    @property
    def reason(self):
        return self.__reason

    @property
    def recovery_suggestion(self):
        return self.__recovery_suggestion

    def to_json(self):
        return {
            "value": self.value,
            "reason": self.reason,
            "recovery_suggestion": self.recovery_suggestion,
        }


class SandboxRecommendationBuilder(object):
    def __init__(self):
        self.__value = None
        self.__reason = None
        self.__recovery_suggestion = None

    def with_value(self, value):
        """
        Sets the value for the recommendation

        :param value: the value
        :type value: str
        :return: the builder
        :rtype: SandboxRecommendationBuilder
        """
        self.__value = value
        return self

    def with_reason(self, reason):
        """
        Sets the reason for the recommendation

        :param reason: the reason
        :type reason: str
        :return: the builder
        :rtype: SandboxRecommendationBuilder
        """
        self.__reason = reason
        return self

    def with_recovery_suggestion(self, recovery_suggestion):
        """
        Sets the recovery suggestion for the recommendation

        :param recovery_suggestion: the recovery suggestion
        :type recovery_suggestion: str
        :return: the builder
        :rtype: SandboxRecommendationBuilder
        """
        self.__recovery_suggestion = recovery_suggestion
        return self

    def build(self):
        return SandboxRecommendation(
            self.__value, self.__reason, self.__recovery_suggestion
        )
