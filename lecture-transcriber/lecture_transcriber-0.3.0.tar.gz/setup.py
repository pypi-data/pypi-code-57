# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lecture_transcriber']

package_data = \
{'': ['*']}

install_requires = \
['deepsegment==2.3.0',
 'deepspeech==0.6.1',
 'pydub==0.23.1',
 'sox==1.3.7',
 'tensorflow>=2.2.0,<3.0.0',
 'tqdm==4.43.0']

setup_kwargs = {
    'name': 'lecture-transcriber',
    'version': '0.3.0',
    'description': 'A DeepSpeech-based transcriber using DeepSegment to separate sentences in a long audio recording.',
    'long_description': None,
    'author': 'Harrison Morgan',
    'author_email': 'harrison.morgan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
