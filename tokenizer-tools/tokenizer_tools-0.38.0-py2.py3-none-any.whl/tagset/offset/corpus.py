from typing import Union, List, Tuple, Callable

import numpy as np
from sklearn.model_selection import train_test_split
from fuzzywuzzy import process
from tqdm import tqdm

from tokenizer_tools.conllz.reader import load_conllx
from tokenizer_tools.tagset.NER.BILUO import BILUOEncoderDecoder
from tokenizer_tools.conllz.writer import write_conllx
from tokenizer_tools.converter.conllx_to_offset import conllx_to_offset
from tokenizer_tools.converter.offset_to_sentence import offset_to_sentence
from tokenizer_tools.tagset.offset.corpus_statistics import CorpusStatistics
from tokenizer_tools.tagset.offset.document import Document
from tokenizer_tools.tagset.offset.document_compare_ways import DocumentCompareWays
from tokenizer_tools.tagset.offset.corpus_stream_writer import CorpusStreamWriter
from tokenizer_tools.tagset.offset.corpus_stream_reader import CorpusStreamReader


class Corpus(List[Document]):
    """
    This Corpus means a single corpus object.
     single corpus file can stored in single file (implemented already)
      or multiple files (not implemented yet).

    a single corpus object contains any number of example. example is the basic unit for model training/evaluate/test.

    The corpus object is a list-like object. it has all the methods and attributes a list should have.
     the only constraint is that the basic element/item in this list container is example.

    TODO: also it should have same behavior (see https://docs.python.org/3.6/library/stdtypes.html#set) with set type:
        isdisjoint, issubset, issuperset, union, intersection, difference, symmetric_difference
    """

    @classmethod
    def read_from_file(cls, data_file):
        offset_data_list = []

        with open(data_file, "rt") as fd:
            for sentence in tqdm(load_conllx(fd)):
                offset_data, result = conllx_to_offset(sentence)

                offset_data_list.append(offset_data)

        return Corpus(offset_data_list)

    def write_to_file(self, output_file):
        sentence_list = [offset_to_sentence(offset) for offset in self]

        with open(output_file, "wt") as fd:
            write_conllx(sentence_list, fd)

    def train_test_split(self, **kwargs) -> Tuple["Corpus", "Corpus"]:
        """
        split corpus into train set and test set
        :param kwargs: kwargs passed directly to sklearn.model_selection.train_test_split
        :return: train_corpus, test_corpus
        """
        train_set, test_set = train_test_split(self, **kwargs)

        return Corpus(train_set), Corpus(test_set)

    def set_document_compare_way(self, compare_way: DocumentCompareWays):
        for document in self:
            document.set_compare_way(compare_way)

    def set_document_compare_method(
        self, compare_method: Callable[["Sequence", "Sequence"], bool]
    ):
        for document in self:
            document.set_compare_method(compare_method)

    def set_document_hash_method(self, hash_method: Callable[["Sequence"], int]):
        for document in self:
            document.set_hash_method(hash_method)

    def __hash__(self):
        return hash(frozenset(self))

    def __eq__(self, other):
        return frozenset(self) == frozenset(other)

    def __getitem__(self, item) -> Union[Document, "Corpus"]:
        if isinstance(item, (np.ndarray, list)):
            subset = []
            for i in item:
                subset.append(self[i])

            return self.__class__(subset)
        else:
            return super().__getitem__(item)

    def __contains__(self, item):
        return item in frozenset(self)

    def isdisjoint(self, other):
        pass

    def issubset(self, other):
        pass

    def issuperset(self, other):
        pass

    def union(self, *others):
        union_corpus = None
        for other in others:
            if union_corpus is None:
                union_corpus = set(self)

            union_corpus = union_corpus.union(set(other))

        return self.__class__(list(union_corpus))

    def intersection(self, *others) -> "Corpus":
        intersection_corpus = None
        for other in others:
            if intersection_corpus is None:
                intersection_corpus = set(self)

            intersection_corpus = intersection_corpus.intersection(set(other))

        return self.__class__(list(intersection_corpus))

    def difference(self, *others):
        difference_corpus = None
        for other in others:
            if difference_corpus is None:
                difference_corpus = set(self)

            difference_corpus = difference_corpus.difference(set(other))

        return self.__class__(list(difference_corpus))

    def symmetric_difference(self, other):
        return self.__class__(list(set(self).symmetric_difference(other)))

    def remove_duplicate(self) -> "Corpus":
        set_corpus = set(self)
        duplicate_free_corpus = self.__class__(set_corpus)
        return duplicate_free_corpus

    def generate_statistics(self) -> CorpusStatistics:
        return CorpusStatistics.create_from_corpus(self)

    def generate_pattern(self) -> "CorpusPattern":
        from tokenizer_tools.tagset.offset.analysis.corpus_pattern import CorpusPattern

        return CorpusPattern.create_from_corpus(self)

    def get_all_doc_ids(self) -> List[str]:
        id_list = list([i.id for i in self])
        if len(id_list) != len(set(id_list)):
            raise ValueError("Document ids have duplicate")

        return id_list

    def get_doc_by_id(self, doc_id, default=None):
        for doc in self:
            if doc.id == doc_id:
                return doc
        return default

    def fuzzy_search(self, query, limit=3) -> List[Tuple[Document, int]]:
        choices = self
        result = process.extract(query, choices, limit=limit)

        return result

    def partial_search(self, query: Union[List, tuple, str]) -> List[Tuple[Document, int]]:
        """
        return document and a int which represent the remain char in doc beside the query chars
        """
        if isinstance(query, (list, tuple)):
            query = "".join(query)

        query_len = len(query)
        result = []
        for doc in self:
            doc_text = "".join(doc.text)
            if query in doc_text:
                result.append((doc, len(doc_text) - query_len))

        return sorted(result, key=lambda x: x[1])

    def annotation_tags(self, scheme=None) -> List[str]:
        if scheme is not None:
            raise ValueError("scheme argument is not supported yet")

        entities = {span.entity for doc in self for span in doc.span_set}

        tags = {
            i for entity in entities for i in BILUOEncoderDecoder(entity).all_tag_set()
        }

        # for better human reading, sort it
        tags_except_oscar = tags - {"O"}

        sorted_tags = ["O"] + sorted(tags_except_oscar)

        return sorted_tags

    @classmethod
    def stream_writer(cls, file_path: str) -> CorpusStreamWriter:
        return CorpusStreamWriter(file_path)

    @classmethod
    def stream_reader(cls, file_path: str) -> CorpusStreamReader:
        return CorpusStreamReader(file_path)
