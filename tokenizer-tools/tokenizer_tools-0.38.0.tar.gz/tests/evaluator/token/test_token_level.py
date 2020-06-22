from tokenizer_tools.evaluator.token.token_level import TokenEvaluator

def test_generate_word_offset_list():
    tokenEvaluator = TokenEvaluator()
    rs = tokenEvaluator.generate_word_offset_list(['panda', 'horse', 'bird'])
    print(rs)
    assert [(0, 5), (5, 10), (10, 14)] == rs

def test_process_one_batch():
    tokenEvaluator = TokenEvaluator()
    rs = tokenEvaluator.process_one_batch(['forest', 'river'], ['farmer', 'risher'])
    print(rs)
    assert None == rs

def test_tokenEvaluator():
    evaluator = TokenEvaluator()
    evaluator.process_one_batch(
        ['我是谁', '呢呢'],
        ['我是', '谁', '呢呢']
    )
    evaluator.process_one_batch(
        ['我是谁', '呢呢'],
        ['我是', '谁', '呢呢']
    )

    score = evaluator.get_score()
    print(score)
