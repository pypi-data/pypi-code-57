# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spacy_fastlang']

package_data = \
{'': ['*']}

install_requires = \
['fasttext>=0.9.2,<0.10.0', 'spacy>=2.3.0,<3.0.0']

setup_kwargs = {
    'name': 'spacy-fastlang',
    'version': '0.4.2',
    'description': 'Language detection using FastText and Spacy',
    'long_description': '# spacy_fastlang\n\n## Install\n\nAssuming you have a working python environment, you can simply install it using\n\n```\npip install spacy_fastlang\n```\n\n## Usage\n\nThe library exports a pipeline component called `LanguageDetector` that will set two spacy extensions\n\n- doc.\\_.language = ISO code of the detected language or `xx` as a fallback\n- doc.\\_.language_score = confidence\n\n```\nfrom spacy_fastlang import LanguageDetector\nnlp = spacy.load("...")\nnlp.add_pipe(LanguageDetector())\ndoc = nlp(en_text)\n\ndoc._.language == "..."\ndoc._.language_score >= ...\n```\n\n## Options\n\n[Check the tests](./tests/test_spacy_fastlang.py) to see more examples and available options\n\n## License\n\nEverythin is under `MIT` except the default model which is distributed under [Creative Commons Attribution-Share-Alike License 3.0](https://creativecommons.org/licenses/by-sa/3.0/) by facebook [here](https://fasttext.cc/docs/en/language-identification.html)\n',
    'author': 'Thomas Thiebaud',
    'author_email': 'thiebaud.tom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thomasthiebaud/spacy-fastlang',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
