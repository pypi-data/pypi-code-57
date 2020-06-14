# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio
import configparser
import os
import pprint
from enum import Enum
from typing import Optional, Dict, List, Any, Tuple, Iterable

import dependency_injector.containers
import dependency_injector.providers
import inflection
from six import string_types

import wagascianpy.utils.environment
import wagascianpy.utils.utils
from wagascianpy.utils.classproperty import classproperty


class RepositoryType(Enum):
    Simple = 1
    Borg = 2


###############################################################################################
#                                        Default values                                       #
###############################################################################################

# WAGASCI database configuration
_WAGASCI_DATABASE = "kekcc:/hsm/nu/wagasci/data/beam/wagascidb.db"
_WAGASCI_REPOSITORY = "kekcc:/hsm/t2k/t2k_JB/t2k_wagasci/rawdata"
_WAGASCI_REPOSITORY_TYPE = RepositoryType.Simple
_WAGASCI_DOWNLOAD_LOCATION = "/tmp/rawdata"
_WAGASCI_DECODED_LOCATION = "/tmp/decoded"
_WAGASCI_DEFAULT_DATABASE_NAME = "wagascidb.db"

# BSD database configuration
_BSD_DATABASE = "kekcc:/hsm/nu/wagasci/data/bsd/bsddb.db"
_BSD_REPOSITORY = "kekcc:/gpfs/fs03/t2k/beam/exp/data/beam_summary/current"
_BSD_DOWNLOAD_LOCATION = "/tmp/bsd"
_BSD_DEFAULT_DATABASE_NAME = "bsddb.db"

# Global configuration
_T2KRUN = 10
_DATA_QUALITY_LOCATION = "/tmp/data_quality"

# Temperature database configuration
_TEMPERATURE_SQLITE_DATABASE = "kekcc:/hsm/nu/wagasci/data/temphum/mh_temperature_sensors_t2krun10.sqlite3"


###############################################################################################
#                                         Utilities                                           #
###############################################################################################

def conf_file_finder(filename, project_path=None):
    # type: (str, Optional[str, List[str]]) -> str
    home = os.path.expanduser("~")
    wagasci_environ = None

    try:
        env = wagascianpy.utils.environment.WagasciEnvironment()
        wagasci_environ = env["WAGASCI_CONFDIR"]
    except KeyError:
        pass

    if isinstance(project_path, list):
        wagasci_project = list(map(lambda x: os.path.join(x, filename), project_path))
    elif isinstance(project_path, str):
        wagasci_project = [os.path.join(project_path, filename)]
    else:
        wagasci_project = None
    if wagasci_environ:
        wagasci_environ = os.path.join(wagasci_environ, filename)
    wagasci_user = os.path.join(home, '.wagasci', filename)
    wagasci_system = os.path.join('/usr/local/wagasci/', filename)

    conf_file = None
    if wagasci_environ and os.path.exists(wagasci_environ):
        conf_file = wagasci_environ
    elif wagasci_user and os.path.exists(wagasci_user):
        conf_file = wagasci_user
    elif wagasci_system and os.path.exists(wagasci_system):
        conf_file = wagasci_system
    elif wagasci_project:
        for path in wagasci_project:
            if os.path.exists(path):
                conf_file = path
                break
    else:
        wagascianpy.utils.utils.mkdir_p(os.path.join(home, '.wagasci'))
        conf_file = wagasci_user
    return conf_file


def _conf_setter_raise(cls, name, value):
    # type: (Any, str, Any) -> None
    raise ValueError("Invalid value {} for option {} of class {}".format(name, value, cls.__name__))


