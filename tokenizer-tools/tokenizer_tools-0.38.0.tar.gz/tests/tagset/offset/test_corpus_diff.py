from tokenizer_tools.tagset.offset.corpus import Corpus
from tokenizer_tools.tagset.offset.corpus_diff import CorpusDiff


# def test_corpus_diff(datadir):
#     corpus_one = Corpus.read_from_file(datadir / "corpus_one.conllx")
#     corpus_two = Corpus.read_from_file(datadir / "corpus_two.conllx")

#     corpus_diff = CorpusDiff(corpus_one, corpus_two)
#     corpus_diff_result = corpus_diff.compare()
#     result = corpus_diff_result.render_to_md()
#     expected = """# 3
# - <D: None, F: None, S: None, I: None>    [王 小 明](PERSON) 在 [台 北 新 竹](GPE) 的 [清 华 大 学](ORG) 读 书 。
# - <D: None, F: None, S: None, I: None>    [王 小 明](PERSON) 在 [台 北 新 竹](CITY) 的 [清 华 大 学](ORG) 读 书 。"""
#     assert result == expected

def test_corpus_diff_intent(datadir):
    corpus_one = Corpus.read_from_file(datadir / "corpus_one.conllx")
    corpus_two = Corpus.read_from_file(datadir / "corpus_two.conllx")

    corpus_diff = CorpusDiff.create_from_corpus(corpus_one, corpus_two)
    fig = corpus_diff.intent_diff.get_figure()

    assert fig

def test_corpus_diff_entity(datadir):
    corpus_one = Corpus.read_from_file(datadir / "corpus_one.conllx")
    corpus_two = Corpus.read_from_file(datadir / "corpus_two.conllx")

    corpus_diff = CorpusDiff.create_from_corpus(corpus_one, corpus_two)
    fig = corpus_diff.entity_diff.get_figure()

    assert fig
