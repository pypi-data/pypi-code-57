from typing import Optional

import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras.layers import Dense, TimeDistributed, Activation
from tensorflow.keras.models import Model


class QuestionAnswering:
    
    @staticmethod
    def build_model(bert_dir: str, input_len=384, init_checkpoint: Optional[str] = None):

        # Create the BERT encoder
        # bert_config_path = os.path.join(bert_dir, 'bert_config.json')
        # bert_config = BertConfig.from_json_file(bert_config_path)
        # bert_layer = get_transformer_encoder(bert_config, sequence_length=input_len)

        input_word_ids = tf.keras.layers.Input(shape=(input_len,), dtype=tf.int32, name="input_word_ids")
        input_mask = tf.keras.layers.Input(shape=(input_len,), dtype=tf.int32, name="input_mask")
        segment_ids = tf.keras.layers.Input(shape=(input_len,), dtype=tf.int32, name="input_type_ids")

        bert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/1", trainable=True)
        #
        bert_inputs = [input_word_ids, input_mask, segment_ids]
        # BERT outputs

        #bert_inputs = bert_layer.inputs
        bert_pooled_output, bert_sequence_output = bert_layer(bert_inputs)
        #bert_pooled_output, bert_sequence_output = bert_layer([input_word_ids, input_mask, segment_ids])

        # if init_checkpoint is not None:
        #     checkpoint = tf.train.Checkpoint(model=bert_layer)
        #     checkpoint.restore(init_checkpoint).assert_existing_objects_matched().run_restore_ops()


        # add the additional layer for intent classification and slot filling
        is_impossible = Dense(64, activation='relu')(bert_pooled_output)
        is_impossible = Dense(1, activation='sigmoid', name='is_impossible')(is_impossible)

        ans_start = TimeDistributed(Dense(64, activation='relu'))(bert_sequence_output)
        ans_start = TimeDistributed(Dense(units=1))(ans_start)
        ans_start = tf.squeeze(ans_start, axis=[-1])  # shape = (batch_size, input_len)
        ans_start = Activation(tf.nn.softmax, name='ans_start')(ans_start)

        ans_end = TimeDistributed(Dense(64, activation='relu'))(bert_sequence_output)
        ans_end = TimeDistributed(Dense(units=1))(ans_end)
        ans_end = tf.squeeze(ans_end, axis=[-1])  # shape = (batch_size, input_len)
        ans_end = Activation(tf.nn.softmax, name='ans_end')(ans_end)

        return Model(inputs=bert_inputs, outputs=[is_impossible, ans_start, ans_end])

    @staticmethod
    def compile_model(model):
        optimizer = tf.optimizers.Adam(lr=5e-6)
        losses = {
            'ans_start': tf.losses.CategoricalCrossentropy(),
            'ans_end': tf.losses.CategoricalCrossentropy(),
            'is_impossible': tf.losses.BinaryCrossentropy()
        }
        metrics = {'is_impossible': 'accuracy' }
        model.compile(optimizer=optimizer, loss=losses, metrics=metrics)
