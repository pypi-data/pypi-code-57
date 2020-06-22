from typing import Callable, Tuple, List
import collections
from tokenizer_tools.tagset.offset.plottable_counter import PlottableCounter as Counter

from tokenizer_tools.tagset.offset.corpus import Corpus
from tokenizer_tools.tagset.offset.document import Document
from tokenizer_tools.tagset.offset.document_compare_ways import DocumentCompareWays
import plotly.express as px
import pandas as pd
from tqdm import tqdm


class Diff:
    def __init__(self, df):
        self.df = df

    def get_figure(self):
        fig = px.parallel_categories(self.df)

        return fig


class CorpusDiff:
    def __init__(self, domain_diff, intent_diff, entity_diff, entity_mismatch):
        self.domain_diff = domain_diff
        self.intent_diff = intent_diff
        self.entity_diff = entity_diff
        self.entity_mismatch = entity_mismatch

    def compare(self, x, y):
        # check
        if x.get_all_doc_ids() != y.get_all_doc_ids():
            raise ValueError("left and right corpus are not equal")

        doc_id_list = x.get_all_doc_ids()
        diff_pair_list = []
        for doc_id in tqdm(doc_id_list):
            left_doc = x.get_doc_by_id(doc_id)
            right_doc = y.get_doc_by_id(doc_id)

            if left_doc == right_doc:
                continue

            diff_pair = DocumentDiffResult(left_doc, right_doc)
            diff_pair_list.append(diff_pair)

        return CorpusDiffResult(diff_pair_list)

    @classmethod
    def create_from_corpus(cls, x: Corpus, y: Corpus):
        intent_diff = cls._compare_intent(x, y)
        domain_diff = cls._compare_domain(x, y)
        entity_diff, entity_mismatch = cls._compare_entity(x, y)
        # TODO: maybe we need a document_diff
        return cls(domain_diff, intent_diff, entity_diff, entity_mismatch)

    @classmethod
    def _compare_intent(cls, x: Corpus, y: Corpus):
        return cls._compare_attr(x, y, "intent")

    @classmethod
    def _compare_domain(cls, x: Corpus, y: Corpus):
        return cls._compare_attr(x, y, "domain")

    @classmethod
    def _compare_attr(cls, x: Corpus, y: Corpus, attr):
        doc_ids = set(x.get_all_doc_ids() + y.get_all_doc_ids())

        x_col = []
        y_col = []
        for doc_id in tqdm(doc_ids):
            x_doc = x.get_doc_by_id(doc_id)
            y_doc = y.get_doc_by_id(doc_id)

            x_attr = getattr(x_doc, attr, "N/A")
            y_attr = getattr(y_doc, attr, "N/A")

            x_col.append(x_attr)
            y_col.append(y_attr)

        df = pd.DataFrame.from_dict({"x": x_col, "y": y_col})

        return Diff(df)

    @classmethod
    def _compare_entity(cls, x: Corpus, y: Corpus):
        doc_ids = set(x.get_all_doc_ids() + y.get_all_doc_ids())

        x_col = []
        x_val_col = []
        y_col = []
        y_val_col = []
        for doc_id in tqdm(doc_ids):
            x_doc = x.get_doc_by_id(doc_id)
            y_doc = y.get_doc_by_id(doc_id)

            if x_doc is None or y_doc is None:
                pass

            x_spans = {(i.start, i.end) for i in x_doc.span_set}
            y_spans = {(i.start, i.end) for i in y_doc.span_set}

            x_dict = {(i.start, i.end): i for i in x_doc.span_set}
            y_dict = {(i.start, i.end): i for i in y_doc.span_set}

            common_spans = x_spans & y_spans
            x_only_spans = x_spans - y_spans
            y_only_spans = y_spans - x_spans

            for span_loc in common_spans:
                x_col.append(x_dict[span_loc].entity)
                x_val_col.append(x_dict[span_loc].value)
                y_col.append(y_dict[span_loc].entity)
                y_val_col.append(y_dict[span_loc].value)

            for span_loc in x_only_spans:
                x_col.append(x_dict[span_loc].entity)
                x_val_col.append(x_dict[span_loc].value)
                y_col.append(("N/A"))
                y_val_col.append(("N/A"))

            for span_loc in y_only_spans:
                x_col.append(("N/A"))
                x_val_col.append(("N/A"))
                y_col.append(y_dict[span_loc].entity)
                y_val_col.append(y_dict[span_loc].value)

        df = pd.DataFrame.from_dict(
            {"x": x_col, "x_val": x_val_col, "y": y_col, "y_val": y_val_col}
        )

        mismatch = collections.defaultdict(list)
        for _, row in df.iterrows():
            key = (row["x"], row["y"])
            value = (tuple(row["x_val"]), tuple(row["y_val"]))
            mismatch[key].append(value)

        mismatch_counter = {}
        for k, v in mismatch.items():
            mismatch_counter[k] = Counter(v)

        return Diff(df[["x", "y"]]), mismatch_counter

    def set_document_compare_way(self, compare_way: DocumentCompareWays):
        self.x.set_document_compare_way(compare_way)
        self.y.set_document_compare_way(compare_way)

    def set_document_compare_method(
        self, compare_method: Callable[["Sequence", "Sequence"], bool]
    ):
        self.x.set_document_compare_method(compare_method)
        self.y.set_document_compare_method(compare_method)

    def set_document_hash_method(self, hash_method: Callable[["Sequence"], int]):
        self.x.set_document_compare_method(hash_method)
        self.y.set_document_compare_method(hash_method)


class DocumentDiffResult:
    def __init__(self, left: Document, right: Document):
        assert left.id == right.id

        self.left = left
        self.right = right

        self.id = left.id


class CorpusDiffResult(List[DocumentDiffResult]):
    def render_to_md(self) -> str:
        doc_pair_segment_list = []
        for doc_diff_result in self:
            doc_pair_segment = "# {}\n- {}\n- {}".format(
                doc_diff_result.id, doc_diff_result.left, doc_diff_result.right
            )
            doc_pair_segment_list.append(doc_pair_segment)

        return "\n\n".join(doc_pair_segment_list)
