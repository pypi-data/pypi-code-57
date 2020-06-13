__all__ = ["Yaap"]

import sys
import json
import yaml
import warnings
import argparse
from dataclasses import dataclass
from typing import Dict, Sequence, Any, Optional

import jsonschema

from .argument import *
from .utils import private_field


@dataclass
class Yaap:
    name: str = None
    desc: str = None
    on_extra: str = "error"
    add_config_arg: bool = True
    config_arg_name: str = "config"
    add_schema_arg: bool = True
    schema_arg_name: str = "schema"
    _parser: argparse.ArgumentParser = private_field()
    _reserved_parser: argparse.ArgumentParser = private_field()
    _args: Dict[str, Argument] = private_field(default_factory=dict)

    def __post_init__(self):
        if self.on_extra not in {"error", "warn", "ignore"}:
            raise ValueError(f"unrecognized on_extra mode: {self.on_extra}")
        self._parser = argparse.ArgumentParser(
            prog=None if self.name is None else self.name,
            description=None if self.desc is None else self.desc
        )
        self._reserved_parser = argparse.ArgumentParser()
        if self.add_config_arg:
            config_arg = Path(
                name=self.config_arg_name,
                must_exist=True,
                help="Path to a configuration (json/yaml) file "
                     "that contains argument key-values. For keys "
                     "that are specified in both command-line "
                     "arguments and config arguments, the former "
                     "will take precedence."
            )
            self._add_reserved(config_arg)
        if self.add_schema_arg:
            schema_arg = Bool(
                self.schema_arg_name,
                help="Prints the argument schema in json format."
            )
            self._add_reserved(schema_arg)

    @property
    def reserved_arg_names(self):
        return self.config_arg_name, self.schema_arg_name

    def _add_reserved(self, arg: Argument):
        self._args[arg.name] = arg
        args, kwargs = arg.generate_args()
        self._parser.add_argument(*args, **kwargs)
        self._reserved_parser.add_argument(*args, **kwargs)

    def add(self, arg: Argument):
        if arg.name in self._args:
            raise NameError(f"argument of the same name exists: "
                            f"{self._args[arg.name]}")
        if arg.name in self.reserved_arg_names:
            raise NameError(f"argument name is reserved: {arg.name}")
        self._args[arg.name] = arg
        args, kwargs = arg.generate_args()
        self._parser.add_argument(*args, **kwargs)

    def add_int(self,
                name: str,
                shortcut: str = None,
                help: str = None,
                required: bool = False,
                default: Any = None,
                min_bound: int = None,
                max_bound: int = None,
                multiples: int = None,
                choices: Sequence[int] = None,
                is_list: bool = False,
                num_elements: int = None):
        """Specifies an integer-type argument.

        Arguments:
            name (str): Name of the argument. Unlike `argparse`, preceding
                hyphens should be omitted. Allows specification by `--{name}`.
            shortcut (optional, str): Argument shortcut. Allows specification
                by `-{shortcut}`.
            help (optional, str): Help text.
            required (optional, str): Whether this argument is required.
            default (optional, *): Default value for the argument. Must be
                hashable (`__hash__`).
            min_bound (optional, int): Minimum bounds for the integer argument.
                Bound inclusive.
            max_bound (optional, int): Maximum bounds for the integer argument.
                Bound inclusive.
            multiples (optional, int): Enforces the argument to be a multiple
                of this number.
            choices (optional, Sequence[int]): Enforces the argument to be
                one of these candidate numbers.
            is_list (bool): Whether this argument is of list type. If true,
                this argument can be specified with multiple values, i.e.

                    --{name} {val1} {val2} ... {valN}

                (default: False)
            num_elements (optional, int): Number of required elements.
                Applicable only if `is_list` is true.
        """
        kwargs = dict(
            name=name,
            shortcut=shortcut,
            help=help,
            required=required,
            default=default,
            min_bound=min_bound,
            max_bound=max_bound,
            multiples=multiples,
            choices=choices
        )
        if is_list:
            kwargs.update(dict(num_elements=num_elements))
        cls = Int if not is_list else IntList
        return self.add(cls(**kwargs))

    def add_flt(self,
                name: str,
                shortcut: str = None,
                help: str = None,
                required: bool = False,
                default: Any = None,
                min_bound: float = None,
                max_bound: float = None,
                multiples: float = None,
                choices: Sequence[float] = None,
                is_list: bool = False,
                num_elements: int = None):
        """Specifies a float-type argument.

        Arguments:
            name (str): Name of the argument. Unlike `argparse`, preceding
                hyphens should be omitted. Allows specification by `--{name}`.
            shortcut (optional, str): Argument shortcut. Allows specification
                by `-{shortcut}`.
            help (optional, str): Help text.
            required (optional, str): Whether this argument is required.
            default (optional, *): Default value for the argument. Must be
                hashable (`__hash__`).
            min_bound (optional, float): Minimum bounds for the float argument.
                Bound inclusive.
            max_bound (optional, float): Maximum bounds for the float argument.
                Bound inclusive.
            multiples (optional, float): Enforces the argument to be a multiple
                of this number.
            choices (optional, Sequence[float]): Enforces the argument to be
                one of these candidate numbers.
            is_list (bool): Whether this argument is of list type. If true,
                this argument can be specified with multiple values, i.e.

                    --{name} {val1} {val2} ... {valN}

                (default: False)
            num_elements (optional, int): Number of required elements.
                Applicable only if `is_list` is true.
        """
        kwargs = dict(
            name=name,
            shortcut=shortcut,
            help=help,
            required=required,
            default=default,
            min_bound=min_bound,
            max_bound=max_bound,
            multiples=multiples,
            choices=choices
        )
        if is_list:
            kwargs.update(dict(num_elements=num_elements))
        cls = Float if not is_list else FloatList
        return self.add(cls(**kwargs))

    def add_float(self, *args, **kwargs):
        """See `self.add_flt`."""
        return self.add_flt(*args, **kwargs)

    def add_pth(self,
                name: str,
                shortcut: str = None,
                help: str = None,
                required: bool = False,
                default: Any = None,
                must_exist: bool = False,
                is_dir: bool = False,
                is_list: bool = False,
                num_elements: int = None):
        """Specifies a path-type argument.

        Arguments:
            name (str): Name of the argument. Unlike `argparse`, preceding
                hyphens should be omitted. Allows specification by `--{name}`.
            shortcut (optional, str): Argument shortcut. Allows specification
                by `-{shortcut}`.
            help (optional, str): Help text.
            required (optional, str): Whether this argument is required.
            default (optional, *): Default value for the argument. Must be
                hashable (`__hash__`).
            must_exist (bool): The specified path must be an existing one.
                The argument parser will check whether path(s) do exist.
                (default: False)
            is_dir (bool): Whether the path is of directory type.
                The argument parser will check whether path(s) are directories.
                (default: False)
            is_list (bool): Whether this argument is of list type. If true,
                this argument can be specified with multiple values, i.e.

                    --{name} {val1} {val2} ... {valN}

                (default: False)
            num_elements (optional, int): Number of required elements.
                Applicable only if `is_list` is true.
        """
        kwargs = dict(
            name=name,
            shortcut=shortcut,
            help=help,
            required=required,
            default=default,
            must_exist=must_exist,
            is_dir=is_dir
        )
        if is_list:
            kwargs.update(dict(num_elements=num_elements))
        cls = Path if not is_list else PathList
        return self.add(cls(**kwargs))

    def add_path(self, *args, **kwargs):
        """See `self.add_pth`."""
        return self.add_pth(*args, **kwargs)

    def add_str(self,
                name: str,
                shortcut: str = None,
                help: str = None,
                required: bool = False,
                default: Any = None,
                min_length: int = None,
                max_length: int = None,
                regex: str = None,
                format: str = None,
                choices: Sequence[float] = None,
                is_list: bool = False,
                num_elements: int = None):
        """Specifies a string-type argument.

        Arguments:
            name (str): Name of the argument. Unlike `argparse`, preceding
                hyphens should be omitted. Allows specification by `--{name}`.
            shortcut (optional, str): Argument shortcut. Allows specification
                by `-{shortcut}`.
            help (optional, str): Help text.
            required (optional, str): Whether this argument is required.
            default (optional, *): Default value for the argument. Must be
                hashable (`__hash__`).
            min_length (optional, int): Minimum bound for length (inclusive).
            max_length (optional, int): Maximum bound for length (inclusive).
            regex (optional, str): Regular expression for matching values.
                The argument parser will check whether the value(s) conform
                the regular expression.
            format (optional, str): String format, as supported by JSONSchema.
                Some common formats include `date-time`, `time`, `url`, `email`.
                More information at JSONSchema reference.
            choices (optional, Sequence[str]): Enforces the argument to be
                one of these candidate strings.
            is_list (bool): Whether this argument is of list type. If true,
                this argument can be specified with multiple values, i.e.

                    --{name} {val1} {val2} ... {valN}

                (default: False)
            num_elements (optional, int): Number of required elements.
                Applicable only if `is_list` is true.
        """
        kwargs = dict(
            name=name,
            shortcut=shortcut,
            help=help,
            required=required,
            default=default,
            min_length=min_length,
            max_length=max_length,
            regex=regex,
            format=format,
            choices=choices
        )
        if is_list:
            kwargs.update(dict(num_elements=num_elements))
        cls = Str if not is_list else StrList
        return self.add(cls(**kwargs))

    def add_bol(self,
                name: str,
                shortcut: str = None,
                help: str = None,
                required: bool = False,
                invert: bool = False):
        """Specifies a bool-type argument. This is value-less argument, which is
        specified with only the keyword argument, i.e. `--{name}`.

        Arguments:
            name (str): Name of the argument. Unlike `argparse`, preceding
                hyphens should be omitted. Allows specification by `--{name}`.
            shortcut (optional, str): Argument shortcut. Allows specification
                by `-{shortcut}`.
            help (optional, str): Help text.
            required (optional, str): Whether this argument is required.
            invert (bool): Whether to invert bool operation. The default
                behavior stores True when the argument is specified and False
                for otherwise.
                (default: False)
        """
        return self.add(Bool(
            name=name,
            shortcut=shortcut,
            help=help,
            required=required,
            invert=invert
        ))

    def add_bool(self, *args, **kwargs):
        """See `self.add_bol`"""
        return self.add_bol(*args, **kwargs)

    def add_intlist(self, *args, **kwargs):
        return self.add_int(*args, **kwargs, is_list=True)

    def add_floatlist(self, *args, **kwargs):
        return self.add_flt(*args, **kwargs, is_list=True)

    def add_pathlist(self, *args, **kwargs):
        return self.add_pth(*args, **kwargs, is_list=True)

    def add_strlist(self, *args, **kwargs):
        return self.add_str(*args, **kwargs, is_list=True)

    def schema(self) -> dict:
        """Returns this argument specification in terms of JSONSchema."""
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$id": str(hash((self.name, self.desc))),
            "type": "object",
            "properties": {arg.name: arg.json_schema()
                           for arg in self._args.values()},
            "required": [arg.name for arg in
                         self._args.values() if arg.required]
        }

    def validate(self, args: dict):
        """Validate a dictionary of arguments against this argument spec."""
        jsonschema.validate(args, self.schema())

    def print_schema(self):
        schema = self.schema()
        sys.stdout.write(json.dumps(schema, ensure_ascii=False, indent=2))

    def _parse_config(self, config: dict):
        args = []
        for k, v in config.items():
            if v is None:
                continue
            arg: Argument = self._args[k]
            if isinstance(v, bool):
                assert isinstance(arg, Bool)
                if v != arg.invert:
                    args.append(f"--{k}")
            elif isinstance(v, str):
                args.extend([f"--{k}", v])
            elif isinstance(v, list):
                args.append(f"--{k}")
                args.extend(map(str, v))
            else:
                args.extend((f"--{k}", str(v)))
        return args

    def _argparse(self, args, namespace=None):
        if self.on_extra == "ignore" or self.on_extra == "warn":
            namespace, extra_args = \
                self._parser.parse_known_args(args, namespace)
            if self.on_extra == "warn":
                warnings.warn(f"following arguments are not argparsed: "
                              f"{extra_args}")
        elif self.on_extra == "error":
            namespace = self._parser.parse_args(args, namespace)
        return namespace

    def parse(self, args: Optional[Sequence[str]] = None,
              namespace: Optional[argparse.Namespace] = None
              ) -> argparse.Namespace:
        if not self.reserved_arg_names:
            return self._argparse(args=args, namespace=namespace)
        reserved_namespace, _ = self._reserved_parser.parse_known_args(args)
        if self.add_schema_arg and getattr(reserved_namespace,
                                           self.schema_arg_name):
            self.print_schema()
            exit(0)
        if self.add_config_arg:
            config_path = getattr(reserved_namespace, self.config_arg_name)
            if config_path is not None:
                with open(config_path, "r") as f:
                    config = yaml.safe_load(f)
                self.validate(config)
                config_args = self._parse_config(config)
                args = list(config_args) + list(args or sys.argv[1:])
        namespace = self._argparse(args=args, namespace=namespace)
        return namespace
