import collections
from typing import List

import numpy as np
import tensorflow as tf
from official.nlp.bert.tokenization import FullSentencePieceTokenizer
from sklearn.preprocessing import LabelEncoder


class Tag:
    def __init__(self, tag_type: str, start: int, end: int, start_tok: int, end_tok: int):
        self.tag_type = tag_type
        self.start = start
        self.end = end
        self.start_tok = start_tok
        self.end_tok = end_tok


class Example:
    def __init__(self,
                 text: str,
                 intent: str,
                 tokens: List[str],
                 tags: List[Tag],
                 word_start_mask: List[int],
                 tokenizer: FullSentencePieceTokenizer):
        self.text = text
        self.intent = intent
        self.tokens = tokens
        self.tags = tags
        self.word_start_mask = word_start_mask
        self.token_tags: List[str] = ['O'] * len(tokens)

        for tag in self.tags:
            for i in range(tag.start_tok, tag.end_tok + 1):
                if i == tag.start_tok:
                    self.token_tags[i] = f'B-{tag.tag_type}'
                else:
                    self.token_tags[i] = f'I-{tag.tag_type}'

        self.tokens = ['[CLS]', *self.tokens, '[SEP]']
        self.token_tags = ['[CLS]', *self.token_tags, '[SEP]']
        self.word_start_mask = [0, *self.word_start_mask, 0]

        self.segment_ids = [0] * len(self.tokens)
        self.input_ids = tokenizer.convert_tokens_to_ids(self.tokens)
        self.input_mask = [1] * len(self.tokens)

    def convert_to_tfexample(self,
                             max_seq_len: int,
                             tag_encoder: LabelEncoder,
                             intent_encoder: LabelEncoder) -> tf.train.Example:
        input_ids = self.input_ids.copy()
        input_mask = self.input_mask.copy()
        segment_ids = self.segment_ids.copy()
        word_start_mask = self.word_start_mask.copy()
        token_tags = self.token_tags.copy()
        intent = intent_encoder.transform([self.intent])[0]

        assert len(input_ids) == len(input_mask) == len(segment_ids) == len(token_tags) == len(word_start_mask)

        while len(input_ids) < max_seq_len:
            input_ids.append(0)
            input_mask.append(0)
            segment_ids.append(0)
            word_start_mask.append(0)
            token_tags.append('O')

        token_tags = tag_encoder.transform(token_tags).astype(np.int32)

        def create_int_feature(values):
            feature = tf.train.Feature(
                int64_list=tf.train.Int64List(value=list(values)))
            return feature

        features = collections.OrderedDict()

        # X
        features["input_ids"] = create_int_feature(input_ids)
        features["input_mask"] = create_int_feature(input_mask)
        features["segment_ids"] = create_int_feature(segment_ids)
        features["word_start_mask"] = create_int_feature(word_start_mask)

        # Y
        features["tags"] = create_int_feature(token_tags)
        features["intent"] = create_int_feature([intent])

        tf_example = tf.train.Example(features=tf.train.Features(feature=features))
        return tf_example
