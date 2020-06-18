from mock import Mock

from yoti_python_sandbox.doc_scan.document_filter import SandboxDocumentFilter
from yoti_python_sandbox.doc_scan.task import (
    SandboxDocumentTextDataExtractionTaskBuilder,
)


def test_should_allow_single_key_value_document_field():
    result = (
        SandboxDocumentTextDataExtractionTaskBuilder()
        .with_document_field("someKey", "someValue")
        .build()
    )

    assert "someKey" in result.result.document_fields
    assert result.result.document_fields.get("someKey") == "someValue"


def test_should_accept_document_filter():
    document_filter_mock = Mock(spec=SandboxDocumentFilter)

    result = (
        SandboxDocumentTextDataExtractionTaskBuilder()
        .with_document_filter(document_filter_mock)
        .build()
    )

    assert result.document_filter == document_filter_mock
