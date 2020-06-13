# Malaya Natural Language Toolkit
#
# Copyright (C) 2019 Malaya Project
# Licensed under the MIT License
# Author: huseinzol05 <husein.zol05@gmail.com>
# URL: <https://malaya.readthedocs.io/>
# For license information, see https://github.com/huseinzol05/Malaya/blob/master/LICENSE


import tensorflow as tf
from bert import modeling
from malaya.text.bpe import (
    bert_tokenization,
    padding_sequence,
    merge_sentencepiece_tokens,
)
from malaya.transformers.sampling import top_k_logits, top_p_logits
from collections import defaultdict
import numpy as np
import os
from herpetologist import check_type
from typing import List

bert_num_layers = {'bert': 12, 'tiny-bert': 4}


def _extract_attention_weights(num_layers, tf_graph):
    attns = [
        {
            f'layer_{i}': tf_graph.get_tensor_by_name(
                f'bert/encoder/layer_{i}/attention/self/Softmax:0'
            )
        }
        for i in range(num_layers)
    ]

    return attns


def _extract_attention_weights_import(num_layers, tf_graph):
    attns = [
        {
            f'layer_{i}': tf_graph.get_tensor_by_name(
                f'import/bert/encoder/layer_{i}/attention/self/Softmax:0'
            )
        }
        for i in range(num_layers)
    ]

    return attns


class Model:
    def __init__(self, bert_config, tokenizer):
        _graph = tf.Graph()
        with _graph.as_default():
            self.X = tf.placeholder(tf.int32, [None, None])
            self.segment_ids = tf.placeholder(tf.int32, [None, None])
            self.top_p = tf.placeholder(tf.float32, None)
            self.top_k = tf.placeholder(tf.int32, None)
            self.k = tf.placeholder(tf.int32, None)
            self.temperature = tf.placeholder(tf.float32, None)
            self.indices = tf.placeholder(tf.int32, [None, None])
            self.MASK = tf.placeholder(tf.int32, [None, None])
            self._tokenizer = tokenizer

            self.model = modeling.BertModel(
                config = bert_config,
                is_training = False,
                input_ids = self.X,
                input_mask = self.MASK,
                use_one_hot_embeddings = False,
            )
            self.logits = self.model.get_pooled_output()
            output_layer = self.model.get_sequence_output()
            embedding = self.model.get_embedding_table()

            with tf.variable_scope('cls/predictions'):
                with tf.variable_scope('transform'):
                    input_tensor = tf.layers.dense(
                        output_layer,
                        units = bert_config.hidden_size,
                        activation = modeling.get_activation(
                            bert_config.hidden_act
                        ),
                        kernel_initializer = modeling.create_initializer(
                            bert_config.initializer_range
                        ),
                    )
                    input_tensor = modeling.layer_norm(input_tensor)
                output_bias = tf.get_variable(
                    'output_bias',
                    shape = [bert_config.vocab_size],
                    initializer = tf.zeros_initializer(),
                )
                logits = tf.matmul(input_tensor, embedding, transpose_b = True)
                self._logits = tf.nn.bias_add(logits, output_bias)
                self._log_softmax = tf.nn.log_softmax(self._logits)

            logits = tf.gather_nd(self._logits, self.indices)
            logits = logits / self.temperature

            def necleus():
                return top_p_logits(logits, self.top_p)

            def select_k():
                return top_k_logits(logits, self.top_k)

            logits = tf.cond(self.top_p > 0, necleus, select_k)
            self.samples = tf.multinomial(
                logits, num_samples = self.k, output_dtype = tf.int32
            )

            self._sess = tf.InteractiveSession()
            self._sess.run(tf.global_variables_initializer())
            var_lists = tf.get_collection(
                tf.GraphKeys.TRAINABLE_VARIABLES, scope = 'bert'
            )
            cls = tf.get_collection(
                tf.GraphKeys.TRAINABLE_VARIABLES, scope = 'cls'
            )
            self._saver = tf.train.Saver(var_list = var_lists + cls)
            attns = _extract_attention_weights(
                bert_config.num_hidden_layers, tf.get_default_graph()
            )
            self.attns = attns

    def _log_vectorize(self, s_tokens, s_masks):

        """
        Log vectorize ids, suitable for spelling correction or any minimizing log probability.

        Parameters
        ----------
        s_tokens : list of tokenized word after sentencepiece.
        s_masks : list of mask tokens.

        Returns
        -------
        result: np.array
        """

        return self._sess.run(
            self._log_softmax,
            feed_dict = {self.X: s_tokens, self.MASK: s_masks},
        )

    @check_type
    def vectorize(self, strings: List[str]):

        """
        Vectorize string inputs using bert attention.

        Parameters
        ----------
        strings : List[str]

        Returns
        -------
        result: np.array
        """

        batch_x, batch_masks, _, _ = bert_tokenization(self._tokenizer, strings)
        return self._sess.run(
            self.logits, feed_dict = {self.X: batch_x, self.MASK: batch_masks}
        )

    def _attention(self, strings):
        batch_x, batch_masks, _, s_tokens = bert_tokenization(
            self._tokenizer, strings
        )
        maxlen = max([len(s) for s in s_tokens])
        s_tokens = padding_sequence(s_tokens, maxlen, pad_int = '[SEP]')
        attentions = self._sess.run(
            self.attns, feed_dict = {self.X: batch_x, self.MASK: batch_masks}
        )
        return attentions, s_tokens, batch_masks

    @check_type
    def attention(self, strings: List[str], method: str = 'last', **kwargs):
        """
        Get attention string inputs from bert attention.

        Parameters
        ----------
        strings : List[str]
        method : str, optional (default='last')
            Attention layer supported. Allowed values:

            * ``'last'`` - attention from last layer.
            * ``'first'`` - attention from first layer.
            * ``'mean'`` - average attentions from all layers.

        Returns
        -------
        result : List[List[Tuple[str, float]]]
        """

        method = method.lower()
        if method not in ['last', 'first', 'mean']:
            raise Exception(
                "method not supported, only support 'last', 'first' and 'mean'"
            )
        attentions, s_tokens, _ = self._attention(strings)

        if method == 'first':
            cls_attn = list(attentions[0].values())[0][:, :, 0, :]

        if method == 'last':
            cls_attn = list(attentions[-1].values())[0][:, :, 0, :]

        if method == 'mean':
            combined_attentions = []
            for a in attentions:
                combined_attentions.append(list(a.values())[0])
            cls_attn = np.mean(combined_attentions, axis = 0).mean(axis = 2)

        cls_attn = np.mean(cls_attn, axis = 1)
        total_weights = np.sum(cls_attn, axis = -1, keepdims = True)
        attn = cls_attn / total_weights
        output = []
        for i in range(attn.shape[0]):
            output.append(
                merge_sentencepiece_tokens(list(zip(s_tokens[i], attn[i])))
            )
        return output

    @check_type
    def visualize_attention(self, string: str):

        """
        Visualize attention.

        Parameters
        ----------
        string : str
        """

        from malaya.function.html import _attention

        strings = [string]
        attentions, s_tokens, _ = self._attention(strings)
        attn_dict = defaultdict(list)
        for layer, attn_data in enumerate(attentions):
            attn = list(attn_data.values())[0][0]
            attn_dict['all'].append(attn.tolist())

        results = {
            'all': {
                'attn': attn_dict['all'],
                'left_text': s_tokens[0],
                'right_text': s_tokens[0],
            }
        }
        _attention(results)


