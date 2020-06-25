# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytezos',
 'pytezos.michelson',
 'pytezos.operation',
 'pytezos.repl',
 'pytezos.rpc',
 'pytezos.standards',
 'pytezos.tools']

package_data = \
{'': ['*']}

install_requires = \
['base58>=1.0.3,<2.0.0',
 'fastecdsa>=1.7.1,<2.0.0',
 'fire',
 'loguru',
 'mnemonic',
 'netstruct',
 'pendulum',
 'ply',
 'pyblake2>=1.1.2,<2.0.0',
 'pysodium>=0.7.1,<0.8.0',
 'pyyaml',
 'requests>=2.21.0,<3.0.0',
 'secp256k1>=0.13.2,<0.14.0',
 'simplejson',
 'tqdm']

entry_points = \
{'console_scripts': ['pytezos = pytezos:cli.main']}

setup_kwargs = {
    'name': 'pytezos',
    'version': '2.5.1',
    'description': 'Python toolkit for Tezos',
    'long_description': "# PyTezos\n\n[![PyPI version](https://badge.fury.io/py/pytezos.svg?)](https://badge.fury.io/py/pytezos)\n[![Build Status](https://travis-ci.org/baking-bad/pytezos.svg?branch=master)](https://travis-ci.org/baking-bad/pytezos)\n[![Docker Build Status](https://img.shields.io/docker/cloud/build/bakingbad/pytezos)](https://hub.docker.com/r/bakingbad/pytezos)\n[![Made With](https://img.shields.io/badge/made%20with-python-blue.svg?)](https://www.python.org)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\nPython SDK for Tezos:\n* RPC query engine\n* Cryptography\n* Building and parsing operations\n* Smart contract interaction\n* Local forging/packing & vice versa\n* Working with Michelson AST\n\nPyTezos CLI:\n* Generating contract parameter/storage schema\n* Activating and revealing accounts\n* Deploying contracts (+ GitHub integration)\n\nMichelson REPL:\n* Builtin interpreter (reimplemented)\n* Set of extra helpers (stack visualization, blockchain context mocking)\n\nMichelson integration testing framework:\n* Writing integration tests using `unittest` package\n* Simulating contract execution using remote intepreter (via RPC) or builtin one\n\n### Requirements\n\n* git\n* python 3.6+\n* pip 19.0.1+\n\nYou will also probably need to install several cryptographic packets.\n\n#### Linux\n\nUse apt or your favourite package manager:\n```\n$ sudo apt install libsodium-dev libsecp256k1-dev libgmp-dev\n```\n\n#### MacOS\n\nUse homebrew:\n```\n$ brew tap cuber/homebrew-libsecp256k1\n$ brew install libsodium libsecp256k1 gmp\n```\n\n#### Windows\n\nThe recommended way is to use WSL and then follow the instructions for Linux,\nbut if you feel lucky you can try to install natively:\n\n1. Install MinGW from [https://osdn.net/projects/mingw/](https://osdn.net/projects/mingw/)\n2. Make sure `C:\\MinGW\\bin` is added to your `PATH`\n3. Download the latest libsodium-X.Y.Z-msvc.zip from [https://download.libsodium.org/libsodium/releases/](https://download.libsodium.org/libsodium/releases/).\n4. Extract the Win64/Release/v143/dynamic/libsodium.dll from the zip file\n5. Copy libsodium.dll to C:\\Windows\\System32\\libsodium.dll\n\n### Installation\n\n```\n$ pip install pytezos\n```\n\n#### Google Colab\n\n`````python\n>>> !apt install libsodium-dev libsecp256k1-dev libgmp-dev\n>>> !pip install pytezos\n`````\n\n#### Docker container\nVerified & minified images for CI/CD https://hub.docker.com/r/bakingbad/pytezos/tags\n```\ndocker pull bakingbad/pytezos\n```\n\n### Quick start\nRead [quick start guide](https://pytezos.baking-bad.org/quick_start.html)\n\n### API reference\nCheck out a complete [API reference](https://pytezos.baking-bad.org)\n\n#### Inline documentation\nIf you are working in Jupyter/Google Colab or any other interactive console, \nyou can display documentation for a particular class/method:\n\n```python\n>>> from pytezos import pytezos\n>>> pytezos\n<pytezos.client.PyTezosClient object at 0x7f904cf339e8>\n\nProperties\n.key  # tz1grSQDByRpnVs7sPtaprNZRp531ZKz6Jmm\n.shell  # https://tezos-dev.cryptonomic-infra.tech/ (alphanet)\n\nHelpers\n.account()\n.activate_account()\n.ballot()\n.contract()\n.delegation()\n.double_baking_evidence()\n.double_endorsement_evidence()\n.endorsement()\n.operation()\n.operation_group()\n.origination()\n.proposals()\n.reveal()\n.seed_nonce_revelation()\n.transaction()\n.using()\n```\n\n### Publications\n\n* Pytezos 2.0 release with embedded docs and smart contract interaction engine  \nhttps://medium.com/coinmonks/high-level-interface-for-michelson-contracts-and-not-only-7264db76d7ae\n\n* Materials from TQuorum:Berlin workshop - building an app on top of PyTezos and ConseilPy  \nhttps://medium.com/coinmonks/atomic-tips-berlin-workshop-materials-c5c8ee3f46aa\n\n* Materials from the EETH hackathon - setting up a local development infrastructure, deploying and interacting with a contract  \nhttps://medium.com/tezoscommons/preparing-for-the-tezos-hackathon-with-baking-bad-45f2d5fca519\n\n* Introducing integration testing engine  \nhttps://medium.com/tezoscommons/testing-michelson-contracts-with-pytezos-513718499e93\n\n### Additional materials\n\n* Interacting with FA1.2 contract by TQTezos  \nhttps://assets.tqtezos.com/token-contracts/1-fa12-lorentz#interactusingpytezos\n* Deploying a contract by Vadim Manaenko  \nhttps://blog.aira.life/tezos-dont-forget-the-mother-console-fd2001261e50\n\n### Michelson test samples\n\n* In this repo  \nhttps://github.com/baking-bad/pytezos/tree/master/examples\n* Atomex (atomic swaps aka cross-chain transactions)  \nhttps://github.com/atomex-me/atomex-michelson/blob/master/tests/test_atomex.py\n* Atomex for FA1.2 (includes cross-contract interaction and views)  \nhttps://github.com/atomex-me/atomex-fa12-ligo/tree/master/tests\n* MultiAsset implementation tests (in a sandbox environment)  \nhttps://github.com/tqtezos/smart-contracts/tree/master/multi_asset/tezos_mac_tests\n\n### Contact\n* Telegram chat: [@baking_bad_chat](https://t.me/baking_bad_chat)\n* Slack channel: [#baking-bad](https://tezos-dev.slack.com/archives/CV5NX7F2L)\n\n### About\nThe project was initially started by Arthur Breitman, now it's maintained by Baking Bad team.\nPyTezos development is supported by Tezos Foundation.\n",
    'author': 'Michael Zaikin',
    'author_email': 'mz@baking-bad.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://baking-bad.github.io/pytezos/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
