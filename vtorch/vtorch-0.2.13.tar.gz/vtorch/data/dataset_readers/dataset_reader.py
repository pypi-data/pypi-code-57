import json
import logging
import os
import re
from typing import Any, Callable, Dict, Iterable, Iterator, Optional

import jsonpickle
from transformers import AutoTokenizer, PreTrainedTokenizer

from ...common import Tqdm
from ...common.checks import ConfigurationError
from ..instance import Instance

logger = logging.getLogger(__name__)
DATASET_READER_PARAMETERS_FILE_NAME = "parameters.json"
DATASET_READER_FOLDER = "dataset_reader"
TOKENIZER_NAME_FIELD = "transformer_tokenizer_name"
TOKENIZER_CONFIG_NAME = "config.json"
TOKENIZER_FOLDER = "tokenizer"


class _LazyInstances(Iterable[Instance]):
    """
    An ``Iterable`` that just wraps a thunk for generating instances and calls it for
    each call to ``__iter__``.
    """

    def __init__(
        self,
        instance_generator: Callable[[], Iterable[Instance]],
        cache_file: Optional[str] = None,
        deserialize: Optional[Callable[[str], Instance]] = None,
        serialize: Optional[Callable[[Instance], str]] = None,
    ) -> None:
        super().__init__()

        if cache_file is not None and os.path.exists(cache_file):
            if deserialize is None:
                raise ConfigurationError("You need to specify deserialize when cache_file is not None")
        elif cache_file is not None:
            if serialize is None:
                raise ConfigurationError("You need to specify serialize when cache_file is not None")

        self.instance_generator = instance_generator
        self.cache_file = cache_file
        self.deserialize = deserialize
        self.serialize = serialize

    def __iter__(self) -> Iterator[Instance]:
        # Case 1: Use cached instances
        if self.cache_file is not None and os.path.exists(self.cache_file):
            with open(self.cache_file) as data_file:
                for line in data_file:
                    if self.deserialize is not None:
                        yield self.deserialize(line)
        # Case 2: Need to cache instances
        elif self.cache_file is not None:
            with open(self.cache_file, "w") as data_file:
                for instance in self.instance_generator():
                    if self.serialize is not None:
                        data_file.write(self.serialize(instance))
                        data_file.write("\n")
                        yield instance
        # Case 3: No cache
        else:
            instances = self.instance_generator()
            if isinstance(instances, list):
                raise ConfigurationError("For a lazy dataset reader, _read() must return a generator")
            yield from instances


