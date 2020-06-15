from typing import List

import tensorflow as tf
from sklearn.preprocessing import LabelEncoder

from bavard.chatbots.albert_intents_and_tags_model.data_preprocessing.training_example import Example


class PreprocessedTrainingData:
    def __init__(self, intents: List[str], tag_types: List[str], examples: List[Example]):
        self.intents = intents
        self.tag_types = tag_types
        self.examples = examples

        tag_set = {'[CLS]', '[SEP]', 'O'}
        for tag_type in self.tag_types:
            tag_set.add(f'B-{tag_type}')
            tag_set.add(f'I-{tag_type}')

        self.tag_encoder = LabelEncoder()
        self.tag_encoder.fit(list(tag_set))
        self.intents_encoder = LabelEncoder()
        self.intents_encoder.fit(self.intents)

    def write_tfrecord(self, filename: str, max_seq_len: int):
        writer = tf.io.TFRecordWriter(filename)

        for ex in self.examples:
            tf_example = ex.convert_to_tfexample(max_seq_len, self.tag_encoder, self.intents_encoder)
            writer.write(tf_example.SerializeToString())

        writer.close()
