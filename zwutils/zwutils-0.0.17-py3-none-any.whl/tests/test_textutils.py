import pytest

from zwutils import textutils as tu

def test_is_chinese():
    assert tu.is_chinese('我') == True
    assert tu.is_chinese('A') == False
    assert tu.is_chinese('體') == True
    assert tu.is_chinese('一') == True

@pytest.mark.parametrize(
    'sentence, result', (
        ('  Zhaowei  is NO1, 一天吃 1 顿 ， 1 顿 吃 一 天 ', 'Zhaowei is NO1,一天吃1顿，1顿吃一天'),
    )
)
def test_remove_space_in_sentence(sentence, result):
    out = tu.remove_space_in_sentence(sentence)
    assert out == result