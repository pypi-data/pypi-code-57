from yoti_python_sandbox.doc_scan.check.sandbox_check_report import SandboxCheckReport
from yoti_python_sandbox.doc_scan.check.sandbox_check_result import SandboxCheckResult
from yoti_python_sandbox.doc_scan.check.sandbox_document_check import (
    SandboxDocumentCheck,
)
from yoti_python_sandbox.doc_scan.check.sandbox_document_check import (
    SandboxDocumentCheckBuilder,
)


class SandboxDocumentAuthenticityCheck(SandboxDocumentCheck):
    @staticmethod
    def builder():
        return SandboxDocumentAuthenticityCheckBuilder()


class SandboxDocumentAuthenticityCheckBuilder(SandboxDocumentCheckBuilder):
    def build(self):
        report = SandboxCheckReport(self.recommendation, self.breakdown)
        result = SandboxCheckResult(report)
        return SandboxDocumentAuthenticityCheck(result, self.document_filter)
