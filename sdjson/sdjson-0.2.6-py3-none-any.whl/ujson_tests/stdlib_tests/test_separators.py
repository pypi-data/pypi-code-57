# stdlib
import textwrap

# 3rd party
import pytest

# this package
import sd_ujson


@pytest.mark.xfail(reason="separators is not supported by ujson")
def test_separators():
    h = [['blorpie'], ['whoops'], [], 'd-shtaeou', 'd-nthiouh', 'i-vhbjkhnth',
         {'nifty': 87}, {'field': 'yes', 'morefield': False} ]

    expect = textwrap.dedent("""\
    [
      [
        "blorpie"
      ] ,
      [
        "whoops"
      ] ,
      [] ,
      "d-shtaeou" ,
      "d-nthiouh" ,
      "i-vhbjkhnth" ,
      {
        "nifty" : 87
      } ,
      {
        "field" : "yes" ,
        "morefield" : false
      }
    ]""")


    d1 = sd_ujson.dumps(h)
    d2 = sd_ujson.dumps(h, indent=2, sort_keys=True, separators=(' ,', ' : '))

    h1 = sd_ujson.loads(d1)
    h2 = sd_ujson.loads(d2)

    assert h1 == h
    assert h2 == h
    assert d2 == expect


@pytest.mark.skip(reason="separators is not supported by ujson")
def test_illegal_separators():
    h = {1: 2, 3: 4}
    with pytest.raises(TypeError):
        sd_ujson.dumps(h, separators=(b', ', ': '))
    with pytest.raises(TypeError):
        sd_ujson.dumps(h, separators=(', ', b': '))
    with pytest.raises(TypeError):
        sd_ujson.dumps(h, separators=(b', ', b': '))

