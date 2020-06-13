# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ccpp',
 'ccpp.ccpp-tmpl.{{ cookiecutter.repo }}.tests',
 'ccpp.ccpp-tmpl.{{ cookiecutter.repo }}.{{ cookiecutter.repo_src }}']

package_data = \
{'': ['*'], 'ccpp': ['ccpp-tmpl/*', 'ccpp-tmpl/{{ cookiecutter.repo }}/*']}

install_requires = \
['cookiecutter>=1.7.2,<2.0.0', 'fire>=0.3.1,<0.4.0', 'poetry>=1.0.9,<2.0.0']

entry_points = \
{'console_scripts': ['ccpp = ccpp.main:main']}

setup_kwargs = {
    'name': 'ccpp',
    'version': '0.1.4',
    'description': 'Cookiecutter template for Python package',
    'long_description': '<p align="center">\n  <a href="https://github.com/guaifish/ccpp"><img src="https://github.com/guaifish/ccpp/blob/master/img/ccpp-logo.png" alt="ccpp"></a>\n</p>\n<p align="center">\n    <em>Cookiecutter template for Python package</em>\n</p>\n<p align="center">\n<a href="https://pypi.org/project/ccpp" target="_blank">\n    <img src="https://badge.fury.io/py/ccpp.svg" alt="Package version">\n</a>\n<a href="https://github.com/guaifish/ccpp/blob/master/LICENSE" target="_blank">\n    <img src="https://img.shields.io/github/license/guaifish/ccpp" alt="GitHub LICNESE">\n</a>\n<a href="https://github.com/guaifish/ccpp/stargazers" target="_blank">\n    <img src="https://img.shields.io/github/stars/guaifish/ccpp?logo=github" alt="GitHub Stars">\n</a>\n<a href="https://github.com/guaifish/ccpp/network/members" target="_blank">\n    <img src="https://img.shields.io/github/forks/guaifish/ccpp?logo=github" alt="GitHub Forks">\n</a>\n</p>\n\n---\n\n## Requirements\n\n* Python 3.6+\n\n* [cookiecutter](https://github.com/cookiecutter/cookiecutter) - template engine\n* [poetry](https://github.com/python-poetry/poetry) - dependency management\n* [python-fire](https://github.com/google/python-fire) - command line tool\n\n## Installation\n\n```console\n$ pip install ccpp\n```\n\n## Usage\n\n### Create a new package\n\n```console\n$ ccpp new hello-world && cd hello-world\n```\n\n### Test the package at the first time\n\n```console\n$ pytest tests\n```\n\n### Building package\n\n```console\n$ poetry build\n\nBuilding hello-world (0.1.0)\n - Building sdist\n - Built hello-world-0.1.0.tar.gz\n\n - Building wheel\n - Built hello-world-0.1.0-py3-none-any.whl\n```\n\n### Publishing package to PyPI\n\n```console\n$ poetry publish\n\nPublishing hello-world (0.1.0) to PyPI\nUsername: guaifish\nPassword:\n - Uploading hello-world-0.1.0-py3-none-any.whl 0%\n - Uploading hello-world-0.1.0-py3-none-any.whl 65%\n - Uploading hello-world-0.1.0-py3-none-any.whl 100%\n - Uploading hello-world-0.1.0-py3-none-any.whl 100%\n - Uploading hello-world-0.1.0.tar.gz 0%\n - Uploading hello-world-0.1.0.tar.gz 83%\n - Uploading hello-world-0.1.0.tar.gz 100%\n - Uploading hello-world-0.1.0.tar.gz 100%\n```\n\n## License\n\nCopyright © 2020 [guaifish](https://github.com/guaifish).\nThis project is [MIT](https://github.com/guaifish/ccpp/blob/master/LICENSE) license.',
    'author': 'guaifish',
    'author_email': 'guaifish@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/guaifish/ccpp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
