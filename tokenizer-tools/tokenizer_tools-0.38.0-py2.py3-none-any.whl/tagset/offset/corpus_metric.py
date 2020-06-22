from typing import Tuple
import statistics

from sklearn.metrics import confusion_matrix

from tokenizer_tools.tagset.offset import seqeval as seq_metrics
from tokenizer_tools.tagset.offset.corpus import Corpus


class MetricUnavailable:
    pass


class CorpusMetric:
    """metrics for corpus between gold and predicted"""

    def __init__(
        self,
        intent_confusion_matrix=None,
        domain_confusion_matrix=None,
        entity_f1_score=None,
        entity_accuracy_score=None,
        entity_precision_score=None,
        entity_recall_score=None,
        entity_classification_report=None,
        doc_entity_correctness=None,
    ):
        super().__init__()

        self.intent_confusion_matrix = intent_confusion_matrix
        self.domain_confusion_matrix = domain_confusion_matrix
        self.entity_f1_score = entity_f1_score
        self.entity_accuracy_score = entity_accuracy_score
        self.entity_precision_score = entity_precision_score
        self.entity_recall_score = entity_recall_score
        self.entity_classification_report = entity_classification_report
        self.doc_entity_correctness = doc_entity_correctness

    @classmethod
    def create_from_corpus(cls, true, pred, skip_match=False):
        if not skip_match:
            true, pred = cls._make_corpus_match(true, pred)

        intent_confusion_matrix = cls._intent_confusion_matrix(true, pred)
        domain_confusion_matrix = cls._domain_confusion_matrix(true, pred)
        entity_f1_score = cls._entity_f1_score(true, pred)
        entity_accuracy_score = cls._entity_accuracy_score(true, pred)
        entity_precision_score = cls._entity_precision_score(true, pred)
        entity_recall_score = cls._entity_recall_score(true, pred)
        entity_classification_report = cls._entity_classification_report(true, pred)
        doc_entity_correctness = cls._doc_entity_correctness(true, pred)

        return cls(
            intent_confusion_matrix,
            domain_confusion_matrix,
            entity_f1_score,
            entity_accuracy_score,
            entity_precision_score,
            entity_recall_score,
            entity_classification_report,
            doc_entity_correctness,
        )

    @classmethod
    def _make_corpus_match(cls, true: Corpus, pred: Corpus) -> Tuple[Corpus, Corpus]:
        assert len(true) == len(pred)
        assert set(true.get_all_doc_ids()) == set(pred.get_all_doc_ids())

        sorted_pred = Corpus([pred.get_doc_by_id(true_doc.id) for true_doc in true])

        return true, sorted_pred

    @classmethod
    def _intent_confusion_matrix(cls, true, pred):
        return cls._attr_confusion_matrix(true, pred, "intent")

    @classmethod
    def _domain_confusion_matrix(cls, true, pred):
        return cls._attr_confusion_matrix(true, pred, "domain")

    @classmethod
    def _attr_confusion_matrix(cls, true, pred, attr):
        true_attr = [getattr(doc, attr) for doc in true]
        pred_attr = [getattr(doc, attr) for doc in pred]

        if None in true_attr or None in pred_attr:
            return MetricUnavailable()

        return confusion_matrix(true_attr, pred_attr)

    @classmethod
    def _entity_f1_score(cls, true, pred):
        return seq_metrics.f1_score(true, pred)

    @classmethod
    def _entity_accuracy_score(cls, true, pred):
        return seq_metrics.accuracy_score(true, pred)

    @classmethod
    def _entity_precision_score(cls, true, pred):
        return seq_metrics.precision_score(true, pred)

    @classmethod
    def _entity_recall_score(cls, true, pred):
        return seq_metrics.recall_score(true, pred)

    @classmethod
    def _entity_classification_report(cls, true, pred):
        return seq_metrics.classification_report(true, pred)

    @classmethod
    def _doc_entity_correctness(cls, true, pred):
        flags = []
        for gold_doc, pred_doc in zip(true, pred):
            flags.append(int(gold_doc.span_set == pred_doc.span_set))

        return statistics.mean(flags)