def conf_setter(cls, name, value):
    # type: (Any, str, Any) -> None
    try:
        if isinstance(getattr(cls, name), Enum):
            if isinstance(value, Enum):
                setattr(cls, name, value)
            elif isinstance(value, int):
                setattr(cls, name, type(getattr(cls, name))(value))
            elif isinstance(value, string_types):
                if '.' in value:
                    value = value.split('.')[1]
                try:
                    setattr(cls, name, getattr(type(getattr(cls, name)), inflection.camelize(value.lower())))
                except AttributeError:
                    raise ValueError
        elif isinstance(getattr(cls, name), bool):
            if isinstance(value, string_types):
                value = value.lower()
            if value in [0, False, None, 'none', 'false', 'off', 'no']:
                setattr(cls, name, False)
            elif value in [1, True, 'true', 'on', 'yes']:
                setattr(cls, name, True)
            else:
                raise ValueError
        elif isinstance(getattr(cls, name), int):
            value = int(value) if value is not None else 0
            setattr(cls, name, int(value))
        elif isinstance(getattr(cls, name), float):
            value = float(value) if value is not None else 0.
            setattr(cls, name, float(value))
        else:
            value = str(value) if value is not None else ''
            setattr(cls, name, str(value))
    except ValueError:
        _conf_setter_raise(cls, name, value)


def conf_getter(cls, name):
    # type: (Any, str) -> Any
    return getattr(cls, name)


###############################################################################################
#                                    Configuration classes                                    #
###############################################################################################

@wagascianpy.utils.classproperty.with_metaclass(classproperty.meta)
class VirtualConfiguration(object):

    @classmethod
    def to_dict(cls):
        # type: (...) -> Dict[str, Any]
        return {key: val.__get__(instance=None, owner=cls) for key, val in vars(cls).items()
                if isinstance(val, classproperty)}

    @classmethod
    def get_hidden_vars(cls):
        # type: (...) -> Iterable[str]
        return [key for key, val in vars(cls).items()
                if key.startswith('_') and not key.startswith('__') and not callable(val)]

    @classmethod
    def get_classproperties(cls):
        # type: (...) -> Iterable[str]
        return [key for key, val in vars(cls).items() if isinstance(val, classproperty)]

    @classmethod
    def dump(cls, indentation_level=0):
        # type: (int) -> None
        for propery in cls.get_classproperties():
            print("{}{} = {}".format(' ' * indentation_level, propery, getattr(cls, propery)))


# noinspection PyMethodParameters,PyPropertyDefinition
class GlobalConfiguration(VirtualConfiguration):
    _t2krun = _T2KRUN
    _data_quality_location = _DATA_QUALITY_LOCATION

    @classmethod
    def reset(cls):
        cls._t2krun = _T2KRUN
        cls._data_quality_location = _DATA_QUALITY_LOCATION

    @classmethod
    def is_volatile(cls):
        return False

    @classproperty
    def t2krun(cls):
        return conf_getter(cls=cls, name='_t2krun')

    @t2krun.setter
    def t2krun(cls, value):
        conf_setter(cls=cls, name='_t2krun', value=value)

    @classproperty
    def data_quality_location(cls):
        return conf_getter(cls=cls, name='_data_quality_location')

    @data_quality_location.setter
    def data_quality_location(cls, value):
        conf_setter(cls=cls, name='_data_quality_location', value=value)


