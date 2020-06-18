from yoti_python_sandbox.doc_scan.check.sandbox_check_report import SandboxCheckReport
from yoti_python_sandbox.doc_scan.check.sandbox_check_result import SandboxCheckResult
from yoti_python_sandbox.doc_scan.check.sandbox_document_check import (
    SandboxDocumentCheck,
)
from yoti_python_sandbox.doc_scan.check.sandbox_document_check import (
    SandboxDocumentCheckBuilder,
)


class SandboxDocumentTextDataCheckResult(SandboxCheckResult):
    def __init__(self, report, document_fields=None):
        SandboxCheckResult.__init__(self, report)
        if document_fields is None:
            document_fields = dict()

        self.__document_fields = document_fields

    @property
    def document_fields(self):
        return self.__document_fields

    def to_json(self):
        parent = SandboxCheckResult.to_json(self)
        parent["document_fields"] = self.document_fields
        return parent


class SandboxDocumentTextDataCheck(SandboxDocumentCheck):
    @staticmethod
    def builder():
        return SandboxDocumentTextDataCheckBuilder()


class SandboxDocumentTextDataCheckBuilder(SandboxDocumentCheckBuilder):
    def __init__(self):
        SandboxDocumentCheckBuilder.__init__(self)
        self.__document_fields = {}

    def with_document_field(self, key, value):
        self.__document_fields[key] = value
        return self

    def build(self):
        report = SandboxCheckReport(self.recommendation, self.breakdown)
        result = SandboxDocumentTextDataCheckResult(report, self.__document_fields)
        return SandboxDocumentTextDataCheck(result, self.document_filter)
