# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['cli_box']
install_requires = \
['strip-ansi>=0.1.1,<0.2.0', 'wcwidth>=0.2.4,<0.3.0']

setup_kwargs = {
    'name': 'cli-box',
    'version': '0.2.0',
    'description': 'Add a box around your text for prettier CLIs',
    'long_description': '# box\n\n> Add a box around your text for prettier CLIs\n\n## Installation\n\n```sh-session\npip install cli-box\n```\n\n## Usage\n\n```python\n>>> import cli_box\n>>> print(cli_box.rounded("""Lorem ipsum\n... dolor sit amet.\n... """))\n╭─────────────────╮\n│   Lorem ipsum   │\n│ dolor sit amet. │\n╰─────────────────╯\n```\n',
    'author': 'Ewen Le Bihan',
    'author_email': 'ewen.lebihan7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ewen-lbh/python-cli-box',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
