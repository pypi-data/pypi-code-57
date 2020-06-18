from abc import ABCMeta
from abc import abstractmethod

from .sandbox_check_result import SandboxCheckResult  # noqa: F401
from yoti_python_sdk.utils import YotiSerializable


class SandboxCheck(YotiSerializable):
    def __init__(self, result):
        """
        :param result: the result
        :type result: SandboxCheckResult
        """
        self.__result = result

    @property
    def result(self):
        """
        :rtype: SandboxCheckResult
        """
        return self.__result

    def to_json(self):
        return {"result": self.result}


class SandboxCheckBuilder(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.__recommendation = None
        self.__breakdown = []

    def with_recommendation(self, recommendation):
        self.__recommendation = recommendation
        return self

    def with_breakdown(self, breakdown):
        self.__breakdown.append(breakdown)
        return self

    def with_breakdowns(self, breakdowns):
        self.__breakdown = breakdowns
        return self

    @property
    def recommendation(self):
        return self.__recommendation

    @property
    def breakdown(self):
        return self.__breakdown

    @abstractmethod
    def build(self):
        raise NotImplementedError
