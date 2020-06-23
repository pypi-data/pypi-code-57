import torch
from pangeamt_nlp.translation_model.translation_model_base import (
    TranslationModelBase,
)
from onmt.translate import GNMTGlobalScorer
from onmt.translate import Translator, TranslationBuilder
from onmt.bin.train import train as onmt_train
from onmt.bin.train import _get_parser
import onmt.inputters as inputters
from onmt.inputters.text_dataset import TextDataReader
from onmt.utils.parse import ArgumentParser
from onmt.model_builder import build_base_model


class ONMT_model(TranslationModelBase):
    NAME = "onmt"
    INITIALIZED = False

    DEFAULT = (
        "-layers 6 -rnn_size 512 -word_vec_size 512 -transformer_ff 2048 "
        "-heads 8 -encoder_type transformer -decoder_type transformer "
        "-position_encoding -train_steps 500000 -max_generator_batches 2 "
        "-dropout 0.1 -batch_size 4096 -batch_type tokens -normalization "
        "tokens -accum_count 2 -optim adam -adam_beta2 0.998 -decay_method "
        "noam -warmup_steps 8000 -learning_rate 2 -max_grad_norm 0 "
        "-param_init 0 -param_init_glorot -label_smoothing 0.1 -valid_steps "
        "10000 -save_checkpoint_steps 10000 -keep_checkpoint 10 "
        "-early_stopping 8"
    )

    DEFAULT_DECODING = {
        "gpu": -1, "n_best": 1, "min_length": 0, "max_length": 100,
        "ratio": 0.0, "beam_size": 30, "random_sampling_topk": 1,
        "random_sampling_temp": 1, "stepwise_penalty": None,
        "dump_beam": False, "block_ngram_repeat": 0, "replace_unk": True,
        "phrase_table": '', "data_type": 'text', "verbose": False,
        "report_time": False, "copy_attn": False, "out_file": None,
        "report_align": False, "report_score": True, "logger": None,
        "seed": 829
    }

    def __init__(self, path: str, **kwargs) -> None:
        super().__init__()
        if kwargs == {}:
            kwargs = self.DEFAULT_DECODING
        kwargs["ignore_when_blocking"] = frozenset({})
        kwargs["global_scorer"] = GNMTGlobalScorer(0.0, -0.0, "none", "none")
        self._args = kwargs
        self._load(path, **kwargs)

    @staticmethod
    def train(
        data_path: str, model_path: str, *args, gpu: str = None, **kwargs
    ):

        prepend_args = (
            f"-data {data_path}/data -save_model {model_path}/model "
        )
        if gpu:
            apend_args = f"-gpu_ranks {gpu} -log_file {data_path}/log.txt"
        else:
            apend_args = f"-log_file {data_path}/log.txt"

        args = (
            prepend_args + (" ").join(list(args)) + " " + apend_args
        ).split(" ")

        parser = _get_parser()

        opt = parser.parse_args(list(args))
        onmt_train(opt)

    def _load(self, path: str, **kwargs) -> None:
        checkpoint = torch.load(
            path, map_location=lambda storage, loc: storage
        )
        self._model_opts = ArgumentParser.ckpt_model_opts(checkpoint["opt"])
        ArgumentParser.update_model_opts(self._model_opts)
        ArgumentParser.validate_model_opts(self._model_opts)

        # Extract vocabulary
        vocab = checkpoint["vocab"]
        if inputters.old_style_vocab(vocab):
            self._fields = inputters.load_old_vocab(
                vocab, "text", dynamic_dict=False
            )
        else:
            self._fields = vocab

        # Train_steps
        self._train_steps = self._model_opts.train_steps

        # Build openmmt model
        def _use_gpu(**kwargs):
            return kwargs["gpu"] >= 0

        self._opennmt_model = build_base_model(
            self._model_opts,
            self._fields,
            _use_gpu(**kwargs),
            checkpoint,
            kwargs["gpu"],
        )

        self._translator = Translator(
            self._opennmt_model,
            self._fields,
            TextDataReader(),
            TextDataReader(),
            **kwargs
        )

    def translate(self, srcs):
        dataset = inputters.Dataset(
            self._fields,
            readers=([self._translator.src_reader]),
            data=[("src", srcs)],
            dirs=[None],
            sort_key=inputters.str2sortkey[self._translator.data_type],
            filter_pred=self._translator._filter_pred,
        )

        data_iter = inputters.OrderedIterator(
            dataset=dataset,
            device=self._translator._dev,
            batch_size=30,
            train=False,
            sort=False,
            sort_within_batch=False,
            shuffle=False,
        )

        # Translation builder
        translation_builder = TranslationBuilder(
            dataset,
            self._fields,
            self._args["n_best"],  # NBest
            self._args["replace_unk"],  # replace_unk,
            False,  # batch have gold targets
            self._args["phrase_table"],  # Phrase table
        )

        results = []
        for batch in data_iter:
            batch_data = self._translator.translate_batch(
                batch, dataset.src_vocabs, True
            )
            translations = translation_builder.from_batch(batch_data)
            for translation in translations:
                # # Get tokens
                # src_tokens = translation.src_raw
                # tgt_tokens = translation.pred_sents[0]
                #
                # # print(f'src_tokens: {src_tokens}')
                # # print(f'tgt_tokens: {tgt_tokens}')
                # # Create src in tgt from tokens
                # # src = ' '.join(src_tokens)
                # # tgt = ' '.join(tgt_tokens)
                #
                # # Create attention matrix
                # attention_matrix = AttentionMatrix(
                #     src_tokens, tgt_tokens, translation.attns[0].tolist()
                # )
                # # Score
                # score = translation.pred_scores[0].item()
                #
                # # Create a translation object
                # t = Translation(
                #     src_tokens, tgt_tokens, attention_matrix, score
                # )
                # # Append to result
                results.append((' ').join(translation.pred_sents[0]))
        return results
