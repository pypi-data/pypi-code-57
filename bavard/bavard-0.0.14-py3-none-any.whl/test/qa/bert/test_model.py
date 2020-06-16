from bavard.qa.bert.model import QuestionAnswering

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

bert_config_path = os.path.join(dir_path, '../../data/uncased_L-12_H-768_A-12/bert_config.json')


def test_qa_model_build():
    qa = QuestionAnswering(bert_config_path=bert_config_path, input_len=384, context_len=128)
    qa_model = qa.build_model()


