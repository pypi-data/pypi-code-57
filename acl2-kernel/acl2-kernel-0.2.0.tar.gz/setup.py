# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acl2_kernel']

package_data = \
{'': ['*']}

install_requires = \
['ipykernel>=5.3.0,<6.0.0',
 'ipython>=7.15.0,<8.0.0',
 'jupyter_client>=6.1.3,<7.0.0',
 'pexpect>=4.8.0,<5.0.0']

setup_kwargs = {
    'name': 'acl2-kernel',
    'version': '0.2.0',
    'description': 'Jupyter Kernel for ACL2',
    'long_description': '# acl2-kernel [![PyPI](https://img.shields.io/pypi/v/acl2-kernel)](https://pypi.org/project/acl2-kernel/) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/tani/acl2-kernel/master?filepath=Example.ipynb)\n\nJupyter Kernel for ACL2\n\n## What is Jupyter and ACL2?\n\n> Project Jupyter exists to develop open-source software, open-standards, and services for interactive computing across dozens of programming languages. (https://jupyter.org/)\n\n> ACL2 is a logic and programming language in which you can model computer systems, together with a tool to help you prove properties of those models. "ACL2" denotes "A Computational Logic for Applicative Common Lisp". (http://www.cs.utexas.edu/users/moore/acl2/)\n\n## Usage\n\n```sh\n$ pip3 install jupyter acl2-kernel\n$ python3 -m acl2_kernel.install\n$ jupyter noteboook\n```\n\nA running example is available in the `example/` directory.\nYou can try it on [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/tani/acl2-kernel/master?filepath=Example.ipynb).\n\n## Related Projects\n\n- [Jupyter](https://jupyter.org/) - Softwares for interactive computing\n- [ACL2](http://www.cs.utexas.edu/users/moore/acl2/) - Theorem prover based on Common Lisp\n\n## License\n\nThis project is released under the BSD 3-clause license.\n\nCopyright (c) 2020, TANIGUCHI Masaya All rights reserved.\n\nWe borrow code from the following projects.\n\n- Egison Kernel; Copyright (c) 2017, Satoshi Egi and contributors All rights reserved.\n- Bash Kernel; Copyright (c) 2015, Thomas Kluyver and contributors All rights reserved.\n',
    'author': 'TANIGUCHI Masaya',
    'author_email': 'mew@cat.ovh',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tani/acl2-kernel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
