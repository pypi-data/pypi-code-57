from tokenizer_tools.evaluator.token.base_evaluator import BaseEvaluator

def test_get_score():
    baseEvaluator = BaseEvaluator()
    baseEvaluator.wc_of_test = 0.1
    baseEvaluator.wc_of_gold = 0.2
    baseEvaluator.wc_of_correct = 0.3
    rs = baseEvaluator.get_score()
    print(rs)
    assert len(rs) == 3


