from tokenizer_tools.tagset.offset.analysis.express_pattern import ExpressPattern
from tokenizer_tools.tagset.offset.corpus import Corpus


def test_express_pattern(datadir):
    corpus = Corpus.read_from_file(datadir / "corpus.conllx")

    express_pattern = ExpressPattern(corpus)
    result = express_pattern.compute()

    result_keys = [str(i) for i in result.keys()]

    expected_keys = ["<PERSON>在<GPE>的<ORG>读书。", "来一首<歌手名>的歌。"]

    for r, e in zip(result_keys, expected_keys):
        assert e in r

    result_value = result.values()

    expected_value = [
        [
            "[王小明](PERSON)在[北京](GPE)的[清华大学](ORG)读书。",
            "[王小明](PERSON)在[台北新竹](GPE)的[清华大学](ORG)读书。",
        ],
        ["来一首[蓝泽雨](歌手名)的歌。"],
    ]

    for i, value in enumerate(result_value):
        for j, element in enumerate(value):
            assert expected_value[i][j] in str(element)
