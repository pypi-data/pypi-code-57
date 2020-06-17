# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poethepoet']

package_data = \
{'': ['*']}

install_requires = \
['pastel>=0.2.0,<0.3.0', 'poetry>=1.0.5,<2.0.0', 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['poe = poethepoet:main']}

setup_kwargs = {
    'name': 'poethepoet',
    'version': '0.2.0',
    'description': 'A task runner that works well with poetry.',
    'long_description': '************\nPoe the Poet\n************\n\nA task runner that works well with poetry.\n\n.. role:: bash(code)\n   :language: bash\n\n.. role:: toml(code)\n   :language: toml\n\nFeatures\n========\n\n- Straight foward declaration of project tasks in your pyproject.toml (kind of like npm\n  scripts)\n- Task are run in poetry\'s virtualenv by default\n- Short and sweet commands with extra arguments passed to the task\n  :bash:`poe [options] task [task_args]`\n- tasks can reference environmental variables as if they were evaluated by a shell\n\nInstallation\n============\n\nInto your project (so it works inside poetry shell):\n\n.. code-block:: bash\n\n  poetry add --dev poethepoet\n\nAnd into your default python environment (so it works outside of poetry shell)\n\n.. code-block:: bash\n\n  pip install poethepoet\n\nBasic Usage\n===========\n\nDefine tasks in your pyproject.toml\n-----------------------------------\n\n`See a real example <https://github.com/nat-n/poethepoet/blob/master/pyproject.toml>`_\n\n.. code-block:: toml\n\n  [tool.poe.tasks]\n  test = "pytest --cov=poethepoet"\n\nRun tasks with the poe cli\n--------------------------\n\n.. code-block:: bash\n\n  poe test\n\nAdditional argument are passed to the task so\n\n.. code-block:: bash\n\n  poe test -v tests/favorite_test.py\n\nresults in the following be run inside poetry\'s virtualenv\n\n.. code-block:: bash\n\n  pytest --cov=poethepoet -v tests/favorite_test.py\n\nYou can also run it like so if you fancy\n\n.. code-block:: bash\n\n  python -m poethepoet [options] task [task_args]\n\nOr install it as a dev dependency with poetry and run it like\n\n.. code-block:: bash\n\n  poetry add --dev poethepoet\n  poetry run poe [options] task [task_args]\n\nThough it that case you might like to do :bash:`alias poe=\'poetry run poe\'`.\n\nAdvanced usage\n==============\n\nRun poe from anywhere\n---------------------\n\nBy default poe will detect when you\'re inside a project with a pyproject.toml in the\nroot. However if you want to run it from elsewhere that is supported too by using the\n`--root` option to specify an alternate location for the toml file.\n\nBy default poe will set the working directory to run tasks. If you want tasks to inherit\nthe working directory from the environment that you disable this by setting the\nfollowing in your pyproject.toml.\n\n.. code-block:: toml\n\n  [tool.poe]\n  run_in_project_root = false\n\nIn all cases the path to project root (where the pyproject.toml resides) is be available\nas `$POE_ROOT` within the command line and process.\n\nContributing\n============\n\nDon\'t delay, create an issue today!\n\nTODO\n====\n\n* support "script" tasks defined as references to python functions\n* task composition/aliases\n* support declaring specific arguments for a task\n* support documenting tasks\n* support running tasks outside of poetry\'s virtualenv (or in another?)\n* maybe try work well without poetry too\n\nLicence\n=======\n\nMIT. Go nuts.\n',
    'author': 'Nat Noordanus',
    'author_email': 'n@natn.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nat-n/poethepoet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
