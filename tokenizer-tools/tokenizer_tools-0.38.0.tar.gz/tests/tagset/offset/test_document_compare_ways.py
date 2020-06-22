import random

from tokenizer_tools.tagset.offset.document_compare_ways import (
    corpus_set_compare_way,
    corpus_get_compare_way,
    DocumentCompareContext,
)
from tokenizer_tools.tagset.offset import document_compare_ways


def test_corpus_set_compare_way():
    expected = random.randint(1, 1e100)

    corpus_set_compare_way(expected)

    result = document_compare_ways.GLOBAL_CORPUS_COMPARE_WAY

    assert result == expected


def test_corpus_get_compare_way():
    expected = random.randint(1, 1e100)
    document_compare_ways.GLOBAL_CORPUS_COMPARE_WAY = expected

    result = corpus_get_compare_way()

    assert result == expected


def test_document_compare_context():
    out_context_expected = "NOT_WANTED"

    document_compare_ways.GLOBAL_CORPUS_COMPARE_WAY = out_context_expected

    in_context_exptected = random.randint(1, 1e100)

    with DocumentCompareContext(in_context_exptected):
        in_context_result = corpus_get_compare_way()

        assert in_context_result == in_context_exptected

    out_context_result = corpus_get_compare_way()

    assert out_context_result == out_context_expected

    # reset to default, otherwise will pollute other test cases
    document_compare_ways.reset_global_corpus_compare_way()
