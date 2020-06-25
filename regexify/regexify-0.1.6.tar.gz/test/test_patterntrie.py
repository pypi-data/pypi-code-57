import re

import pytest
from hypothesis import given
import hypothesis.strategies as st

from regexify import PatternTrie


def test_pattern_matches_original():
    data = ['there', 'hi', 'python', 'pythons', 'hiya']
    trie = PatternTrie(*data)
    pat = re.compile(trie.pattern)
    for word in data:
        assert pat.match(word)


def test_assert_no_data_pattern():
    trie = PatternTrie(*[])
    with pytest.raises(ValueError):
        trie.pattern


def test_assert_nonword_pattern():
    trie = PatternTrie('')
    with pytest.raises(ValueError):
        trie.pattern


@given(st.lists(st.text(min_size=1), min_size=1))
def test_pattern_matches_original_hypothesis(words):
    pattern = PatternTrie(*words).pattern
    pat = re.compile(pattern)
    for word in words:
        assert pat.match(word)
