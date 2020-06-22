import collections
import copy
from typing import Tuple, Dict, Any

from tokenizer_tools.tagset.offset.analysis.document_pattern import \
    DocumentPattern
from tokenizer_tools.tagset.offset.analysis.entity_placeholder import \
    EntityPlaceholder
from tokenizer_tools.tagset.offset.corpus import Corpus
from tokenizer_tools.tagset.offset.document import Document


class ExpressPattern:
    def __init__(self, corpus: Corpus):
        self.corpus = corpus

    def compute(self) -> Dict[DocumentPattern, Document]:
        pattern_mapping = collections.defaultdict(list)
        for doc in self.corpus:
            pattern = self.convert_to_pattern(doc)
            pattern_mapping[pattern].append(doc)

        return dict(pattern_mapping)

    @staticmethod
    def convert_to_pattern(doc: Document) -> DocumentPattern:
        dp = DocumentPattern.build_from_document(doc)

        return dp
