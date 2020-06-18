from yoti_python_sdk.utils import YotiSerializable

from yoti_python_sandbox.doc_scan.check.sandbox_check_report import (  # noqa: F401
    SandboxCheckReport,
)


class SandboxCheckResult(YotiSerializable):
    def __init__(self, report):
        """
        :param report: the check report
        :type report: SandboxCheckReport
        """
        self.__report = report

    @property
    def report(self):
        """
        :rtype: SandboxCheckReport
        """
        return self.__report

    def to_json(self):
        return {
            "report": self.report,
        }
