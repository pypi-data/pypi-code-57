# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neuralartstudio']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.5,<2.0.0',
 'pandas>=1.0.4,<2.0.0',
 'plotly>=4.8.1,<5.0.0',
 'streamlit>=0.61.0,<0.62.0',
 'torch>=1.5.0,<2.0.0',
 'torchvision>=0.6.0,<0.7.0']

entry_points = \
{'console_scripts': ['fix = scripts:fix']}

setup_kwargs = {
    'name': 'neuralartstudio',
    'version': '0.1.0',
    'description': 'App for experimenting and creating your own art using neural style transfer',
    'long_description': '[![pypi neuralartstudio version](https://img.shields.io/pypi/v/neuralartstudio.svg)](https://pypi.python.org/pypi/neuralartstudio)\n[![Conda neuralartstudio version](https://img.shields.io/conda/v/neuralartstudio/neuralartstudio.svg)](https://anaconda.org/neuralartstudio/neuralartstudio)\n[![neuralartstudio python compatibility](https://img.shields.io/pypi/pyversions/neuralartstudio.svg)](https://pypi.python.org/pypi/neuralartstudio)\n[![neuralartstudio license](https://img.shields.io/pypi/l/neuralartstudio.svg)](https://pypi.python.org/pypi/neuralartstudio)\n\n[![latest release date](https://img.shields.io/github/release-date/soumendra/neuralartstudio.svg)](https://pypi.python.org/pypi/neuralartstudio)\n[![latest release version](https://img.shields.io/github/release/soumendra/neuralartstudio.svg)](https://pypi.python.org/pypi/neuralartstudio)\n[![issue count](https://img.shields.io/github/issues-raw/soumendra/neuralartstudio.svg)](https://pypi.python.org/pypi/neuralartstudio)\n[![open pr count](https://img.shields.io/github/issues-pr-raw/soumendra/neuralartstudio.svg)](https://pypi.python.org/pypi/neuralartstudio)\n[![last commit at](https://img.shields.io/github/last-commit/soumendra/neuralartstudio.svg)](https://pypi.python.org/pypi/neuralartstudio)\n[![contributors count](https://img.shields.io/github/contributors/soumendra/neuralartstudio.svg)](https://pypi.python.org/pypi/neuralartstudio)\n\n# Getting started\n\nLatest docs at https://neuralartstudio.readthedocs.io/en/latest/\n\nInstall `neuralartstudio`\n\n```bash\npip install neuralartstudio\n```\n\n- It is possible to create meaningful output with a cpu.\n- A gpu can speed up the experiments.\n\n## Running as a streamlit app\n\nCreate a `streamlit` app (say in a file called `main.py`)\n\n```python\nfrom neuralartstudio.streamlit import neural_style_transfer\n\nneural_style_transfer(\n    contentpath="assets/dancing.jpg", stylepath="assets/picasso.jpg",\n)\n```\n\n**Note**: You have to provide paths to your content and style image to start with. You can replace the content image later in the app.\n\nThat\'s it. Now run the app with streamlit\n\n```bash\nstreamlit run main.py\n```\n\n## Running from a python program\n\n**ToDo**\n\n## Running in a Jupyter notebook\n\n**ToDo**\n',
    'author': 'Soumendra Dhanee',
    'author_email': 'soumendra@gmail.com',
    'maintainer': 'Soumendra Dhanee',
    'maintainer_email': 'soumendra@gmail.com',
    'url': 'https://github.com/soumendra/neuralartstudio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
