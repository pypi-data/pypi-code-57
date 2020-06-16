from typing import List

import tensorflow as tf


class InputFeatures(object):
    def __init__(self,
                 tokens: List[str],
                 token_to_word_idx: List[int],
                 input_ids,
                 input_mask,
                 segment_ids,
                 ans_start_idx=None,
                 ans_end_idx=None,
                 is_impossible=None):
        self.tokens = tokens
        self.token_to_word_idx = token_to_word_idx
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        self.ans_start_idx = ans_start_idx
        self.ans_end_idx = ans_end_idx
        self.is_impossible = is_impossible

    def to_prediction_input(self):
        return {
            'input_word_ids': tf.convert_to_tensor([self.input_ids]),
            'input_mask': tf.convert_to_tensor([self.input_mask]),
            'input_type_ids': tf.convert_to_tensor([self.segment_ids]),
        }
