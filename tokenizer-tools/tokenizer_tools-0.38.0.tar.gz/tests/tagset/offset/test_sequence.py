from tokenizer_tools.tagset.offset.sequence import Sequence
from tokenizer_tools.tagset.offset.span import Span
from tokenizer_tools.tagset.offset.span_set import SpanSet


def test_check_span_set():
    seq = Sequence("王小明在北京的清华大学读书。")
    seq.span_set.append(Span(0, 3, 'PERSON'))
    seq.span_set.append(Span(4, 6, 'GPE'))
    seq.span_set.append(Span(7, 11, 'ORG'))

    result, overlapped_result = seq.check_span_set()
    assert result

    seq = Sequence("来一首蓝泽雨的歌。")
    seq.span_set.append(Span(3, 6, '歌手名'))
    seq.span_set.append(Span(5, 6, '歌曲名'))

    result, overlapped_result = seq.check_span_set()
    assert not result


def test_eq__():
    a = Sequence("text")

    b = Sequence("text")

    assert a == b

    c = Sequence("other_text")

    assert a != c

    d = Sequence('text')
    d.span_set.append(Span(0, 1, 'entity'))

    e = Sequence('text')
    e.span_set.append(Span(0, 1, 'entity'))

    assert d == e

    f = Sequence('text')
    f.span_set.append(Span(0, 2, 'entity'))

    assert d != f


def test_hash__():
    a = Sequence("text")

    b = Sequence("text")

    assert hash(a) == hash(b)

    c = Sequence("other_text")

    assert hash(a) != hash(c)

    d = Sequence('text')
    d.span_set.append(Span(0, 1, 'entity'))

    e = Sequence('text')
    e.span_set.append(Span(0, 1, 'entity'))

    assert hash(d) == hash(e)

    f = Sequence('text')
    f.span_set.append(Span(0, 2, 'entity'))

    assert hash(d) != hash(f)

    g = Sequence('text')
    g.span_set.append(Span(0, 1, 'entity'))
    g.span_set.append(Span(1, 2, 'entity'))

    h = Sequence('text')
    h.span_set.append(Span(0, 1, 'entity'))
    h.span_set.append(Span(1, 2, 'entity'))

    assert hash(g) == hash(h)

    i = Sequence('text')
    i.span_set.append(Span(0, 2, 'entity'))

    assert hash(g) != hash(i)


def test_set_compare_method():
    # test case 1
    a = Sequence('text')
    a.span_set.append(Span(0, 1, 'entity'))

    b = Sequence('text')
    b.span_set.append(Span(0, 1, 'other_entity'))

    assert a != b

    def consider_text_only_compare_method(self, other):
        return self.text == other.text

    a.set_compare_method(consider_text_only_compare_method)
    b.set_compare_method(consider_text_only_compare_method)

    assert a == b

    # test case 2
    a = Sequence('text')
    a.span_set.append(Span(0, 1, 'entity'))

    b = Sequence('other_text')
    b.span_set.append(Span(0, 1, 'entity'))

    assert a != b

    def consider_entity_only_compare_method(self, other):
        return self.span_set == other.span_set

    a.set_compare_method(consider_entity_only_compare_method)
    b.set_compare_method(consider_entity_only_compare_method)

    assert a == b


def test_set_hash_method():
    # test case 1
    a = Sequence('text')
    a.span_set.append(Span(0, 1, 'entity'))

    b = Sequence('text')
    b.span_set.append(Span(0, 1, 'other_entity'))

    assert hash(a) != hash(b)

    def consider_text_only_hash_method(self):
        return hash(frozenset(self.text))

    a.set_hash_method(consider_text_only_hash_method)
    b.set_hash_method(consider_text_only_hash_method)

    assert hash(a) == hash(b)

    # test case 2
    a = Sequence('text')
    a.span_set.append(Span(0, 1, 'entity'))

    b = Sequence('other_text')
    b.span_set.append(Span(0, 1, 'entity'))

    assert hash(a) != hash(b)

    def consider_entity_only_hash_method(self):
        return hash(self.span_set)

    a.set_hash_method(consider_entity_only_hash_method)
    b.set_hash_method(consider_entity_only_hash_method)

    assert hash(a) == hash(b)


def test_span_set_bind():
    seq = Sequence("abce", span_set=SpanSet([Span(1, 2, '1-2')]))

    result = seq.span_set[0].value
    expected = ["b"]

    assert result == expected
