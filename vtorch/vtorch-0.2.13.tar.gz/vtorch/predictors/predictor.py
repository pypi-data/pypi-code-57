from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

import torch

from ..nn import utils as nn_util
from .predictions_postprocessing.default import PredictionPostprocessor

if TYPE_CHECKING:
    from ..data import Instance
    from ..data.dataset_readers import DatasetReader
    from ..data.iterators import DataIterator
    from ..models import Model


class Predictor:
    """
    a ``Predictor`` is a thin wrapper around an AllenNLP model that handles JSON -> JSON predictions
    that can be used for serving models through the web API or making predictions in bulk.
    """

    def __init__(
        self,
        model: "Model",
        dataset_reader: "DatasetReader",
        iterator: "DataIterator",
        language_post_processors: Dict[str, PredictionPostprocessor],
        resort_predictions: bool = True,
        cuda_device: int = -1,
        torchscript: bool = False,
    ) -> None:
        self._model = model
        self._model.eval()
        self._dataset_reader = dataset_reader
        self._iterator = iterator
        self._iterator.index_with(self._model.vocab)
        self._resort_predictions = resort_predictions
        self._cuda_device = cuda_device
        self._torchscript = torchscript
        self._torchscript_inference: Optional[Callable[[torch.Tensor, torch.Tensor], torch.Tensor]] = None
        self._language_post_processors = language_post_processors
        for postprocessor in self._language_post_processors.values():
            postprocessor.index_with(self._model.vocab, self._model.labels_namespace)

    def _json_to_instance(self, json_dict: Dict[str, Any]) -> "Instance":
        """
        Converts a JSON object into an :class:`~vtorch.data.instance.Instance`
        and a ``JsonDict`` of information which the ``Predictor`` should pass through,
        such as tokenised inputs.
        """
        raise NotImplementedError

    def predict_batch_json(self, inputs: List[Dict[str, Any]]) -> torch.Tensor:
        instances = self._batch_json_to_instances(inputs)
        return self.predict_batch_instance(instances)

    def predict_batch_instance(
        self, instances: List["Instance"], additional_batch_params: Optional[Dict[str, Any]] = None
    ) -> torch.Tensor:
        data_iterator = self._iterator(instances, num_epochs=1, shuffle=False)
        not_sorted_predictions = []
        serial_indexes: List[int] = []
        with torch.no_grad():
            for batch in data_iterator:
                serial_indexes.extend(batch["serial_index"])
                batch = nn_util.move_to_device(batch, self._cuda_device)
                if additional_batch_params is not None:
                    batch.update(additional_batch_params)
                not_sorted_predictions.append(self._make_predictions(batch).cpu())
        not_sorted_predictions = torch.cat(not_sorted_predictions)
        sorted_predictions = torch.zeros_like(not_sorted_predictions)
        sorted_predictions[torch.tensor(serial_indexes, dtype=torch.long)] = not_sorted_predictions

        return sorted_predictions

    def _make_predictions(self, batch: Dict[str, torch.Tensor]) -> torch.Tensor:
        if not self._torchscript:
            return self._model(**batch)
        if self._torchscript_inference is None:
            self._torchscript_inference = torch.jit.trace(  # type: ignore
                self._model, (batch["text"], batch["sequence_length"]),
            )
        batch_predictions = self._torchscript_inference(batch["text"], batch["sequence_length"])[0]
        return batch_predictions

    def _batch_json_to_instances(self, json_dicts: List[Dict[str, Any]]) -> List["Instance"]:
        """
        Converts a list of JSON objects into a list of :class:`~vtorch.data.instance.Instance`s.
        By default, this expects that a "batch" consists of a list of JSON blobs which would
        individually be predicted by :func:`predict_json`. In order to use this method for
        batch prediction, :func:`_json_to_instance` should be implemented by the subclass, or
        if the instances have some dependency on each other, this method should be overridden
        directly.
        """
        instances = []
        for json_dict in json_dicts:
            instances.append(self._json_to_instance(json_dict))
        return instances

    def predict(self, inputs: List[Dict[str, Any]]) -> Any:
        raise NotImplementedError()

    @property
    def labels(self) -> Any:
        raise NotImplementedError()

    def _post_process_predictions_by_language(
        self, raw_predictions: torch.Tensor, languages: List[str]
    ) -> List[List[str]]:
        predictions = torch.zeros_like(raw_predictions)
        for post_processor_language, post_processor in self._language_post_processors.items():
            serial_indices = [
                serial_index for serial_index, language in enumerate(languages) if language == post_processor_language
            ]
            if len(serial_indices) == 0:
                continue
            predictions[serial_indices] = post_processor.postprocess(raw_predictions[serial_indices])

        labels_predictions: List[List[str]] = [[] for _ in predictions]
        for mention_serial_number, label_index in predictions.nonzero().tolist():  # type: ignore
            labels_predictions[mention_serial_number].append(self.labels[label_index])
        return labels_predictions


def _unsqueeze_dict(dictionary_item: Dict[Any, Any]) -> List[Dict[Any, Any]]:
    to_right_d_values = [_unsqueeze_dict(v) if isinstance(v, dict) else v for v in dictionary_item.values()]
    return [dict(zip(dictionary_item, v)) for v in zip(*to_right_d_values)]
