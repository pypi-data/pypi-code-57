from yoti_python_sdk.utils import YotiSerializable


class SandboxCheckReport(YotiSerializable):
    def __init__(self, recommendation, breakdown):
        """
        :param recommendation: the recommendation
        :type recommendation: SandboxRecommendation
        :param breakdown: the list of breakdowns
        :type breakdown: list[SandboxBreakdown]
        """
        self.__recommendation = recommendation
        self.__breakdown = breakdown

    @property
    def recommendation(self):
        """
        The recommendation expectation for the sandbox check

        :return: the recommendation
        :rtype: SandboxRecommendation
        """
        return self.__recommendation

    @property
    def breakdown(self):
        """
        The list of breakdowns for the sandbox check

        :return: the list of breakdowns
        :rtype: list[SandboxBreakdown]
        """
        return self.__breakdown

    def to_json(self):
        return {
            "recommendation": self.recommendation,
            "breakdown": self.breakdown,
        }
