# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['hist_navigator']
install_requires = \
['prompt-toolkit', 'xonsh>=0.9.17']

setup_kwargs = {
    'name': 'xontrib-hist-navigator',
    'version': '0.4.1',
    'description': "A Xonsh plugin to navigate between directories like fish's prevd/nextd",
    'long_description': '# xontrib-hist-navigator\n\nFish-shell like `prevd` and `nextd` for [xonsh](https://github.com/xonsh/xonsh/) with keyboard shortcuts\n\n# Usage\n\n- install using pip \n```sh\npip install xontrib-hist-navigator\n```\n\n- or xpip (that is installed alongside xonsh)\n```sh\nxpip install xontrib-hist-navigator\n```\n\n- add to list of xontribs loaded.\n```sh\nxontrib load hist_navigator\n```\n\n# Overview\n\n- it keeps track of `cd` usage per session\n- `nextd` -> move to previous working directory (`Alt + Left Arrow`)\n- `prevd` -> move to next working directory in the history (`Alt + Right Arrow`), if `prevd` is used.\n',
    'author': 'Noortheen Raja',
    'author_email': 'jnoortheen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/xontrib-hist-navigator',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
