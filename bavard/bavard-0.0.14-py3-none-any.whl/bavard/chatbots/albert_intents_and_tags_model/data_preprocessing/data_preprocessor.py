import json
from typing import List, Dict

import tensorflow as tf
import tensorflow_hub as hub
from official.nlp.bert import tokenization
from official.nlp.bert.tokenization import FullSentencePieceTokenizer

from bavard.text import utils
from bavard.chatbots.albert_intents_and_tags_model.data_preprocessing.preprocessed_training_data import PreprocessedTrainingData
from bavard.chatbots.albert_intents_and_tags_model.data_preprocessing.training_example import Example, Tag


class DataPreprocessor:
    @staticmethod
    def preprocess_text(text: str, tokenizer: FullSentencePieceTokenizer):
        text_words = text.split()
        text_tokens = []
        token_to_word_idx = []
        word_to_token_map = []
        word_start_mask = []
        for (wi, word) in enumerate(text_words):
            word_to_token_map.append(len(text_tokens))
            word_tokens = tokenizer.tokenize(word)
            for ti, token in enumerate(word_tokens):
                token_to_word_idx.append(wi)
                text_tokens.append(token)

                if ti == 0:
                    word_start_mask.append(1)
                else:
                    word_start_mask.append(0)

        return text_tokens, word_start_mask, word_to_token_map

    @staticmethod
    def preprocess(json_data: any, tokenizer: FullSentencePieceTokenizer) -> PreprocessedTrainingData:
        result_examples: List[Example] = []

        tag_types = json_data['tagTypes']
        intents = json_data['intents']
        examples = json_data['examples']

        for ex in examples:
            text = ex['text']
            intent = ex['intent']
            raw_tags = ex['tags']

            text_tokens, word_start_mask, word_to_token_map = DataPreprocessor.preprocess_text(text, tokenizer)

            char_to_word_map = utils.get_char_to_word_map(text)

            result_tags: List[Tag] = []
            for tag in raw_tags:
                start = tag['start']
                end = tag['end']
                tag_type = tag['tagType']

                start_word_idx = char_to_word_map[start]
                end_word_idx = char_to_word_map[end - 1]

                start_tok = word_to_token_map[start_word_idx]
                end_tok = word_to_token_map[end_word_idx]
                result_tags.append(Tag(tag_type=tag_type,
                                       start=start,
                                       end=end,
                                       start_tok=start_tok,
                                       end_tok=end_tok))

            result_examples.append(Example(
                text=text,
                intent=intent,
                tokens=text_tokens,
                tags=result_tags,
                word_start_mask=word_start_mask,
                tokenizer=tokenizer,
            ))
        return PreprocessedTrainingData(intents=intents, tag_types=tag_types, examples=result_examples)


def decode_tf_record(record, input_len: int, n_intents: int, is_training: bool) -> Dict[str, any]:
    read_features = {
        "input_ids": tf.io.FixedLenFeature([input_len], tf.int64),
        "input_mask": tf.io.FixedLenFeature([input_len], tf.int64),
        "segment_ids": tf.io.FixedLenFeature([input_len], tf.int64),
        "word_start_mask": tf.io.FixedLenFeature([input_len], tf.int64),
    }

    if is_training:
        read_features["intent"] = tf.io.FixedLenFeature([], tf.int64)
        read_features["tags"] = tf.io.FixedLenFeature([input_len], tf.int64)

    example = tf.io.parse_single_example(record, read_features)

    # tf.Example only supports tf.int64, but the TPU only supports tf.int32.
    # So cast all int64 to int32.
    for name in example.keys():
        t = example[name]
        if t.dtype == tf.int64:
            t = tf.cast(t, tf.int32)
        example[name] = t

    if is_training:
        intent = example["intent"]
        example["intent"] = tf.one_hot(intent, n_intents)

    return example


def agent_data_to_tfrecord(json_path: str, output_path: str):
    albert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/albert_en_base/1", trainable=False)
    sp_model_file = albert_layer.resolved_object.sp_model_file.asset_path.numpy()
    tokenizer = tokenization.FullSentencePieceTokenizer(sp_model_file)

    print("Processing JSON Data.")

    with open(json_path) as f:
        data = json.load(f)
        processed_data = DataPreprocessor.preprocess(json_data=data, tokenizer=tokenizer)

    print(f'Writing TF records to {output_path}')
    processed_data.write_tfrecord(filename=output_path, max_seq_len=200)
