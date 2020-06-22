from tokenizer_tools.evaluator.tag_level_evaluator import TagLevelEvaluator
import pytest


@pytest.mark.skip("")
def test_get_score():
    ex = TagLevelEvaluator()
    ex.process_one_batch(["我是谁", "呢呢"], ["我是", "谁", "呢呢"])
    ex.process_one_batch(["我是谁", "呢呢"], ["我是", "谁", "呢呢"])
    rs = ex.get_score()
    print(rs)


@pytest.mark.skip("")
def test_process_one_batch():
    ex = TagLevelEvaluator()
    rs = TagLevelEvaluator.process_one_batch(ex, 1, 11)
    print(rs)