# noinspection PyMethodParameters,PyPropertyDefinition
class WagasciDatabaseConfiguration(VirtualConfiguration):
    _wagasci_database = _WAGASCI_DATABASE
    _wagasci_repository = _WAGASCI_REPOSITORY
    _repository_type = _WAGASCI_REPOSITORY_TYPE
    _wagasci_download_location = _WAGASCI_DOWNLOAD_LOCATION
    _wagasci_decoded_location = _WAGASCI_DECODED_LOCATION
    _default_database_name = _WAGASCI_DEFAULT_DATABASE_NAME

    @classmethod
    def reset(cls):
        cls._wagasci_database = _WAGASCI_DATABASE
        cls._wagasci_repository = _WAGASCI_REPOSITORY
        cls._repository_type = _WAGASCI_REPOSITORY_TYPE
        cls._wagasci_download_location = _WAGASCI_DOWNLOAD_LOCATION
        cls._wagasci_decoded_location = _WAGASCI_DECODED_LOCATION
        cls._default_database_name = _WAGASCI_DEFAULT_DATABASE_NAME

    @classmethod
    def is_volatile(cls):
        return False

    @classproperty
    def wagasci_database(cls):
        return conf_getter(cls=cls, name='_wagasci_database')

    @wagasci_database.setter
    def wagasci_database(cls, value):
        conf_setter(cls=cls, name='_wagasci_database', value=value)

    @classproperty
    def wagasci_repository(cls):
        return conf_getter(cls=cls, name='_wagasci_repository')

    @wagasci_repository.setter
    def wagasci_repository(cls, value):
        conf_setter(cls=cls, name='_wagasci_repository', value=value)

    @classproperty
    def repository_type(cls):
        return conf_getter(cls=cls, name='_repository_type')

    @repository_type.setter
    def repository_type(cls, value):
        conf_setter(cls=cls, name='_repository_type', value=value)

    @classproperty
    def wagasci_download_location(cls):
        return conf_getter(cls=cls, name='_wagasci_download_location')

    @wagasci_download_location.setter
    def wagasci_download_location(cls, value):
        conf_setter(cls=cls, name='_wagasci_download_location', value=value)

    @classproperty
    def wagasci_decoded_location(cls):
        return conf_getter(cls=cls, name='_wagasci_decoded_location')

    @wagasci_decoded_location.setter
    def wagasci_decoded_location(cls, value):
        conf_setter(cls=cls, name='_wagasci_decoded_location', value=value)

    @classproperty
    def default_database_name(cls):
        return conf_getter(cls=cls, name='_default_database_name')

    @default_database_name.setter
    def default_database_name(cls, value):
        conf_setter(cls=cls, name='_default_database_name', value=value)


# noinspection PyMethodParameters,PyPropertyDefinition
class BsdDatabaseConfiguration(VirtualConfiguration):
    _bsd_database = _BSD_DATABASE
    _bsd_repository = _BSD_REPOSITORY
    _bsd_download_location = _BSD_DOWNLOAD_LOCATION
    _default_database_name = _BSD_DEFAULT_DATABASE_NAME

    @classmethod
    def reset(cls):
        cls._bsd_database = _BSD_DATABASE
        cls._bsd_repository = _BSD_REPOSITORY
        cls._bsd_download_location = _BSD_DOWNLOAD_LOCATION
        cls._default_database_name = _BSD_DEFAULT_DATABASE_NAME

    @classmethod
    def is_volatile(cls):
        return False

    @classproperty
    def bsd_database(cls):
        return conf_getter(cls=cls, name='_bsd_database')

    @bsd_database.setter
    def bsd_database(cls, value):
        conf_setter(cls=cls, name='_bsd_database', value=value)

    @classproperty
    def bsd_repository(cls):
        return conf_getter(cls=cls, name='_bsd_repository')

    @bsd_repository.setter
    def bsd_repository(cls, value):
        conf_setter(cls=cls, name='_bsd_repository', value=value)

    @classproperty
    def bsd_download_location(cls):
        return conf_getter(cls=cls, name='_bsd_download_location')

    @bsd_download_location.setter
    def bsd_download_location(cls, value):
        conf_setter(cls=cls, name='_bsd_download_location', value=value)

    @classproperty
    def default_database_name(cls):
        return conf_getter(cls=cls, name='_default_database_name')

    @default_database_name.setter
    def default_database_name(cls, value):
        conf_setter(cls=cls, name='_default_database_name', value=value)


# noinspection PyMethodParameters,PyMethodParameters,PyPropertyDefinition
class TemperatureConfiguration(VirtualConfiguration):
    _temperature_sqlite_database = _TEMPERATURE_SQLITE_DATABASE

    @classmethod
    def reset(cls):
        cls._temperature_sqlite_database = _TEMPERATURE_SQLITE_DATABASE

    @classmethod
    def is_volatile(cls):
        return False

    @classproperty
    def temperature_sqlite_database(cls):
        return conf_getter(cls=cls, name='_temperature_sqlite_database')

    @temperature_sqlite_database.setter
    def temperature_sqlite_database(cls, value):
        conf_setter(cls=cls, name='_temperature_sqlite_database', value=value)


###############################################################################################
#                                    Configuration parser                                     #
###############################################################################################


