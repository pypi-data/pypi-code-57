from tokenizer_tools.evaluator.offset_evaluator import OffsetEvaluator

def test_process_one_batch():
    evaluator = OffsetEvaluator()
    evaluator.process_one_batch(
        ['我是谁', '呢呢'],
        ['我是', '谁', '呢呢']
    )
    evaluator.process_one_batch(
        ['我是谁', '呢呢'],
        ['我是', '谁', '呢呢']
    )
    print(evaluator)
    score = evaluator.get_score()
    print(score)
    assert len(score) == 3
