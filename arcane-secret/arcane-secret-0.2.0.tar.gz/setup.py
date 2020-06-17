# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcane']

package_data = \
{'': ['*']}

install_requires = \
['pycryptodome>=3.9.7,<4.0.0']

setup_kwargs = {
    'name': 'arcane-secret',
    'version': '0.2.0',
    'description': 'A package to encode or decode tokens',
    'long_description': "# Arcane secret\nThis package allows to encode and decode secrets.\n\n## Get Started\n\n```sh\npip install arcane-secret\n```\n\n## Example Usage\n\n```python\nfrom arcane.secret import decode\n\ndecoded_secret = decode('secret', 'path_to_secret_key_file')\n```\n\nor\n\n```python\nfrom arcane.secret import encode\n\n# Import your configs\nfrom configure import Config\n\nencoded_secret = encode(secret, Config.SECRET_KEY_FILE)\n```\n",
    'author': 'Arcane',
    'author_email': 'product@arcane.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
