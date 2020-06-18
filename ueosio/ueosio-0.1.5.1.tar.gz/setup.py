# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ueosio']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.0.0,<3.0.0', 'cryptos>=1.36,<2.0', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'ueosio',
    'version': '0.1.5.1',
    'description': 'uEOSIO python library',
    'long_description': '# µEOSIO\n**Python wrapper for EOSio**\n\nMicro EOSIO allows you to interact with any EOSio chain using Python.\n\n# Build\n\n    git clone https://github.com/AntarticaLabs/ueosio\n    cd ueosio\n    python3 -m venv venv\n    source venv/bin/activate\n    pip install -r examples/requirements.txt\n\n### Examples:\n\n[tx.py](/examples/tx.py): Send a transaction on any given chain.\n\n[keys.py](/examples/keys.py): Generate a key pair or get the public key of any given private key.\n\n[approve_multisig.py](/examples/approve_multisig.py): Approve a multisig transaction.\n\n[create_account.py](/examples/create_account.py): Create an account, buy ram and delegate bandwidth and CPU. \n\n_____\n\n\n[MIT License](LICENSE) \\\nCopyright (c) 2020 AntarticaLabs\n',
    'author': 'Matias Romeo',
    'author_email': 'matias.romeo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
