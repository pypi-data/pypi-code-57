from typing import Generator

import tensorflow_datasets as tfds
from official.nlp.bert.tokenization import FullTokenizer

from bavard.text_summarization.extractive.bert.input_features import InputFeatures
from bavard.text_summarization.extractive.bert.input_preprocessing import raw_input_to_features


class ExtractiveDataLoader:
    @staticmethod
    def load_training_set(tokenizer: FullTokenizer) -> Generator[InputFeatures, None, None]:
        ds, info = tfds.load('cnn_dailymail', split="train", with_info=True, shuffle_files=False)

        ds = tfds.as_numpy(ds)

        for example in ds:
            article = example['article'].decode('utf-8')
            highlights = example['highlights'].decode('utf-8')

            features = raw_input_to_features(tokenizer=tokenizer,
                                             article=article,
                                             summary=highlights,
                                             max_seq_len=512,
                                             max_sentences=20,
                                             is_training=True)
            for feature in features:
                yield feature
