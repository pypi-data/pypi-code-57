"""
Copyright (c) 2019, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""


class BaseKey:
    # BaseKey holds a binary key.

    def __init__(self, key: bytes):
        self.key = key

    def get_key(self) -> bytes:
        return self.key
