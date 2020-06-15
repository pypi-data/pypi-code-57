from datetime import datetime
from typing import List

import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from official.nlp.bert.tokenization import FullSentencePieceTokenizer
from sklearn.preprocessing import LabelEncoder
from tensorflow.python.keras.layers import Input, Dense, TimeDistributed, Dropout, Lambda
from tensorflow.python.keras.models import Model

from bavard.chatbots.albert_intents_and_tags_model.data_preprocessing.data_preprocessor import decode_tf_record
from bavard.chatbots.albert_intents_and_tags_model.data_preprocessing.prediction_input import PredictionInput


class AlbertIntentsAndTagsModel:
    def __init__(self, max_seq_len, n_tags, n_intents, saved_model_dir: str, load_model=False):
        self.max_seq_len = max_seq_len
        self.n_tags = n_tags
        self.n_intents = n_intents
        self.save_model_dir = saved_model_dir
        self.model = None

        if load_model:
            #self.model = tf.saved_model.load(saved_model_dir)
            self.model = tf.keras.models.load_model(saved_model_dir)
        else:
            self._build_model()
        self._compile_model()

    def _build_model(self):
        albert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/albert_en_base/1",
                                      trainable=True)

        in_id = Input(shape=(self.max_seq_len,), name='input_ids', dtype=tf.int32)
        in_mask = Input(shape=(self.max_seq_len,), name='input_mask', dtype=tf.int32)
        in_segment = Input(shape=(self.max_seq_len,), name='segment_ids', dtype=tf.int32)
        word_start_mask = Input(shape=(self.max_seq_len,), name='word_start_mask', dtype=tf.float32)
        bert_inputs = [in_id, in_mask, in_segment]
        all_inputs = [in_id, in_mask, in_segment, word_start_mask]

        # the output of trained Bert
        pooled_output, sequence_output, = albert_layer(bert_inputs)

        # add the additional layer for intent classification and slot filling
        intents_drop = Dropout(rate=0.1)(pooled_output)
        intents_out = Dense(self.n_intents, activation='softmax', name='intent')(intents_drop)

        tags_drop = Dropout(rate=0.1)(sequence_output)
        tags_out = TimeDistributed(Dense(self.n_tags, activation='softmax'))(tags_drop)
        tags_out = Lambda(lambda x: x, name='tags')(tags_out)
        # tags_out = Multiply(name='tagger')([tags_out, word_start_mask])

        self.model = Model(inputs=all_inputs, outputs=[tags_out, intents_out])

    def _compile_model(self):
        optimizer = tf.keras.optimizers.Adam(lr=5e-5)
        losses = {
            'tags': 'sparse_categorical_crossentropy',
            'intent': 'categorical_crossentropy'
        }
        loss_weights = {'tags': 3.0, 'intent': 1.0}
        metrics = {'intent': 'acc'}
        self.model.compile(optimizer=optimizer, loss=losses, loss_weights=loss_weights, metrics=metrics)
        self.model.summary()

    def get_tags_output_mask(self, word_start_mask):
        word_start_mask = np.expand_dims(word_start_mask, axis=2)  # n x seq_len x 1
        tags_output_mask = np.tile(word_start_mask, (1, 1, self.n_tags))  # n x seq_len x n_tags
        return tags_output_mask

    def train(self, training_path: str, batch_size: int, steps_per_epoch: int, epochs: int):
        train_dataset = tf.data.TFRecordDataset([training_path])

        def split_x_y(item):
            x = {
                'input_ids': item['input_ids'],
                'input_mask': item['input_mask'],
                'segment_ids': item['segment_ids'],
                'word_start_mask': item['word_start_mask'],
            }
            y = {
                'tags': item['tags'],
                'intent': item['intent'],
            }
            return x, y

        ds = train_dataset \
            .shuffle(buffer_size=1000) \
            .map(map_func=lambda x: decode_tf_record(x, self.max_seq_len, n_intents=self.n_intents, is_training=True)) \
            .map(split_x_y).batch(batch_size=batch_size).repeat()

        test_ds = ds.take(200)
        train_ds = ds.skip(200)

        # checkpoints

        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=self.save_model_dir,
                                                         save_best_only=True,
                                                         save_weights_only=False,
                                                         verbose=1)

        # tensorboard

        logdir = "logs/" + datetime.now().strftime("%Y%m%d-%H%M%S")
        tb_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)

        # train

        self.model.fit(train_ds,
                       epochs=epochs,
                       steps_per_epoch=steps_per_epoch,
                       validation_data=test_ds,
                       callbacks=[cp_callback, tb_callback],
                       use_multiprocessing=True)

    def predict(self, text: str, intents: List[str], tag_types: List[str], tokenizer: FullSentencePieceTokenizer):
        pred_input = PredictionInput(text=text,
                                    intents=intents,
                                    tag_types=tag_types,
                                    max_seq_len=self.max_seq_len,
                                    tokenizer=tokenizer)
        model_input = pred_input.to_model_input()
        [tags_raw, intent_raw] = self.model.predict(x=model_input)
        tags_raw = np.squeeze(tags_raw)
        intent_raw = np.squeeze(intent_raw)

        intent = pred_input.decode_intent(intent_raw)
        tags = pred_input.decode_tags(tags_raw)
        return {
            'intent': intent,
            'tags': tags,
        }
