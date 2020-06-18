from yoti_python_sdk.utils import YotiSerializable


class SandboxBreakdown(YotiSerializable):
    def __init__(self, sub_check, result, details):
        """
        :type sub_check: str
        :type result: str
        :type details: list[SandboxDetails]
        """
        self.__sub_check = sub_check
        self.__result = result
        self.__details = details

    @property
    def sub_check(self):
        return self.__sub_check

    @property
    def result(self):
        return self.__result

    @property
    def details(self):
        return self.__details

    def to_json(self):
        return {
            "sub_check": self.sub_check,
            "result": self.result,
            "details": self.details,
        }


class SandboxBreakdownBuilder(object):
    def __init__(self):
        self.__sub_check = None
        self.__result = None
        self.__details = []

    def with_sub_check(self, sub_check):
        """
        Sets the sub check for the breakdown

        :param sub_check: the sub check
        :type sub_check: str
        :return: the builder
        :rtype: SandboxBreakdownBuilder
        """
        self.__sub_check = sub_check
        return self

    def with_result(self, result):
        """
        Sets the result for the breakdown

        :param result: the result
        :type result: str
        :return: the builder
        :rtype: SandboxBreakdownBuilder
        """
        self.__result = result
        return self

    def with_detail(self, details):
        """
        Sets the details for the breakdown

        :param details: the details
        :type details: SandboxDetails
        :return: the builder
        :rtype: SandboxBreakdownBuilder
        """
        self.__details.append(details)
        return self

    def build(self):
        return SandboxBreakdown(self.__sub_check, self.__result, self.__details)
