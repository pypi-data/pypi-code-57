"""
:py:class:`Model` is an abstract class representing
a Transformers model.
"""

import logging
import os
from typing import Any, Dict, Optional, Sequence, Type, TypeVar, Union

import torch
from overrides import overrides
from transformers import AutoConfig, AutoModel, PreTrainedModel

from ..data import Vocabulary
from ..nn import utils
from ..training.metrics.metric import Metric
from .model_parameters import ModelParameters

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

# When training a model, many sets of weights are saved. By default we want to
# save/load this set of weights.
_MODEL_WEIGHTS_NAME = "model.th"

T = TypeVar("T", bound="Model")


class Model(torch.nn.Module):  # type: ignore
    """
    This abstract class represents a model to be trained. Rather than relying completely
    on the Pytorch Module, we modify the output spec of ``forward`` to be a dictionary.
    Models built using this API are still compatible with other pytorch models and can
    be used naturally as modules within other models - outputs are dictionaries, which
    can be unpacked and passed into other layers. One caveat to this is that if you
    wish to use an AllenNLP model inside a Container (such as nn.Sequential), you must
    interleave the models with a wrapper module which unpacks the dictionary into
    a list of tensors.
    In order for your model to be trained using the :class:`~allennlp.training.Trainer`
    api, the output dictionary of your Model must include a "loss" key, which will be
    optimised during the training process.
    Finally, you can optionally implement :func:`Model.get_metrics` in order to make use
    of early stopping and best-model serialization based on a validation metric in
    :class:`~vtorch.training.Trainer`. Metrics that begin with "_" will not be logged
    to the progress bar by :class:`~vtorch.training.Trainer`.
    """

    MODEL_NAME = "default"

    def __init__(
        self,
        transformer: PreTrainedModel,
        vocab: Vocabulary,
        model_params: ModelParameters,
        labels_namespace: Any = "labels",
    ) -> None:
        super().__init__()
        self._transformer = transformer
        self._transformer_output_size = (
            self._transformer.config.emb_dim
            if hasattr(self._transformer.config, "emb_dim")
            else self._transformer.config.hidden_size
        )
        self.vocab = vocab
        self._model_params = model_params
        self.labels_namespace = labels_namespace
        self.metrics: Optional[Dict[str, Metric]] = self._model_params.metrics
        if self.metrics is not None:
            for metric in self.metrics.values():
                metric.index_with(self.vocab)

    def forward(self, *args: Any, **kwargs: Any) -> Sequence[torch.Tensor]:  # type: ignore
        """
        Defines the forward pass of the model. In addition, to facilitate easy training,
        this method is designed to compute a loss function defined by a user.
        The input is comprised of everything required to perform a
        training update, `including` labels - you define the signature here!
        It is down to the user to ensure that inference can be performed
        without the presence of these labels. Hence, any inputs not available at
        inference time should only be used inside a conditional block.
        The intended sketch of this method is as follows::
            def forward(self, input1, input2, targets=None):
                ....
                ....
                output1 = self.layer1(input1)
                output2 = self.layer2(input2)
                output_dict = {"output1": output1, "output2": output2}
                if targets is not None:
                    # Function returning a scalar torch.Tensor, defined by the user.
                    loss = self._compute_loss(output1, output2, targets)
                    output_dict["loss"] = loss
                return output_dict
        Parameters
        ----------
        inputs:
            Tensors comprising everything needed to perform a training update, `including` labels,
            which should be optional (i.e have a default value of ``None``).  At inference time,
            simply pass the relevant inputs, not including the labels.
        Returns
        -------
        output_dict: ``Dict[str, torch.Tensor]``
            The outputs from the model. In order to train a model using the
            :class:`~allennlp.training.Trainer` api, you must provide a "loss" key pointing to a
            scalar ``torch.Tensor`` representing the loss to be optimized.
        """
        raise NotImplementedError

    def get_metrics(self, reset: bool = False) -> Dict[str, float]:
        """
        Returns a dictionary of metrics. This method will be called by
        :class:`vtorch.training.Trainer` in order to compute and use model metrics for early
        stopping and model serialization.  We return an empty dictionary here rather than raising
        as it is not required to implement metrics for a new model.  A boolean `reset` parameter is
        passed, as frequently a metric accumulator will have some state which should be reset
        between epochs. This is also compatible with :class:`~vtorch.training.Metric`s. Metrics
        should be populated during the call to ``forward``, with the
        :class:`~vtorch.training.Metric` handling the accumulation of the metric until this
        method is called.
        """
        # pylint: disable=unused-argument,no-self-use
        return {}

    @classmethod
    def load(
        cls: Type[T],
        model_params: ModelParameters,
        serialization_dir: str,
        weights_file: Optional[str] = None,
        cuda_device: int = -1,
        **kwargs: Any,
    ) -> T:
        """
        Instantiates an already-trained model, based on the experiment
        configuration and some optional overrides.
        """
        weights_file = weights_file or os.path.join(serialization_dir, _MODEL_WEIGHTS_NAME)

        vocab = Vocabulary.from_files(os.path.join(serialization_dir, "vocabulary"))

        config = AutoConfig.from_pretrained(serialization_dir)

        model = cls(transformer=AutoModel.from_config(config), vocab=vocab, model_params=model_params,)
        model_state = torch.load(  # type: ignore
            weights_file, map_location=utils.device_mapping(cuda_device)
        )
        model.load_state_dict(model_state, strict=False)
        model.to(cuda_device)

        return model

    @overrides  # type: ignore
    def to(
        self: Type[T],
        device: Optional[Union[int, torch.device]] = ...,
        dtype: Optional[Union[torch.dtype, str]] = ...,
        non_blocking: bool = True,
    ) -> Type[T]:
        if device != -1:
            super().to(device)
            # This is required for the model correctly transferring to any CUDA device except for cuda:0.
            # During backpropagation, some of the modules create a tensor like torch.cuda.LongTensor(), which
            # sets it to cuda:0 by default. This results in CUDA ILLIGAL MEMORY ACCESS later.
            torch.cuda.set_device(torch.device(f"cuda:{device}"))
        else:
            self.cpu()
        return self

    @classmethod
    def from_config(cls: Type[T], config: ModelParameters, vocab: Vocabulary, cuda_device: int = -1) -> T:
        model = cls(
            transformer=AutoModel.from_pretrained(config.transformer_model_name), vocab=vocab, model_params=config,
        )
        model = model.to(cuda_device)

        return model

    def save(self, path: str) -> None:
        self.vocab.save_to_files(os.path.join(path, "vocabulary"))
        self._model_params.save(path, self.MODEL_NAME)
        self._transformer.config.save_pretrained(path)
        with open(os.path.join(path, _MODEL_WEIGHTS_NAME), "wb") as f:
            torch.save(self.state_dict(), f)  # type: ignore
