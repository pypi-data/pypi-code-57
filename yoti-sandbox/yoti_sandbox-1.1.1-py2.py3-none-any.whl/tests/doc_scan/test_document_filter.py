from yoti_python_sandbox.doc_scan import SandboxDocumentFilterBuilder


def test_should_allow_multiple_document_types():
    result = (
        SandboxDocumentFilterBuilder()
        .with_document_type("PASSPORT")
        .with_document_type("DRIVING_LICENCE")
        .build()
    )

    assert len(result.document_types) == 2
    assert result.document_types[0] == "PASSPORT"
    assert result.document_types[1] == "DRIVING_LICENCE"


def test_should_allow_multiple_country_codes():
    result = (
        SandboxDocumentFilterBuilder()
        .with_country_code("GBR")
        .with_country_code("USA")
        .build()
    )

    assert len(result.country_codes) == 2
    assert result.country_codes[0] == "GBR"
    assert result.country_codes[1] == "USA"