class WagasciConfigParser(GlobalConfiguration,
                          WagasciDatabaseConfiguration,
                          BsdDatabaseConfiguration,
                          TemperatureConfiguration):

    def _baseclasses(self):
        # type: (...) -> Optional[Tuple]
        base_classes = WagasciConfigParser.__bases__
        if self.__class__ != WagasciConfigParser:
            base_classes += tuple([bc for bc in self.__class__.__bases__ if bc != WagasciConfigParser])
        return base_classes

    def __init__(self, config_file_path=None):
        # type: (Optional[str]) -> None

        # Create ConfigParser default object
        self._config_parser = configparser.ConfigParser()

        # Set default values and create the section object attributes
        for base_class in self._baseclasses():
            section_name = inflection.underscore(base_class.__name__)
            setattr(self, section_name, base_class)

        # fill the ConfigParser object
        self._fill_config_parser()

        # check file access permissions
        if config_file_path:
            if not os.access(os.path.dirname(config_file_path), os.W_OK):
                raise OSError("The configuration file path is not writable "
                              "by the current user : %s" % config_file_path)
            # If the configuration file exists read it
            if os.path.exists(config_file_path):
                print("Reading configuration from file")
                self._config_parser.read(config_file_path)
                for section in self._config_parser.sections():
                    if not hasattr(self, section):
                        raise AttributeError("Section name not recognized : %s" % section)
                    for key, val in self._config_parser.items(section=section):
                        setattr(getattr(self, section), key, val)
            else:
                # If the file does not exist write the default configuration to file
                with open(config_file_path, 'w') as configfile:
                    print("Writing default configuration to file")
                    self._config_parser.write(configfile)

    def get_sections(self):
        # type: (...) -> Optional[List[str]]
        return [key for key in vars(self) if not key.startswith('_')]

    def get_section(self, name):
        # type: (str) -> Any
        return getattr(self, name)

    def prettyprint(self):
        for section in self.get_sections():
            print()
            print(section.upper().replace('_', ' '))
            pprint.pprint(self.get_section(section).to_dict())

    def _fill_config_parser(self):
        for section in self.get_sections():
            if not self.get_section(section).is_volatile():
                if not self._config_parser.has_section(section):
                    self._config_parser.add_section(section)
                for key, var in self.get_section(section).to_dict().items():
                    if isinstance(var, Enum):
                        var = str(var).split('.')[1]
                    self._config_parser.set(section, key, str(var))

    def write(self, config_file_path):
        self._fill_config_parser()
        with open(config_file_path, 'w') as configfile:
            self._config_parser.write(configfile)


###############################################################################################
#                                Configuration Global Object                                  #
###############################################################################################


def _create_sections(cls, parser_class=WagasciConfigParser):
    conf_file = conf_file_finder(filename='wagasci_conf.ini', project_path='../..')
    parser = parser_class(conf_file)
    setattr(cls, 'parser', parser)
    for section in parser.get_sections():
        if not hasattr(cls, section):
            setattr(cls, section, dependency_injector.providers.Configuration(section))
            getattr(cls, section).override(getattr(parser, section).to_dict())
    return cls


# wrap _create_sections to allow for deferred calling
def create_sections(cls=None, parser_class=WagasciConfigParser):
    if cls:
        return _create_sections(cls)
    else:
        def wrapper(function):
            return _create_sections(function, parser_class)
        return wrapper


@create_sections
class Configuration(dependency_injector.containers.DeclarativeContainer):
    """IoC container of configuration providers."""

    @classmethod
    def create_section(cls, name):
        # type: (str) -> None
        if not hasattr(cls, name):
            setattr(cls, name, dependency_injector.providers.Configuration(name))

    @classmethod
    def delete_section(cls, name):
        # type: (str) -> None
        if hasattr(cls, name):
            delattr(cls, name)

    @classmethod
    def get_sections(cls):
        # type: (...) -> Optional[List[str]]
        return [val.get_name() for val in vars(cls).values()
                if isinstance(val, dependency_injector.providers.Configuration)]

    @classmethod
    def dump(cls):
        for section in cls.parser.get_sections():
            print("[{}]".format(section))
            getattr(cls.parser, section).dump(indentation_level=2)


if __name__ == "__main__":
    Configuration.parser.prettyprint()
