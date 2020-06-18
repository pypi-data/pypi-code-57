from yoti_python_sdk.utils import YotiSerializable

from .task_results import SandboxTaskResults  # noqa: F401


class ResponseConfig(YotiSerializable):
    def __init__(self, task_results, check_reports):
        self.__task_results = task_results
        self.__check_reports = check_reports

    @property
    def check_reports(self):
        """
        :return: the check reports
        :rtype: CheckReports
        """
        return self.__check_reports

    @property
    def task_results(self):
        """
        :return: the task results
        :rtype: SandboxTaskResults
        """
        return self.__task_results

    def to_json(self):
        payload = {}
        if self.__task_results is not None:
            payload["task_results"] = self.__task_results

        if self.__check_reports is not None:
            payload["check_reports"] = self.__check_reports

        return payload


class ResponseConfigBuilder(object):
    def __init__(self):
        self.__task_results = None
        self.__check_reports = None

    def with_task_results(self, results):
        """
        :param results: the task result container
        :type results: SandboxTaskResults
        """
        self.__task_results = results
        return self

    def with_check_reports(self, report):
        self.__check_reports = report
        return self

    def build(self):
        return ResponseConfig(self.__task_results, self.__check_reports)