@check_type
def load(model: str = 'base', **kwargs):
    """
    Load bert model.

    Parameters
    ----------
    model : str, optional (default='base')
        Model architecture supported. Allowed values:

        * ``'bert'`` - base bert-bahasa released by Malaya.
        * ``'tiny-bert'`` - tiny bert-bahasa released by Malaya.

    Returns
    -------
    result : malaya.transformers.bert.Model class
    """

    from malaya.path import PATH_BERT, S3_PATH_BERT
    from malaya.function import check_file

    model = model.lower()
    check_file(PATH_BERT[model]['model'], S3_PATH_BERT[model], **kwargs)

    if not os.path.exists(PATH_BERT[model]['directory'] + 'model.ckpt'):
        import tarfile

        with tarfile.open(PATH_BERT[model]['model']['model']) as tar:
            tar.extractall(path = PATH_BERT[model]['path'])

    import sentencepiece as spm
    from malaya.text.bpe import SentencePieceTokenizer

    bert_checkpoint = PATH_BERT[model]['directory'] + 'model.ckpt'
    vocab_model = PATH_BERT[model]['directory'] + 'sp10m.cased.bert.model'
    vocab = PATH_BERT[model]['directory'] + 'sp10m.cased.bert.vocab'
    bert_config = PATH_BERT[model]['directory'] + 'config.json'

    sp_model = spm.SentencePieceProcessor()
    sp_model.Load(vocab_model)

    with open(vocab) as fopen:
        v = fopen.read().split('\n')[:-1]
    v = [i.split('\t') for i in v]
    v = {i[0]: no for no, i in enumerate(v)}
    tokenizer = SentencePieceTokenizer(v, sp_model)

    bert_config = modeling.BertConfig.from_json_file(bert_config)
    model = Model(bert_config, tokenizer)
    model._saver.restore(model._sess, bert_checkpoint)
    return model
