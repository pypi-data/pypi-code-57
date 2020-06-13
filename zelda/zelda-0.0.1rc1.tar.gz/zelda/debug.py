# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: itachi971009@gmail.com

@version: 1.0
@file: debug.py
@time: 2019/12/21 11:22

这一行开始写关于本文件的说明与解释


"""
import tensorflow as tf
from zelda.models.text_classifier.aver_pooling_text_classifier_model import AverPoolingTextClassifierModel
from zelda.data.dataset_readers.text_classifier_dataset_reader import TextClassifierDatasetReader
from zelda.data.token_indexers.single_id_token_indexer import SingleIdTokenIndexer
from zelda.data.tokenizers.character_tokenizer import CharacterTokenizer
from zelda.data.vocabulary import Vocabulary
from zelda.data.iterators.bucket_iterator import BucketIterator
from zelda.training.trainer import Trainer

text_dataset_reader = TextClassifierDatasetReader(token_indexers={"tokens": SingleIdTokenIndexer()},
                                                  tokenizer=CharacterTokenizer(),
                                                  max_sequence_length=32)
instances = text_dataset_reader.read(
    file_path="../dataset/AGNews/ag_news_training.jsonl")
print(instances[:10])
vocab = Vocabulary.from_instances(instances)

iterator = BucketIterator(batch_size=32)
model = AverPoolingTextClassifierModel()
# model.build_graph(input_shape=(None, None))
# model.summary()
iterator.index_with(vocab=vocab)
trainer = Trainer(model=model,
                  optimizer=tf.optimizers.Adam(),
                  iterator=iterator,
                  num_epochs=50,
                  train_dataset=instances,
                  cuda_device=0,
                  loss_object=tf.keras.losses.SparseCategoricalCrossentropy(),
                  accuracy_object=tf.keras.metrics.SparseCategoricalAccuracy)

if __name__ == '__main__':
    trainer.train()
