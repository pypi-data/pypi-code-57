import collections
from tokenizer_tools.tagset.offset.document import Document
from tokenizer_tools.tagset.offset.span import Span
from tokenizer_tools.tagset.offset.exceptions import OffsetSpanCheckError
import operator


def test_repr__():
    span = Span(0, 9, "entity")
    assert repr(span) == "Span(0, 9, 'entity', value=None, normal_value=None)"

def test_eq__():
    a = Span(0, 1, "entity")
    b = Span(0, 1, "entity")
    assert a == b

    c = Span(0, 2, "entity")
    assert a != c

def test_hash__():
    a = Span(0, 1, "entity")

    assert isinstance(a, collections.Hashable)

def test_init__():
    try:
        a = Span(-1, 1, "entity")
    except Exception as e:
        assert isinstance(e, OffsetSpanCheckError)
        #assert True == operator.eq(e, OffsetSpanCheckError("start index should greater or equal than zero"))
        #assert e.eq(OffsetSpanCheckError("start index should greater or equal than zero"))

    try:
        a = Span(6, 1, "entity")
    except Exception as e:
        assert isinstance(e, OffsetSpanCheckError)
        #assert e == OffsetSpanCheckError("end is smaller than or equal to start")

    try:
        a = Span(1, 3, '')
    except Exception as e:
        print(e)
        assert isinstance(e, OffsetSpanCheckError)
        #assert e == OffsetSpanCheckError("this is a illlegal entity")

    try:
        a = Span(1, 3, "entity", 'aaaa')
    except Exception as e:
        assert isinstance(e, ValueError)
        # assert e == ValueError(
        #                 "argument value={} is not supported anymore, ignore it".format('aaaa')
        #             )

def test_bind1():
    a = Span(1, 3, 'entity')
    a.bind("Sequence")
    #print(repr(a))

def test_bind():
    doc = Document("abc")
    doc.span_set.append(Span(start=0, end=1, entity="a"))

    result = doc.convert_to_md()
    expected = "[a](a)bc"

    assert result == expected

    span = doc.span_set[0]
    span.bind(doc)

    span.value = ["a", "a", "a"]
    result = doc.convert_to_md()
    expected = "[aaa](a)bc"

    assert result == expected

def test_deepcopy():
    a = Span(3, 9, 'nice')
    b = {}
    Span.__deepcopy__(a, b)
    print(repr(b))

def test_value():
    a = Span(3, 9, 'nice')
    #a.host.text = []
    print(a.value)

def test_fetch_value_from_text():
    a = Span(3, 9, 'nice')
    b = a.fetch_value_from_text("hahahahaha")
    assert 'ahahah' == b

def test_update_value():
    a = Span(3, 9, 'nice')
    #a.host.text = 'coiciweicvwpfvwmg';
    #a.update_value('cdd')
    print(a)

def test_check_match():
    a = Span(3, 9, 'nice')
    assert False == a.check_match('aa')

def test_fill_text():
    a = Span(3, 9, 'nice')
    #a.fill_text('niveveiogkoverokveoi')
    print(a)
