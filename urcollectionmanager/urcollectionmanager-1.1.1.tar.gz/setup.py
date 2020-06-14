# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['urcollectionmanager']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'requests>=2.23.0,<3.0.0', 'sqlalchemy>=1.3.15,<2.0.0']

setup_kwargs = {
    'name': 'urcollectionmanager',
    'version': '1.1.1',
    'description': 'API for Urban Rivals collection management',
    'long_description': "Urban Rivals Collection Management API (urcollectionmanager)\n============================================================\n\nA module to support reading player purchase history data and\nstoring it in a database.\n\nPuchases History Use:\n    #) Import `api` from `urcollectionmanager`\n    #) Create a request.Session and pass it, along with\n       your credentials to `session_connect_to_ur`\n    #) Pass that same session (now authenticated) to\n       `get_purchase_history` along with the number of\n       pages to scrape.\n    #) Pass the result to `convert_purchase_history`\n\n        Optionally: Pass result to your own HTML parser.\n\n    #) You now have a list of Purchase objects that contain\n       all relevant information available from the purchase\n       history page.\n\nMissions Use:\n    #) Import `api` from `urcollectionmanager`\n    #) Create a request.Session and pass it, along with\n       your credentials to `session_connect_to_ur`\n    #) Pass that same session (now authenticated) to\n       `get_missions_list` along with the mission category\n       to find. An empty string returns everything.\n    #) Pass the result to `convert_missions`\n\n        Optionally: Pass result to your own HTML parser.\n\n    #) You now have a list of Mission objects that contain\n       all relevent information available from the missions\n       page.\n\nDatabase Use:\n    #) Run `connect_and_initialize_database` if you have a\n       particular database location you want to connect to.\n       By default this will connect to `data/collection.sqlite`\n    #) Pass a list of Purchase objects to `write_history_to_database`\n\n        If using `convert_purchase_history`, you will need to flatten\n        the list of lists\n\n    #) Once the database has Purchase objects in it, you can\n       run `get_history_from_database` to retrieve them.\n\n    #) Similarly, you can run `write_missions_to_database` to write\n       Mission objects and `get_missions_from_database` to read mission\n       Mission objects from the same database as Purchases.\n\nDev\n---\nHow To Use Tools:\n    Poetry_\n        - To run the project (preferably configure venv first)\n\n        >>> poetry install\n\n        - To configure your venv\n\n        >>> python -m venv /path/to/new/virtual/environment\n        >>> poetry env info\n\n            - If `env info` does not match your path, try manually running \\\n              `Scripts/activate` inside that environment\n\n        - To add a dependency (add a -D if it's only for development)\n\n        >>> poetry add <dependency>\n\n    Commitizen_\n        >>> git add\n        >>> cz c\n\n    - More options can be found under options under Commitizen_\n\n    PreCommit_\n        Update .pre-commit-config.yaml, then run\n\n    >>> pre-commit install\n    >>> pre-commit run --all-files\n\n    - More hook plugins can be found at PreCommitHooks_\n\nTODO:\n\n- Use UR-API_ to collect player data. UR-API-Example_\n- Default to file output (excel or some form of that)\n- Testing (pytest, Coverage-py_)\n- Documentation (Sphinx_)\n\nNot Required at this Time:\n\n- Black_\n- iSort_\n\n.. _UR-API: https://www.urban-rivals.com/api/developer/\n.. _UR-API-Example: https://github.com/Buscatrufas/UrbanRivals/blob/master/index.php\n.. _Coverage-py: https://coverage.readthedocs.io/en/latest/config.html\n.. _Sphinx: https://www.sphinx-doc.org/en/master/\n.. _AutoPEP8: https://github.com/hhatto/autopep8#usage\n.. _Black: https://github.com/psf/black#version-control-integration\n.. _iSort: https://github.com/pre-commit/mirrors-isort\n.. _Commitizen: https://woile.github.io/commitizen/\n.. _PreCommit: https://pre-commit.com/\n.. _PreCommitHooks: https://pre-commit.com/hooks.html\n.. _Poetry: https://python-poetry.org/docs/cli/\n.. _PypiToken: https://pypi.org/help/#apitoken",
    'author': 'Brent Spector',
    'author_email': 'brent.spector@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brentspector/urcollectionmanager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
