from yoti_python_sandbox.doc_scan.check.sandbox_check_report import SandboxCheckReport
from yoti_python_sandbox.doc_scan.check.sandbox_check_result import SandboxCheckResult
from yoti_python_sandbox.doc_scan.check.sandbox_document_check import (
    SandboxDocumentCheck,
)
from yoti_python_sandbox.doc_scan.check.sandbox_document_check import (
    SandboxDocumentCheckBuilder,
)


class SandboxDocumentFaceMatchCheck(SandboxDocumentCheck):
    @staticmethod
    def builder():
        return SandboxDocumentFaceMatchCheckBuilder()


class SandboxDocumentFaceMatchCheckBuilder(SandboxDocumentCheckBuilder):
    def build(self):
        report = SandboxCheckReport(self.recommendation, self.breakdown)
        result = SandboxCheckResult(report)
        return SandboxDocumentFaceMatchCheck(result, self.document_filter)