class DatasetReader:
    DATASET_READER_NAME = "default"
    TYPE_PARAMETER = "type"
    """
    A ``DatasetReader`` knows how to turn a file containing a dataset into a collection
    of ``Instance`` s.  To implement your own, just override the `_read(file_path)` method
    to return an ``Iterable`` of the instances. This could be a list containing the instances
    or a lazy generator that returns them one at a time.
    All parameters necessary to _read the data apart from the filepath should be passed
    to the constructor of the ``DatasetReader``.
    Parameters
    ----------
    lazy : ``bool``, optional (default=False)
        If this is true, ``instances()`` will return an object whose ``__iter__`` method
        reloads the dataset each time it's called. Otherwise, ``instances()`` returns a list.
    """

    def __init__(
        self,
        transformer_tokenizer_name: str,
        max_padding_length: Optional[int] = None,
        to_lower: bool = True,
        use_fast: bool = False,
        lazy: bool = False,
    ) -> None:
        self._lazy = lazy
        self._cache_directory: Optional[str] = None
        self._tokenizer: PreTrainedTokenizer = AutoTokenizer.from_pretrained(
            transformer_tokenizer_name, do_lower_case=to_lower, use_fast=use_fast
        )
        self._max_padding_length = max_padding_length
        self._to_lower = to_lower
        self._use_fast = use_fast
        self._init_parameters = {
            self.TYPE_PARAMETER: self.DATASET_READER_NAME,
            "max_padding_length": max_padding_length,
            "to_lower": to_lower,
            "use_fast": use_fast,
        }

    def cache_data(self, cache_directory: str) -> None:
        """
        When you call this method, we will use this directory to store a cache of already-processed
        ``Instances`` in every file passed to :func:`read`, serialized as one string-formatted
        ``Instance`` per line.  If the cache file for a given ``file_path`` exists, we read the
        ``Instances`` from the cache instead of re-processing the data (using
        :func:`deserialize_instance`).  If the cache file does `not` exist, we will `create` it on
        our first pass through the data (using :func:`serialize_instance`).
        IMPORTANT CAVEAT: It is the `caller's` responsibility to make sure that this directory is
        unique for any combination of code and parameters that you use.  That is, if you call this
        method, we will use any existing cache files in that directory `regardless of the
        parameters you set for this DatasetReader!`  If you use our commands, the ``Train`` command
        is responsible for calling this method and ensuring that unique parameters correspond to
        unique cache directories.  If you don't use our commands, that is your responsibility.
        """
        self._cache_directory = cache_directory
        os.makedirs(self._cache_directory, exist_ok=True)

    def read(self, file_path: str) -> Iterable[Instance]:
        """
        Returns an ``Iterable`` contself.trainer.serialization_diraining all the instances
        in the specified dataset.
        If ``self.lazy`` is False, this calls ``self._read()``,
        ensures that the result is a list, then returns the resulting list.
        If ``self.lazy`` is True, this returns an object whose
        ``__iter__`` method calls ``self._read()`` each iteration.
        In this case your implementation of ``_read()`` must also be lazy
        (that is, not load all instances into memory at once), otherwise
        you will get a ``ConfigurationError``.
        In either case, the returned ``Iterable`` can be iterated
        over multiple times. It's unlikely you want to override this function,
        but if you do your result should likewise be repeatedly iterable.
        """

        if self._lazy is None:
            logger.warning("DatasetReader.lazy is not set, did you forget to call the superclass constructor?")

        cache_file: Optional[str] = None
        if self._cache_directory:
            cache_file = self._get_cache_location_for_file_path(file_path)

        if self._lazy:
            return _LazyInstances(
                lambda: self._read(file_path), cache_file, self.deserialize_instance, self.serialize_instance
            )
        else:
            # First we read the instances, either from a cache or from the original file.
            if cache_file and os.path.exists(cache_file):
                instances = self._instances_from_cache_file(cache_file)
            else:
                instances = self._read(file_path)

            # Then some validation.
            if not isinstance(instances, list):
                instances = [instance for instance in Tqdm.tqdm(instances)]
            if not instances:
                raise ConfigurationError(
                    "No instances were read from the given filepath {}. " "Is the path correct?".format(file_path)
                )

            # And finally we write to the cache if we need to.
            if cache_file and not os.path.exists(cache_file):
                logger.info(f"Caching instances to {cache_file}")
                with open(cache_file, "w") as cache:
                    for instance in Tqdm.tqdm(instances):
                        cache.write(self.serialize_instance(instance) + "\n")
            return instances

    def _get_cache_location_for_file_path(self, file_path: str) -> str:
        if self._cache_directory is None:
            raise ConfigurationError("You haven't specified a cache directory")
        return os.path.join(self._cache_directory, file_path)

    def _read(self, file_path: str) -> Iterable[Instance]:
        """
        Reads the instances from the given file_path and returns them as an
        `Iterable` (which could be a list or could be a generator).
        You are strongly encouraged to use a generator, so that users can
        read a dataset in a lazy way, if they so choose.
        """
        raise NotImplementedError

    def _instances_from_cache_file(self, cache_filename: str) -> Iterable[Instance]:
        with open(cache_filename, "r") as cache_file:
            for line in cache_file:
                yield self.deserialize_instance(line.strip())

    def text_to_instance(self, *inputs: Any, **kwargs: Any) -> Instance:
        """
        Does whatever tokenization or processing is necessary to go from textual input to an
        ``Instance``.  The primary intended use for this is with a
        :class:`~vtroch.service.predictors.predictor.Predictor`, which gets text input as a JSON
        object and needs to process it to be input to a model.
        The intent here is to share code between :func:`_read` and what happens at
        model serving time, or any other time you want to make a prediction from new data.  We need
        to process the data in the same way it was done at training time.  Allowing the
        ``DatasetReader`` to process new text lets us accomplish this, as we can just call
        ``DatasetReader.text_to_instance`` when serving predictions.
        The input type here is rather vaguely specified, unfortunately.  The ``Predictor`` will
        have to make some assumptions about the kind of ``DatasetReader`` that it's using, in order
        to pass it the right information.
        """
        raise NotImplementedError

    def serialize_instance(self, instance: Instance) -> str:
        """
        Serializes an ``Instance`` to a string.  We use this for caching the processed data.
        The default implementation is to use ``jsonpickle``.  If you would like some other format
        for your pre-processed data, override this method.
        """
        # pylint: disable=no-self-use
        return jsonpickle.dumps(instance)

    def deserialize_instance(self, string: str) -> Instance:
        """
        Deserializes an ``Instance`` from a string.  We use this when reading processed data from a
        cache.
        The default implementation is to use ``jsonpickle``.  If you would like some other format
        for your pre-processed data, override this method.
        """
        # pylint: disable=no-self-use
        return jsonpickle.loads(string)  # type: ignore

    def _to_json_file(self, json_file_path: str) -> None:
        with open(json_file_path, "w", encoding="utf-8") as writer:
            writer.write(self._to_json_string())

    def _to_json_string(self) -> str:
        jsonpickle.set_encoder_options('json', sort_keys=True, indent=2)
        return jsonpickle.dumps(self._init_parameters) + "\n"

    @property
    def _tokenizer_type(self) -> str:
        tokenizer_full_type = str(type(self._tokenizer))
        tokenizer_class = tokenizer_full_type.split(".")[-1]
        tokenizer_type = re.findall(r"(.*)Tokenizer", tokenizer_class)[0]
        return tokenizer_type.lower()

    def _save_tokenizer(self, save_directory: str) -> None:
        tokenizer_folder = os.path.join(save_directory, TOKENIZER_FOLDER)
        if not os.path.exists(tokenizer_folder):
            os.makedirs(tokenizer_folder)
        self._tokenizer.save_pretrained(tokenizer_folder)
        with open(os.path.join(tokenizer_folder, TOKENIZER_CONFIG_NAME), "w") as f:
            json.dump({"model_type": self._tokenizer_type}, f)

    def save(self, save_directory: str) -> None:
        dataset_reader_folder = os.path.join(save_directory, DATASET_READER_FOLDER)
        if not os.path.exists(dataset_reader_folder):
            os.makedirs(dataset_reader_folder)
        output_config_file = os.path.join(dataset_reader_folder, DATASET_READER_PARAMETERS_FILE_NAME)
        self._save_tokenizer(dataset_reader_folder)
        self._to_json_file(output_config_file)

    @classmethod
    def load_parameters(cls, path: str) -> Dict[str, Any]:
        dataset_reader_path = os.path.join(path, DATASET_READER_FOLDER)
        with open(
            os.path.join(dataset_reader_path, DATASET_READER_PARAMETERS_FILE_NAME), "r", encoding="utf-8"
        ) as reader:
            text = reader.read()
        dataset_reader_parameters = jsonpickle.loads(text)
        dataset_reader_parameters[TOKENIZER_NAME_FIELD] = os.path.join(dataset_reader_path, TOKENIZER_FOLDER)
        return dataset_reader_parameters
