# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nndict']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nndict',
    'version': '1.0.0',
    'description': 'A dict that does not support None entries. Silently deletes entry if updated to null and works recursively.',
    'long_description': None,
    'author': 'Tiago Santos',
    'author_email': 'tiago.santos@vizidox.com',
    'maintainer': 'Sara Pereira',
    'maintainer_email': 'sara.pereira@vizidox.com',
    'url': 'https://github.com/Morphotech/NeverNoneDict',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
