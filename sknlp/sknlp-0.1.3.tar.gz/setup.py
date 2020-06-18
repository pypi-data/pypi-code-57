# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sknlp',
 'sknlp.callbacks',
 'sknlp.data',
 'sknlp.data.text_segmenter',
 'sknlp.layers',
 'sknlp.metrics',
 'sknlp.module',
 'sknlp.module.classifiers',
 'sknlp.module.text2vec',
 'sknlp.typing',
 'sknlp.utils',
 'sknlp.vocab']

package_data = \
{'': ['*']}

install_requires = \
['jieba_fast>=0.53,<0.54',
 'joblib>=0.14.1,<0.15.0',
 'pandas==1.0.4',
 'sklearn>=0.0,<0.1',
 'tabulate>=0.8.6,<0.9.0',
 'tensorflow-text>=2.2.0,<3.0.0',
 'tensorflow>=2.2.0,<3.0.0',
 'tf-models-official>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'sknlp',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'nanaya',
    'author_email': 'nanaya100@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
