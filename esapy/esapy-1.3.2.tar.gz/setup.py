# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['esapy']

package_data = \
{'': ['*']}

install_requires = \
['gitpython', 'ipython>=6', 'pyyaml', 'requests']

entry_points = \
{'console_scripts': ['esa = esapy.entrypoint:main']}

setup_kwargs = {
    'name': 'esapy',
    'version': '1.3.2',
    'description': 'A python implementation of esa.io API',
    'long_description': '# esapy\n\nA python implementation of esa.io API\n\nThe main purpose of this package is implementation of easy uploading and sharing jupyter notebook to esa.io service.\n\n\n[![PyPI version](https://badge.fury.io/py/esapy.svg)](https://badge.fury.io/py/esapy) [![Python Versions](https://img.shields.io/pypi/pyversions/esapy.svg)](https://pypi.org/project/esapy/)\n[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)\n\nDescription in Japanese: <https://esa-pages.io/p/sharing/14661/posts/184/d983bd2e71ad35528500.html>\n\n\n## INSTALATION\n\n1. Install pandoc\n\n    ```shell\n    $sudo apt install pandoc\n    ```\n\n    This package call nbconvert internally.\n\n1. Install package\n\n    ```shell\n    $pip install esapy\n    ```\n\n1. generate esa.io token with read/write permission.\n\n1. make configuration file in your home directory (`~/.esapyrc`).\n\n    ```YAML: ~/.esapyrc\n    token: your_token\n    team: your_team\n    ```\n\n    - You can set them as environment variables: `ESA_PYTHON_TOKEN`, `ESA_PYTHON_TEAM`.\n    - Environment variables are prior to `.esapyrc` file.\n    - You can check your token using `esa config` from command line. \n\n\n\n## HOW TO USE\n\n1. Prepare .ipynb file\n\n1. Convert to markdown and upload images.\n\n    ```shell\n    $ esa up target.ipynb\n    ```\n\n    This package uploads images, and uploads markdown file as a new post or update the previously uploaded post.\n\n1. access the new post and edit.\n\n1. if process fails due to a network problem, you can check by `esa stats`.\n\n\n## DOCUMENT\n\n### commands\nThis package registers following command line tools.\n\n- `esa up <input_filepath>`\n  - upload your file\n  - supported format: ipynb, tex, and md\n\n- `esa config`\n  - list environs and config\n\n- `esa stats`\n  - show statistics of your team\n  - This command can be used for access test.\n\n- `esa reset <target.ipynb> [--number <post_number>]`\n  - remove upload history by esapy in notebook file\n  - new post_number can be assigned\n\n- `esa ls <dirname>`\n  - show notebook list in the directory\n  - `<dirname>` can be abbreveated. Default is the current working directory.\n\n### config file\nThe config file (`~/.esapyrc`) should be written in yaml format.\nAn example is shown below.\n```yaml: ~/.esapyrc\ntoken: your_token\nteam: your_team\n```\n\n\n## INSTALLATION for DEVELOPMENT\n\n1. setup poetry on your environment\n1. clone this repository\n1. cd repo directory\n1. `poetry install`\n1. `git checkout develop`\n\n## LICENSE\nCopyright (c) 2020 Kosuke Mizuno  \nThis package is released under the MIT license (see [LICENSE](LICENSE) file).\n',
    'author': 'Kosuke Mizuno',
    'author_email': 'dotmapu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/KosukeMizuno/esapy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4',
}


setup(**setup_kwargs)
