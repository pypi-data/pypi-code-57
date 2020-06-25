# Copyright 2011-2014 Biomedical Imaging Group Rotterdam, Departments of
# Medical Informatics and Radiology, Erasmus MC, Rotterdam, The Netherlands
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This package contains the base class and meta class for all serializable
objects in the Fastr system.
"""

import gzip
import json
import os
import pickle
from abc import abstractstaticmethod, abstractmethod
from collections.abc import Mapping
import time
from pathlib import Path
from typing import Union, Optional, IO, Tuple

from jsonschema.exceptions import ValidationError
import yaml

from .. import exceptions, version
from ..helpers import xmltodict, jsonschemaparser, config, log


class ReadWriteHandler:
    HANDLERS = {}

    # Needs to be implemented in subclasses to register
    EXTENSIONS = ()

    def __init_subclass__(cls, **kwargs):
        for extension in cls.EXTENSIONS:
            cls.HANDLERS[extension] = cls

    @classmethod
    def get_handler(cls, method):
        return cls.HANDLERS[method]

    @abstractstaticmethod
    def dump(doc: dict, stream: IO, **kwargs):
        """
        Dump doc into a stream

        :param stream: Stream to write to
        :param doc: Doc to write
        :param kwargs: Extra arguments for specific subclasses
        :return:
        """

    @abstractstaticmethod
    def dumps(doc: dict, **kwargs) -> str:
        """
        Dump doc into a string

        :param doc: Doc to write
        :param kwargs: Extra arguments for specific subclasses
        :return: string representation of the doc
        """

    @classmethod
    def dumpf(cls, doc: dict, path: Union[str, os.PathLike], **kwargs):
        """
        Dump doc into a file

        :param doc: The data to write to the file
        :param path: Path of the file to write
        :param kwargs: Extra arguments for specific subclasses
        """
        if isinstance(path, os.PathLike):
            path = path.__fspath__()

        compress = path.endswith('.gz')

        if compress:
            open_func = gzip.open
        else:
            open_func = open

        with open_func(path, 'w') as fh_out:
            cls.dump(doc, fh_out, **kwargs)

            # Try to flush the file best as possible
            fh_out.flush()
            os.fsync(fh_out.fileno())

    @abstractstaticmethod
    def load(stream: IO) -> dict:
        """
        Load object doc from a stream

        :param stream: stream to load from
        :return: the dict representation of the object read
        """

    @abstractstaticmethod
    def loads(data: str) -> dict:
        """
        Load object doc from a string

        :param data: The string representation to load
        :return: The dict representation of the result
        """

    @classmethod
    def loadf(cls, path: Union[str, os.PathLike], retry_scheme: Tuple[int, ...]=(1, 3, 5)) -> dict:
        """
        Load object doc from a file

        :param path: Path of the file to load
        :return: The dict represention of the loaded object
        """
        if isinstance(path, Path):
            compress = path.suffix == '.gz'
        else:
            compress = path.endswith('.gz')

        if compress:
            open_func = gzip.open
        else:
            open_func = open

        attempt = 0

        # Loop for max retries
        while attempt <= len(retry_scheme):
            try:
                with open_func(path, 'rb') as fin:
                    data = cls.load(fin)
                break
            except Exception as exception:
                if attempt < len(retry_scheme):
                    delay = retry_scheme[0]
                    attempt += 1
                    log.debug('Retry {} after {} seconds of delay'.format(attempt, delay))
                    time.sleep(delay)
                elif isinstance(exception, FileNotFoundError):
                    raise exceptions.FastrFileNotFound(f'Could not open {path} for reading')
                else:
                    raise exception

        return data


class YamlHandler(ReadWriteHandler):
    """
    Read and write data to YAML files
    """
    EXTENSIONS = ('yaml', 'yml')

    @staticmethod
    def dump(data, stream, sort_keys=False, **kwargs):
        yaml.safe_dump(data, stream=stream, sort_keys=sort_keys, **kwargs)

    @staticmethod
    def dumps(data, sort_keys=False, **kwargs) -> str:
        return yaml.safe_dump(data, sort_keys=sort_keys, **kwargs)

    @staticmethod
    def load(data):
        return yaml.safe_load(data)

    @staticmethod
    def loads(data: str):
        return yaml.safe_load(data)


class JSONHandler(ReadWriteHandler):
    EXTENSIONS = ('json',)

    @staticmethod
    def dump(data, stream, **kwargs):
        json.dump(data, stream, **kwargs)

    @staticmethod
    def dumps(data, **kwargs) -> str:
        return json.dumps(data, **kwargs)

    @staticmethod
    def load(stream, **kwargs):
        return json.load(stream, **kwargs)

    @staticmethod
    def loads(data: str, **kwargs):
        return json.loads(data, **kwargs)


class XMLHandler(ReadWriteHandler):
    EXTENSIONS = ('xml',)

    @staticmethod
    def dump(data, stream):
        xmltodict.dump(data, stream)

    @staticmethod
    def dumps(data):
        return xmltodict.dumps(data)

    @staticmethod
    def load(stream):
        return xmltodict.load(stream)

    @staticmethod
    def loads(data: str):
        return xmltodict.loads(data)


class PassThroughHandler(ReadWriteHandler):
    """
    Passthrough handler for debugging of data just shows
    the string representation of the data
    """
    EXTENSIONS = ('dict',)

    @staticmethod
    def dump(stream, data):
        stream.write(repr(data))

    @staticmethod
    def dumps(data):
        return repr(data)

    @staticmethod
    def load(stream):
        raise NotImplementedError

    @staticmethod
    def loads(data: str):
        raise NotImplementedError


class Serializable:
    """
    Superclass for all classes that can be serialized.
    """
    SERIALIZERS = {}
    SERIALIZABLE_CLASSES = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        cls.SERIALIZABLE_CLASSES[cls.class_key()] = cls

    @classmethod
    def class_key(cls):
        return f'{cls.__module__}.{cls.__name__}'

    @classmethod
    def get_class(cls, key, default=None) -> 'Serializable':
        return cls.SERIALIZABLE_CLASSES.get(key, default)

    @classmethod
    def get_serializer(cls, filename=None):
        if filename is None:
            if hasattr(cls, '__dataschemafile__'):
                filename = cls.__dataschemafile__
            else:
                raise exceptions.FastrValueError('Cannot get serializer for class without dataschemafile specified!')
        if not os.path.exists(filename):
            filename = os.path.join(config.schemadir, filename)

        if filename not in cls.SERIALIZERS:
            try:
                cls.SERIALIZERS[filename] = jsonschemaparser.getblueprinter(filename)
            except IOError as err:
                log.warning('Serializable class {} cannot read schemafile {}: {}'.format(
                    cls.__name__, filename, err.strerror))

        return cls.SERIALIZERS[filename]

    @abstractmethod
    def __getstate__(self):
        raise exceptions.FastrNotImplementedError('For a Serializable the __getstate__ has to be set by the subjc')

    @classmethod
    def deserialize(cls, doc, network=None):
        """
        Classmethod that returns an object constructed based on the
        str/dict (or OrderedDict) representing the object

        :param dict doc: the state of the object to create
        :param network: the network the object will belong to
        :type network: :py:class:`Network <fastr.planning.network.Network>`
        :return: newly created object
        """
        return cls.createobj(doc, network)

    @classmethod
    def createobj(cls, state, _=None):
        """
        Create object function for generic objects

        :param cls: The class to create
        :param state: The state to use to create the Link
        :param network: the parent Network
        :return: newly created Link
        """
        # If object is immutable with new args
        if hasattr(cls, '__getnewargs__'):
            if isinstance(state, Mapping):
                obj = cls.__new__(cls, **state)
            else:
                obj = cls.__new__(cls, *state)

        else:
            # Otherwise object can be created empty and set the state
            obj = cls.__new__(cls)

        if hasattr(obj, '__setstate__'):
            # We just check if __setstate__ existed, but pylint missed that
            # pylint: disable=no-member,maybe-no-member
            obj.__setstate__(state)
        elif hasattr(obj, '__dict__'):
            obj.__dict__.update(state)

        return obj

    def serialize(self):
        """
        Method that returns a dict/str/list structure with the data to rebuild
        the object.

        :returns: serialized representation of object
        """
        doc = self.__getstate__()
        return doc


def save(obj: Serializable, path: Union[str, os.PathLike], method: Optional[str]=None, annotate: bool = True):
    if isinstance(path, os.PathLike):
        path = path.__fspath__()

    if method is None:
        method = os.path.splitext(path)[1][1:]

    # Note the class used
    data = obj.serialize()
    if annotate:
        data['__class__'] = obj.class_key()
        data['__fastr_version__'] = version.full_version

    handler = ReadWriteHandler.get_handler(method)
    handler.dumpf(data, path)


def load(path: Union[str, os.PathLike], method: Optional[str]=None, cls=None):
    if isinstance(path, os.PathLike):
        path = path.__fspath__()

    if method is None:
        method = os.path.splitext(path)[1][1:]

    handler = ReadWriteHandler.get_handler(method)
    data = handler.loadf(path)

    if cls is None:
        class_spec = data.pop('__class__')

        if class_spec is None:
            raise exceptions.FastrValueError('Class is not added in the document, cannot find class to create')

        cls = Serializable.get_class(class_spec)

    fastr_version = data.pop('__fastr_version__', None)
    if fastr_version is None:
        log.debug(f'Loading objects without a fastr version')
    elif fastr_version != version.full_version:
        log.warning(f'Loading objects created with different version of fastr '
                    f'(current {version.full_version}, object saved with {fastr_version}')

    if hasattr(cls, '__dataschemafile__'):
        # We just check if __dataschemafile__ existed, but pylint missed that
        # pylint: disable=no-member
        data = cls.get_serializer().instantiate(data)

    # Instantiate object
    obj = cls.deserialize(data)

    # Store path
    obj.filename = path

    return obj
