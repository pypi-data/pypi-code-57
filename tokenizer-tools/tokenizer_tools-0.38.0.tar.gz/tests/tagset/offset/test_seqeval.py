"""
Evaluation test is performed for the following dataset.
https://www.clips.uantwerpen.be/conll2000/chunking/output.html
"""
# NOTE: this file adopted from https://github.com/chakki-works/seqeval
# modified for Document object

import os
import random
import subprocess
import unittest
from typing import List

import numpy
import pytest

from tokenizer_tools.tagset.NER.BILUO import tags_to_span_set
from tokenizer_tools.tagset.offset.corpus import Corpus
from tokenizer_tools.tagset.offset.document import Document
from tokenizer_tools.tagset.offset.seqeval import (
    accuracy_score,
    classification_report,
    f1_score,
    get_entities,
    performance_measure,
    precision_score,
    recall_score,
)
from tokenizer_tools.tagset.offset.span import Span
from tokenizer_tools.tagset.offset.span_set import SpanSet


@pytest.fixture
def self(datadir):
    y_true = build_mock_corpus_from_tags(
        [["O", "O", "O", "B-MISC", "L-MISC", "O", "U-ORG"], ["B-PER", "L-PER", "O"]]
    )
    y_pred = build_mock_corpus_from_tags(
        [["O", "O", "B-MISC", "I-MISC", "L-MISC", "O", "O"], ["B-PER", "L-PER", "O"]]
    )
    obj = type("MockedObject", (), {"y_true": y_true, "y_pred": y_pred})

    return obj


def build_mock_doc_from_tags(tags: List[str]) -> Document:
    doc = Document(["A"] * len(tags))
    doc.span_set = tags_to_span_set(tags)

    return doc


def build_mock_corpus_from_tags(tags: List[List[str]]) -> Corpus:
    docs = [build_mock_doc_from_tags(tag) for tag in tags]
    return Corpus(docs)


def test_get_entities():
    corpus = build_mock_corpus_from_tags(
        [
            ["O", "O", "O", "B-MISC", "I-MISC", "L-MISC", "O", "B-PER", "L-PER"],
            ["O", "O", "O", "B-MISC", "I-MISC", "L-MISC", "O", "B-PER", "L-PER"],
        ]
    )

    expected = [
        ("MISC", 3, 6, 0),
        ("PER", 7, 9, 0),
        ("MISC", 3, 6, 1),
        ("PER", 7, 9, 1),
    ]

    assert get_entities(corpus) == expected


def test_performance_measure():
    y_true = build_mock_corpus_from_tags(
        [["O", "O", "O", "B-MISC", "L-MISC", "O", "U-ORG"], ["B-PER", "L-PER", "O"]]
    )
    y_pred = build_mock_corpus_from_tags(
        [["O", "O", "B-MISC", "I-MISC", "L-MISC", "O", "O"], ["B-PER", "L-PER", "O"]]
    )
    performance_dict = performance_measure(y_true, y_pred)
    assert performance_dict == {"FN": 1, "FP": 3, "TN": 4, "TP": 3}


def test_classification_report(self):
    print(classification_report(self.y_true, self.y_pred))
