from enum import Enum
from typing import Dict


def consider_text_only_document_compare_function(self, other):
    return self.text == other.text


def consider_text_only_document_hash_function(self):
    return hash(frozenset(self.text))


def consider_text_entity_compare_function(self, other):
    return self.text == other.text and self.span_set == other.span_set


def corpus_set_compare_way(compare_way):
    # set global corpus compare way
    global GLOBAL_CORPUS_COMPARE_WAY

    GLOBAL_CORPUS_COMPARE_WAY = compare_way


def corpus_get_compare_way():
    # get global corpus compare way
    return GLOBAL_CORPUS_COMPARE_WAY


def consider_text_entity_hash_function(self):
    return hash((frozenset(self.text), self.span_set))


def consider_all_compare_function(self, other):
    return (
        self.text == other.text
        and self.span_set == other.span_set
        and self.extra_attr == other.extra_attr
    )


def consider_all_hash_method(self):
    return hash((frozenset(self.text), self.span_set, self.label))


class DocumentCompareContext:
    def __init__(self, current_context):
        self.current_context = current_context
        self.previous_context = None

    def __enter__(self):
        # save current compare way
        self.previous_context = corpus_get_compare_way()

        # set up new compare way
        corpus_set_compare_way(self.current_context)

    def __exit__(self, exception_type, exception_value, traceback):
        # restore the old compare way
        corpus_set_compare_way(self.previous_context)

        if exception_value is not None:  # an exception has occurred
            return False  # reraise the exception


class DocumentCompareWays(Enum):
    ALL = {
        "eq": consider_all_compare_function,
        "hash": consider_all_hash_method
    }
    TEXT_ONLY = {
        "eq": consider_text_only_document_compare_function,
        "hash": consider_text_only_document_hash_function,
    }
    TEXT_ENTITY_ONLY = {
        "eq": consider_text_only_document_compare_function,
        "hash": consider_text_entity_hash_function,
    }
    TEXT_ENTITY_INTENT_ONLY = 3
    TEXT_ENTITY_INTENT_DOMAIN = 4


GLOBAL_CORPUS_COMPARE_WAY = None


def reset_global_corpus_compare_way():
    global GLOBAL_CORPUS_COMPARE_WAY
    GLOBAL_CORPUS_COMPARE_WAY = DocumentCompareWays.ALL.value


# call function to set up the default one
reset_global_corpus_compare_way()
