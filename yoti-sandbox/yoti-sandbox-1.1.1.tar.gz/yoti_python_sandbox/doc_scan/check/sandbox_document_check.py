from abc import ABC

from yoti_python_sandbox.doc_scan.check.sandbox_check import SandboxCheck
from yoti_python_sandbox.doc_scan.check.sandbox_check import SandboxCheckBuilder


class SandboxDocumentCheck(SandboxCheck):
    def __init__(self, result, document_filter):
        SandboxCheck.__init__(self, result)
        self.__document_filter = document_filter

    @property
    def document_filter(self):
        return self.__document_filter

    def to_json(self):
        parent = SandboxCheck.to_json(self)
        if self.document_filter is not None:
            parent["document_filter"] = self.document_filter
        return parent


class SandboxDocumentCheckBuilder(SandboxCheckBuilder, ABC):
    def __init__(self):
        SandboxCheckBuilder.__init__(self)
        self.__document_filter = None

    def with_document_filter(self, document_filter):
        self.__document_filter = document_filter
        return self

    @property
    def document_filter(self):
        return self.__document_filter
