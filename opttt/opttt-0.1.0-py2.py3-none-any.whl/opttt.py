# (c) Copyright 2020 Trent Hauck
# All Rights Reserved
"""Main entrypoint for opttt."""

import argparse
import sys

import pydantic


def _add_fields_to_parser(obj, parser):
    for field_name, field in obj.__fields__.items():

        extra = field.field_info.extra

        if field.required and "env" not in extra:
            parser.add_argument(field.alias, type=field.type_, help=field.field_info.description)
        else:
            parser.add_argument(
                f"--{field.alias}",
                type=field.type_,
                help=field.field_info.description,
                default=field.default,
            )


class Opttt(pydantic.BaseSettings):
    @classmethod
    def from_args(cls, arguments=sys.argv[1:]):

        if hasattr(cls, "Config"):
            description = cls.Config.description
        else:
            description = None

        parser = argparse.ArgumentParser(description=description)

        _add_fields_to_parser(cls, parser)

        arguments = parser.parse_args(arguments)
        return cls.parse_obj(vars(arguments))
