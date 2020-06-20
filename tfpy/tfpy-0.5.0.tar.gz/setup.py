# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tfpy', 'tfpy.core']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.4.1,<0.5.0',
 'pyyaml>=5.3.1,<6.0.0',
 'terraformpy==1.3.0',
 'typer>=0.2.1,<0.3.0']

entry_points = \
{'console_scripts': ['tfpy = tfpy.main:app']}

setup_kwargs = {
    'name': 'tfpy',
    'version': '0.5.0',
    'description': 'Create Terraform resources using Python',
    'long_description': 'tfpy\n====\n\n.. image:: https://github.com/rgreinho/tfpy/workflows/ci/badge.svg\n   :target: https://github.com/rgreinho/tfpy/actions?query=workflow%3Aci\n\n.. image:: https://badge.fury.io/py/tfpy.svg\n   :target: https://badge.fury.io/py/tfpy\n\nCreate Terraform resources using Python.\n\nDescription\n-----------\n\n``tfpy`` is a thin wrapper around `terraformpy`_, aiming at providing a well defined\nstructure to organize your `terraform`_ stacks and leverage the power of Python to\ndefine them rather than using `HCL`_.\n\nThe goal is to have a repository layout inspired from `Ansible <https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html#directory-layout>`_\nwhere the stacks are driven by the variables.\n\nFor more information regarding how to create your stacks, please refer to the official\n`terraformpy`_ documentation.\n\nInstallation\n------------\n\ntfpy requires Python 3.7+ to work\n\n::\n\n  pip install tfpy\n\nUsage\n-----\n\nThe ``tfpy`` command needs to be run at the root of your project.\n\nThe output will be created in a new subfolder within your project, named ``generated``.\nFor instance ``generated/gke/production/main.tf.json``\n\nProject layout\n^^^^^^^^^^^^^^\n\n::\n\n  .\n  ├── generated\n  │\xa0\xa0 └── commerce\n  │\xa0\xa0     └── staging\n  │\xa0\xa0         └── main.tf.json\n  ├── library\n  │\xa0\xa0 ├── backend.py\n  │\xa0\xa0 └── provider.py\n  ├── stacks\n  │\xa0\xa0 └── commerce\n  │\xa0\xa0     ├── README.md\n  │\xa0\xa0     ├── gke.tf.py\n  │\xa0\xa0     └── terraform.tf.py\n  └── vars\n      ├── all\n      │\xa0\xa0 ├── cartigan.yml\n      │\xa0\xa0 └── config.yml\n      └── staging\n          └── commerce\n              ├── gke.yml\n              └── project.yml\n\n* ``generated``: folder where the stack are stored as JSON once generated.\n* ``library``: folder where you can place custom functions.\n* ``stacks``: the stacks created using TerraformPy.\n* ``vars``: the variables used to create the stacks.\n\nExamples\n^^^^^^^^\n\nBuild a project stack without an environment::\n\n  tfpy generate organization\n\nBuild a project stack for a specific environment::\n\n  tfpy generate gke production\n\n\n.. _HCL: https://github.com/hashicorp/hcl\n.. _terraform: https://www.terraform.io\n.. _terraformpy: https://github.com/NerdWalletOSS/terraformpy\n',
    'author': 'Rémy Greinhofer',
    'author_email': 'remy.greinhofer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://rgreinho.github.io/tfpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
