from tokenizer_tools.tagset.offset.analysis.document_pattern import DocumentPattern
from tokenizer_tools.tagset.offset.analysis.entity_placeholder import EntityPlaceholder
from tokenizer_tools.tagset.offset.span_set import SpanSet


def test_document_pattern():
    # construct a pattern object
    dp = DocumentPattern("name 的 goods".split())

    dp.entities = SpanSet(
        [
            EntityPlaceholder(start=0, end=1, entity="name"),
            EntityPlaceholder(start=2, end=3, entity="goods"),
        ]
    )
    dp.label = "LABEL"

    # test if render method works

    doc = dp.render({"name": ["Real", "Name"], "goods": ["RealGoods"]})
    assert doc.label == "LABEL"

    expected_doc_snippet = "[RealName](name)的[RealGoods](goods)"
    result_doc = str(doc)

    assert expected_doc_snippet in result_doc

    # make sure DocumentPattern is untouched

    expected_pattern_snippet = "<name>的<goods>"
    result_pattern = str(dp)

    assert expected_pattern_snippet in result_pattern
