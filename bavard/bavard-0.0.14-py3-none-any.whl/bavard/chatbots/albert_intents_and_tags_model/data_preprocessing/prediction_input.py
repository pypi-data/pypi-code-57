from typing import List
import tensorflow as tf
from official.nlp.bert.tokenization import FullSentencePieceTokenizer
from sklearn.preprocessing import LabelEncoder
import numpy as np
from bavard.chatbots.albert_intents_and_tags_model.data_preprocessing.data_preprocessor import DataPreprocessor


class PredictionInput:
    def __init__(self,
                 text: str,
                 intents: List[str],
                 tag_types: List[str],
                 max_seq_len: int,
                 tokenizer: FullSentencePieceTokenizer):
        self.text = text
        self.intents = sorted(intents)
        self.tag_types = sorted(tag_types)

        tag_set = {'[CLS]', '[SEP]', 'O'}
        for tag_type in self.tag_types:
            tag_set.add(f'B-{tag_type}')
            tag_set.add(f'I-{tag_type}')

        self.tag_encoder = LabelEncoder()
        self.tag_encoder.fit(list(tag_set))
        self.intents_encoder = LabelEncoder()
        self.intents_encoder.fit(self.intents)

        tokens, word_start_mask, word_to_token_map = DataPreprocessor.preprocess_text(self.text, tokenizer)

        self.tokens = ['[CLS]', *tokens, '[SEP]']
        self.input_ids = tokenizer.convert_tokens_to_ids(self.tokens)
        self.input_mask = [1] * len(self.tokens)
        self.segment_ids = [0] * len(self.input_ids)
        self.word_start_mask = [0, *word_start_mask, 0]

        while len(self.input_ids) < max_seq_len:
            self.input_ids.append(0)
            self.input_mask.append(0)
            self.segment_ids.append(0)
            self.word_start_mask.append(0)

    def to_model_input(self):
        return {
            'input_ids': tf.convert_to_tensor([self.input_ids]),
            'input_mask': tf.convert_to_tensor([self.input_mask]),
            'segment_ids': tf.convert_to_tensor([self.segment_ids]),
            'word_start_mask': tf.convert_to_tensor([self.word_start_mask]),
        }

    def decode_intent(self, intent: np.ndarray):
        intent_max = np.argmax(intent)
        decoded_intent = self.intents_encoder.inverse_transform([intent_max])[0]
        return decoded_intent

    def decode_tags(self, tags: np.ndarray):
        assert tags.shape[0] == len(self.word_start_mask)
        decoded_tags = []
        for i, e in enumerate(self.word_start_mask):
            if e == 1:
                predicted_tag_idx = np.argmax(tags[i])
                predicted_tag = self.tag_encoder.inverse_transform([predicted_tag_idx])[0]
                decoded_tags.append(predicted_tag)

        words = self.text.split()

        result = []
        current_tag_words = []
        current_tag_type = None
        for i, tag in enumerate(decoded_tags):
            if tag == 'O':
                if current_tag_words and current_tag_type:
                    result.append({
                        'tagType': current_tag_type,
                        'value': ' '.join(current_tag_words),
                    })

                current_tag_type = None
                current_tag_words = []
                continue

            if tag.startswith('B-'):
                if current_tag_words and current_tag_type:
                    result.append({
                        'tagType': current_tag_type,
                        'value': ' '.join(current_tag_words),
                    })

                current_tag_words = [words[i]]
                current_tag_type = tag[2:]
            elif tag.startswith('I-'):
                current_tag_words.append(words[i])

        if current_tag_words and current_tag_type:
            result.append({
                'tagType': current_tag_type,
                'value': ' '.join(current_tag_words),
            })

        return result
