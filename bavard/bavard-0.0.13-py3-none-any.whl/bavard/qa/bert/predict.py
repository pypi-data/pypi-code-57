import os
from typing import Optional

import tensorflow as tf
from official.nlp.bert.tokenization import FullTokenizer

from bavard.qa.bert.input_preprocessing import raw_input_to_features
from bavard.qa.bert.raw_input import RawInput


class QAPredictor:
    def __init__(self, bert_dir: str, checkpoint_dir: str):
        self.tokenizer = FullTokenizer(vocab_file=os.path.join(bert_dir, 'vocab.txt'))
        self.qa_model = tf.keras.models.load_model(checkpoint_dir)

    def get_answer(self, context: str, question: str) -> Optional[str]:

        raw_input = RawInput(question=question, context=context, is_training=False)
        input_features = raw_input_to_features(tokenizer=self.tokenizer,
                                               raw_input=raw_input,
                                               max_seq_len=384,
                                               max_question_len=64,
                                               stride=128,
                                               is_training=False)

        best_ans = None
        max_score = float('-inf')
        context_words = context.split()

        for features in input_features:
            prediction_input = features.to_prediction_input()
            out = self.qa_model.predict(prediction_input)

            ans_start = out[1][0][:len(features.tokens)]
            ans_end = out[2][0][:len(features.tokens)]

            ans, score = QAPredictor.decode_prediction(context_words, features, ans_start, ans_end)

            if score > max_score:
                max_score = score
                best_ans = ans

        return best_ans

    @staticmethod
    def decode_prediction(context_words, features, ans_start, ans_end):
        (s, e), score = QAPredictor.get_best_answer_span(ans_start, ans_end)

        if s == 0 or e == 0:
            return None, score

        s, e = s - 1, e - 1
        ws = features.token_to_word_idx[s]
        we = features.token_to_word_idx[e]
        ans = ' '.join(context_words[ws:we + 1])
        return ans, score

    @staticmethod
    def get_best_answer_span(ans_start, ans_end):
        best_score = float('-inf')
        best = (0, 0)
        for s in range(len(ans_start)):
            for e in range(s, len(ans_end)):
                score = ans_start[s] * ans_end[e]
                if score > best_score:
                    best_score = score
                    best = (s, e)
        return best, best_score