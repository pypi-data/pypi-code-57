# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poethepoet', 'poethepoet.task']

package_data = \
{'': ['*']}

install_requires = \
['clikit>=0.4.2,<0.5.0',
 'pastel>=0.2.0,<0.3.0',
 'poetry>=1.0.9,<2.0.0',
 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['poe = poethepoet:main']}

setup_kwargs = {
    'name': 'poethepoet',
    'version': '0.3.0',
    'description': 'A task runner that works well with poetry.',
    'long_description': '************\nPoe the Poet\n************\n\nA task runner that works well with poetry.\n\n.. role:: bash(code)\n   :language: bash\n\n.. role:: toml(code)\n   :language: toml\n\nFeatures\n========\n\n✅ Straight foward declaration of project tasks in your pyproject.toml (kind of like npm scripts)\n\n✅ Task are run in poetry\'s virtualenv by default\n\n✅ Tasks can be shell commands or references to python functions (like tool.poetry.scripts)\n\n✅ Short and sweet commands with extra arguments passed to the task :bash:`poe [options] task [task_args]`\n\n✅ Tasks can reference environmental variables as if they were evaluated by a shell\n\nInstallation\n============\n\nInto your project (so it works inside poetry shell):\n\n.. code-block:: bash\n\n  poetry add --dev poethepoet\n\nAnd into your default python environment (so it works outside of poetry shell)\n\n.. code-block:: bash\n\n  pip install poethepoet\n\nBasic Usage\n===========\n\nDefine tasks in your pyproject.toml\n-----------------------------------\n\n`See a real example <https://github.com/nat-n/poethepoet/blob/master/pyproject.toml>`_\n\n.. code-block:: toml\n\n  [tool.poe.tasks]\n  test       = "pytest --cov=poethepoet"                                # simple command based task\n  mksandwich = { script = "my_package.sandwich:build" }                 # python script based task\n  tunnel     = { shell = "ssh -N -L 0.0.0.0:8080:$PROD:8080 $PROD &" }  # shell script based task\n\nRun tasks with the poe cli\n--------------------------\n\n.. code-block:: bash\n\n  poe test\n\nAdditional argument are passed to the task so\n\n.. code-block:: bash\n\n  poe test -v tests/favorite_test.py\n\nresults in the following be run inside poetry\'s virtualenv\n\n.. code-block:: bash\n\n  pytest --cov=poethepoet -v tests/favorite_test.py\n\nYou can also run it like so if you fancy\n\n.. code-block:: bash\n\n  python -m poethepoet [options] task [task_args]\n\nOr install it as a dev dependency with poetry and run it like\n\n.. code-block:: bash\n\n  poetry add --dev poethepoet\n  poetry run poe [options] task [task_args]\n\nThough it that case you might like to do :bash:`alias poe=\'poetry run poe\'`.\n\nTypes of task\n=============\n\nThere are three types of task: simple commands (cmd), python scripts (script), and shell\nscripts (shell).\n\n- **Command tasks** contain a single command that will be executed without a shell.\n  This covers most basic use cases for example:\n\n  .. code-block:: toml\n\n    [tool.poe.tasks]\n    format = "black ."  # strings are interpreted as commands by default\n    clean = """\n    # Multiline commands including comments work too. Unescaped whitespace is ignored.\n    rm -rf .coverage\n           .mypy_cache\n           .pytest_cache\n           dist\n           ./**/__pycache__\n    """\n    lint = { "cmd": "pylint poethepoet" }  # Inline tables with a cmd key work too\n    greet = "echo Hello $USER"  # Environmental variables work, even though there\'s no shell!\n\n- **Script tasks** contain a reference to a python callable to import and execute, for\n  example:\n\n  .. code-block:: toml\n\n    [tool.poe.tasks]\n    fetch-assets = { "script" = "my_package.assets:fetch" }\n\n  If extra arguments are passed to task, then they will be available to the called python\n  function via `sys.argv`.\n\n- **Shell tasks** are similar to simple command tasks except that they are executed\n  inside a new shell, and can consist of multiple seperate commands, command\n  substitution, pipes, background processes, etc\n\n  An example use case for this might be opening some ssh tunnels in the background with\n  one task and closing them with another like so:\n\n  .. code-block:: toml\n\n    [tool.poe.tasks]\n    pfwd = { "shell" = "ssh -N -L 0.0.0.0:8080:$STAGING:8080 $STAGING & ssh -N -L 0.0.0.0:5432:$STAGINGDB:5432 $STAGINGDB &" }\n    pfwdstop = { "shell" = "kill $(pgrep -f "ssh -N -L .*:(8080|5432)")" }\n\n\nProject-wide configuration options\n==================================\n\nRun poe from anywhere\n---------------------\n\nBy default poe will detect when you\'re inside a project with a pyproject.toml in the\nroot. However if you want to run it from elsewhere that is supported too by using the\n`--root` option to specify an alternate location for the toml file.\n\nBy default poe will set the working directory to run tasks. If you want tasks to inherit\nthe working directory from the environment that you disable this by setting the\nfollowing in your pyproject.toml.\n\n.. code-block:: toml\n\n  [tool.poe]\n  run_in_project_root = false\n\nIn all cases the path to project root (where the pyproject.toml resides) is be available\nas `$POE_ROOT` within the command line and process.\n\nChange the default task type\n----------------------------\n\nBy default tasks defined as strings are interpreted as shell commands, and script tasks\nrequire the more verbose table syntax to specify. For example:\n\n.. code-block:: toml\n\n  my_cmd_task = "cmd args"\n  my_script_task = { "script" = "my_package.my_module:run" }\n\nThis behavoir can be reversed by setting the `default_task_type` option in your\npyproject.toml like so:\n\n.. code-block:: toml\n\n  [tool.poe]\n  default_task_type = "script"\n\n  [tool.poe.tasks]\n  my_cmd_task = { "cmd" = "cmd args" }\n  my_script_task = "my_package.my_module:run"\n\nContributing\n============\n\nThere\'s plenty to do, come say hi in the issues! 👋\n\nTODO\n====\n\n☐ task composition/aliases\n\n☐ support declaring specific arguments for a task\n\n☐ support documenting tasks\n\n☐ command line completion\n\n☐ support running tasks outside of poetry\'s virtualenv (or in another?)\n\n☐ maybe try work well without poetry too\n\nLicence\n=======\n\nMIT.\n',
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
