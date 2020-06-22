"""
Copyright (c) 2019, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

from katena_chain_sdk_py.crypto.ed25519.private_key import PrivateKey


class TxSigner:
    # TxSigner contains all information about a Tx signer.

    def __init__(self, fqid: str, private_key: PrivateKey):
        self.fqid = fqid
        self.private_key = private_key

    def get_key_id(self) -> str:
        return self.fqid

    def get_private_key(self) -> PrivateKey:
        return self.private_key
