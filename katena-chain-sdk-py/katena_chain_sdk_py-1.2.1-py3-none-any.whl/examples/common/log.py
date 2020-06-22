"""
Copyright (c) 2019, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

import typing

from katena_chain_sdk_py.serializer.base_schema import BaseSchema


def println_json(data: any, schema: typing.Type[BaseSchema], is_array: bool = False):
    print(schema().dumps(data, indent=2, many=is_array))
    print()
