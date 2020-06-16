import os
from datetime import datetime

import tensorflow as tf

from bavard.qa.bert.decode_tf_record import decode_tf_record
from bavard.qa.bert.model import QuestionAnswering

tf.random.set_seed(0)


class BertSquadTrainer:
    def __init__(self,
                 squad_train: str,
                 bert_dir: str,
                 saved_model_dir: str):

        if os.path.exists(saved_model_dir):
            print('Loading saved model')
            self.model = tf.keras.models.load_model(saved_model_dir)
        else:
            self.model = QuestionAnswering.build_model(bert_dir=bert_dir,
                                                       init_checkpoint=os.path.join(bert_dir, 'bert_model.ckpt'))

        QuestionAnswering.compile_model(self.model)
        self.save_model_dir = saved_model_dir
        self.train_dataset = tf.data.TFRecordDataset([squad_train])

    def train(self, batch_size: int, steps_per_epoch: int, epochs: int):
        def split_x_y(item):
            x = {
                'input_word_ids': item['input_word_ids'],
                'input_mask': item['input_mask'],
                'input_type_ids': item['input_type_ids'],
            }
            y = {
                'is_impossible': item['is_impossible'],
                'ans_start': item['ans_start'],
                'ans_end': item['ans_end']
            }
            return x, y

        ds = self.train_dataset \
            .shuffle(buffer_size=1000) \
            .map(map_func=lambda x: decode_tf_record(x, 384, is_training=True)) \
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
