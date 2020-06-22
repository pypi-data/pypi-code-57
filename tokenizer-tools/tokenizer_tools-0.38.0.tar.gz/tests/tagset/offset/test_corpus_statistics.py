from collections import Counter

from tokenizer_tools.tagset.offset.corpus import Corpus
from tokenizer_tools.tagset.offset.document import Document
from tokenizer_tools.tagset.offset.corpus_statistics import CorpusStatistics


def test_eq__(datadir):
    corpus = Corpus.read_from_file(datadir / "data.conllx")

    corpus_statistics = CorpusStatistics.create_from_corpus(corpus)

    expected = CorpusStatistics(
        domain=Counter({"domain_one": 2, "domain_two": 2}),
        function=Counter({"function_one": 2, "function_two": 2}),
        sub_function=Counter({"sub_function_one": 2, "sub_function_two": 2}),
        intent=Counter({"intent_one": 2, "intent_two": 2}),
        entity_types={
            "PERSON": Counter({("王", "小", "明"): 2}),
            "GPE": Counter({("北", "京"): 2}),
            "ORG": Counter({("清", "华", "大", "学"): 2}),
            "歌手名": Counter({("蓝", "泽", "雨"): 2}),
        },
        entity_values={
            ("王", "小", "明"): Counter({"PERSON": 2}),
            ("北", "京"): Counter({"GPE": 2}),
            ("清", "华", "大", "学"): Counter({"ORG": 2}),
            ("蓝", "泽", "雨"): Counter({"歌手名": 2}),
        },
    )

    assert corpus_statistics == expected


def test_collect_domain(datadir):
    corpus = Corpus.read_from_file(datadir / "data.conllx")

    corpus_statistics = CorpusStatistics.create_from_corpus(corpus)

    result = corpus_statistics.domain

    expected = Counter({"domain_one": 2, "domain_two": 2})

    assert result == expected


def test_collect_function(datadir):
    corpus = Corpus.read_from_file(datadir / "data.conllx")

    corpus_statistics = CorpusStatistics.create_from_corpus(corpus)

    result = corpus_statistics.function

    expected = Counter({"function_one": 2, "function_two": 2})

    assert result == expected


def test_collect_sub_function(datadir):
    corpus = Corpus.read_from_file(datadir / "data.conllx")

    corpus_statistics = CorpusStatistics.create_from_corpus(corpus)

    result = corpus_statistics.sub_function

    expected = Counter({"sub_function_one": 2, "sub_function_two": 2})

    assert result == expected


def test_collect_intent(datadir):
    corpus = Corpus.read_from_file(datadir / "data.conllx")

    corpus_statistics = CorpusStatistics.create_from_corpus(corpus)

    result = corpus_statistics.intent

    expected = Counter({"intent_one": 2, "intent_two": 2})

    assert result == expected


def test_collect_entity_types(datadir):
    corpus = Corpus.read_from_file(datadir / "data.conllx")

    corpus_statistics = CorpusStatistics.create_from_corpus(corpus)

    result = corpus_statistics.entity_types

    expected = {
        "PERSON": Counter([("王", "小", "明"), ("王", "小", "明")]),
        "GPE": Counter([("北", "京"), ("北", "京")]),
        "ORG": Counter([("清", "华", "大", "学"), ("清", "华", "大", "学")]),
        "歌手名": Counter([("蓝", "泽", "雨"), ("蓝", "泽", "雨")]),
    }

    assert result == expected


def test_collect_entity_values(datadir):
    corpus = Corpus.read_from_file(datadir / "data.conllx")

    corpus_statistics = CorpusStatistics.create_from_corpus(corpus)

    result = corpus_statistics.entity_values

    expected = {
        ("王", "小", "明"): Counter(["PERSON", "PERSON"]),
        ("北", "京"): Counter(["GPE", "GPE"]),
        ("清", "华", "大", "学"): Counter(["ORG", "ORG"]),
        ("蓝", "泽", "雨"): Counter(["歌手名", "歌手名"]),
    }

    assert result == expected


def test_collect_token_values(datadir):
    corpus = Corpus.read_from_file(datadir / "data.conllx")

    corpus_statistics = CorpusStatistics.create_from_corpus(corpus)

    result = corpus_statistics.token_values["在"]

    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], Document)
