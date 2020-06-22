from tokenizer_tools.tagset.offset.corpus import Corpus
from tokenizer_tools.tagset.offset.corpus_metric import CorpusMetric, MetricUnavailable


def test_corpus_metric(datadir):
    corpus = Corpus.read_from_file(datadir / "true.conllx")

    cm = CorpusMetric.create_from_corpus(corpus, corpus)

    assert cm.entity_f1_score == 1.0
    assert cm.entity_accuracy_score == 1.0
    assert cm.entity_recall_score == 1.0
