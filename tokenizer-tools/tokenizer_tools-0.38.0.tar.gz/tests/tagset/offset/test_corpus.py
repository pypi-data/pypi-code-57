import filecmp

from tokenizer_tools.tagset.offset.document import Document
from tokenizer_tools.tagset.offset.span import Span
from tokenizer_tools.tagset.offset.corpus import Corpus
from tokenizer_tools.tagset.offset.document_compare_ways import DocumentCompareWays
from tokenizer_tools.tagset.offset.span_set import SpanSet

seq = Document("王小明在北京的清华大学读书。", id="1")
seq.span_set.append(Span(0, 3, "PERSON"))
seq.span_set.append(Span(4, 6, "GPE"))
seq.span_set.append(Span(7, 11, "ORG"))
seq_one = seq

seq = Document("来一首蓝泽雨的歌。", id="2")
seq.span_set.append(Span(3, 6, "歌手名"))
seq_two = seq


def test_read_from_file(datadir):
    corpus = Corpus.read_from_file(datadir / "output.conllx")

    assert len(corpus) == 2
    assert corpus[0] == seq_one
    assert corpus[1] == seq_two


def test_write_to_file(datadir, tmpdir):
    corpus = Corpus()

    corpus.append(seq_one)
    corpus.append(seq_two)

    result_file = tmpdir / "output.conllx"
    corpus.write_to_file(result_file)

    gold_file = datadir / "output.conllx"

    assert filecmp.cmp(result_file, gold_file)


def test_getitem__(datadir, tmpdir):
    corpus = Corpus()

    corpus.append(seq_one)
    corpus.append(seq_two)

    # test single element get item
    item = corpus[0]

    assert item == seq_one

    # test batch element get item
    other_corpus = corpus[[0, 1]]

    assert other_corpus == corpus


def test_contains__(datadir, tmpdir):
    corpus = Corpus()

    corpus.append(seq_one)
    corpus.append(seq_two)

    assert seq_one in corpus

    other_corpus = Document("")

    assert other_corpus not in corpus


def test_remove_duplicate(datadir):
    corpus = Corpus.read_from_file(datadir / "duplicate.conllx")

    assert len(corpus) == 4

    duplicate_free = corpus.remove_duplicate()

    assert isinstance(duplicate_free, Corpus)
    assert len(duplicate_free) == 2


def test_intersection(datadir):
    corpus = Corpus.read_from_file(datadir / "self.conllx")
    other_corpus = Corpus.read_from_file(datadir / "other.conllx")

    result = corpus.intersection(other_corpus)

    assert isinstance(result, Corpus)
    assert len(result) == 2

    second_corpus = Corpus.read_from_file(datadir / "second_other.conllx")
    result = corpus.intersection(other_corpus, second_corpus)

    assert isinstance(result, Corpus)
    assert len(result) == 1


def test_set_document_compare_function_and_set_document_hash_function(datadir):
    corpus_one = Corpus.read_from_file(datadir / "corpus_one.conllx")
    corpus_two = Corpus.read_from_file(datadir / "corpus_two.conllx")

    assert corpus_one != corpus_two

    def consider_text_only_document_compare_function(self, other):
        return self.text == other.text

    corpus_one.set_document_compare_method(consider_text_only_document_compare_function)
    corpus_two.set_document_compare_method(consider_text_only_document_compare_function)

    def consider_text_only_document_hash_function(self):
        return hash(frozenset(self.text))

    corpus_one.set_document_hash_method(consider_text_only_document_hash_function)
    corpus_two.set_document_hash_method(consider_text_only_document_hash_function)

    assert corpus_one == corpus_two


def test_set_document_compare_way(datadir):
    corpus_one = Corpus.read_from_file(datadir / "corpus_one.conllx")
    corpus_two = Corpus.read_from_file(datadir / "corpus_two.conllx")

    assert corpus_one != corpus_two

    corpus_one.set_document_compare_way(DocumentCompareWays.TEXT_ONLY)
    corpus_two.set_document_compare_way(DocumentCompareWays.TEXT_ONLY)

    assert corpus_one == corpus_two


def test_difference(datadir):
    corpus_one = Corpus.read_from_file(datadir / "corpus_one.conllx")
    corpus_two = Corpus.read_from_file(datadir / "corpus_two.conllx")

    result = corpus_one.difference(corpus_two)
    expected = Corpus(
        [
            Document(
                "王小明在台北新竹的清华大学读书。",
                span_set=SpanSet(
                    [Span(0, 3, "PERSON"), Span(4, 8, "GPE"), Span(9, 13, "ORG")]
                ),
                id="3",
            )
        ]
    )

    assert result == expected


def test_union(datadir):
    corpus_one = Corpus.read_from_file(datadir / "corpus_one.conllx")
    corpus_two = Corpus.read_from_file(datadir / "corpus_two.conllx")

    result = len(corpus_one.union(corpus_two))
    expected = 4

    assert result == expected


def test_symmetric_difference(datadir):
    corpus_one = Corpus.read_from_file(datadir / "corpus_one.conllx")
    corpus_two = Corpus.read_from_file(datadir / "corpus_two.conllx")

    result = len(corpus_one.symmetric_difference(corpus_two))
    expected = 2

    assert result == expected


def test_fuzzy_search(datadir):
    corpus = Corpus.read_from_file(datadir / "output.conllx")

    result = corpus.fuzzy_search("北京 读书", limit=1)

    expected = seq_one

    assert result[0][0] == expected
