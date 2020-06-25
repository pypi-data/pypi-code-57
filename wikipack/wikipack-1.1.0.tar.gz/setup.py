# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wikipack',
 'wikipack.commands',
 'wikipack.events',
 'wikipack.stars',
 'wikipack.tables']

package_data = \
{'': ['*']}

install_requires = \
['royalnet[alchemy_easy,constellation]>=5.9.0,<5.10.0']

setup_kwargs = {
    'name': 'wikipack',
    'version': '1.1.0',
    'description': 'A Wiki for Royalnet',
    'long_description': '# `wikipack`\n\nThis pack adds a small Wiki to Royalnet, allowing communities to create their own small Wikis.\n\n## Configuration options\n\n```toml\n[Packs."wikipack"]\n\n# The roles that are authorized by default to complete certain actions.\n# Setting them to * disables the authentication requirement, allowing unauthenticated users that privilege\n[Packs."wikipack".roles]\n\n# Users with this role will be able to view wiki pages that do not have a different role set.\nview = "*"\n\n# Users with this role will be able to create new wiki pages.\ncreate = "wiki_create"\n\n# Users with this role will be able to edit wiki pages that do not have a different role set.\nedit = "wiki_edit"\n\n# Users with this role will be able to delete wiki pages.\ndelete = "wiki_delete"\n\n# Users with this role will override all other privileges.\nadmin = "wiki_admin"\n```\n',
    'author': 'Stefano Pigozzi',
    'author_email': 'ste.pigozzi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Steffo99/wikipack/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
