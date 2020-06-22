from tokenizer_tools.evaluator.token.tag_level import TagEvaluator

def test_tagEvaluator():
    tagEvaluator = TagEvaluator()
    tag_evaluator = TagEvaluator()
    tag_evaluator.process_one_batch(
        'BMEBE',
        'BESBE'
    )
    tag_evaluator.process_one_batch(
        'BMEBE',
        'BESBE'
    )
    score = tag_evaluator.get_score()
    print(score)

