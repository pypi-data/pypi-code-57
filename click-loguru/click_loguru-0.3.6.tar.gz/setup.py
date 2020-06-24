# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['click_loguru']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'loguru>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'click-loguru',
    'version': '0.3.6',
    'description': 'Logging to stderr and file for click applications.',
    'long_description': 'click_loguru\n============\n``click_loguru`` initializes `loguru <https://github.com/Delgan/loguru/>`_\nfor logging to stderr and (optionally) a file for use\nwith a `click <https://click.palletsprojects.com/>`_ CLI.\n\nIf your click application uses subcommands (via ``@click.group()``),\nlog files will include the subcommand in the name.\nLog files are numbered, with a retention policy specified.  Log files can be enabled or disabled\nper-subcommand and written to a subdirectory your application specifies.  \n\nGlobal options control verbose, quiet, and logfile creation.  The values of these global\noptions are accessible from your application.\n\nInstantiation is from a single class, ``ClickLoguru``, with the arguments of the name and version\nof your application.  Optional keyworded arguments are the integer ``retention`` to set the number\nof log files retained per-application to values other than the default (4), ``log_dir_parent`` to\nset the location of the log file directory other than its default value of ``./logs``,\n``file_log_level`` to set the level of logging to the file other than the default of ``DEBUG``,\nand ``stderr_log_level`` which by default is set to ``INFO``.\n\nThe ``logging_options`` method returns a decorator to be used for the CLI method which defines\nthe global options that allows control of ``quiet``, ``verbose``, and ``logfile`` booleans.\n\nThe ``stash_subcommand`` method returns a decorator to be used for the CLI method for applications\nwhich define subcommands.\n\nThe ``init_logger`` method returns a decorator which must be used for each subcommand.   It allows\noverride of the default ``log_dir_parent`` established at instantiation, as well as turning\noff file logging for that command by setting ``logfile`` to ``False``.\n\nThe ``log_elapsed_time`` method returns a decorator which causes the elapsed time for the subcommand\nto be emitted at the ``DEBUG`` level.\n\nThe ``get_global_options`` method returns the context object associated with the global options.\nThe context object is printable.  The attributes of the context object are the booleans ``verbose``,\n``quiet``, and ``logfile``, the string ``subcommand`` showing the subcommand that was invoked,\nand ``logfile_handler_id`` if your code wishes to manipulate the handler directly.\n\nSee the file ``tests/__init__.py`` for usage examples.\n\nPrerequisites\n-------------\nPython 3.6 or greater is required.\nThis package is tested under Linux and MacOS using Python 3.7.\n\n\nProject Status\n--------------\n+-------------------+------------+\n| Latest Release    | |pypi|     |\n+-------------------+------------+\n| GitHub            | |repo|     |\n+-------------------+------------+\n| License           | |license|  |\n+-------------------+------------+\n| Travis Build      | |travis|   |\n+-------------------+------------+\n| Coverage          | |coverage| |\n+-------------------+------------+\n| Code Grade        | |codacy|   |\n+-------------------+------------+\n| Dependencies      | |depend|   |\n+-------------------+------------+\n| Pre-commit        | |precommit||\n+-------------------+------------+\n| Issues            | |issues|   |\n+-------------------+------------+\n\n.. |pypi| image:: https://img.shields.io/pypi/v/click_loguru.svg\n    :target: https://pypi.python.org/pypi/click_loguru\n    :alt: Python package\n\n.. |repo| image:: https://img.shields.io/github/commits-since/legumeinfo/click_loguru/0.1.0.svg\n    :target: https://github.com/legumeinfo/click_loguru\n    :alt: GitHub repository\n\n.. |license| image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg\n    :target: https://github.com/legumeinfo/click_loguru/blob/master/LICENSE.txt\n    :alt: License terms\n\n.. |travis| image:: https://img.shields.io/travis/legumeinfo/click_loguru.svg\n    :target:  https://travis-ci.org/legumeinfo/click_loguru\n    :alt: Travis CI\n\n.. |codacy| image:: https://api.codacy.com/project/badge/Grade/6ee5771afe014cffbb32a2f79cf17fff\n    :target: https://www.codacy.com/gh/legumeinfo/click_loguru?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=legumeinfo/click_loguru&amp;utm_campaign=Badge_Grade\n    :alt: Codacy.io grade\n\n.. |coverage| image:: https://codecov.io/gh/legumeinfo/click_loguru/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/legumeinfo/click_loguru\n    :alt: Codecov.io test coverage\n\n.. |precommit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n    :target: https://github.com/pre-commit/pre-commit\n    :alt: pre-commit\n\n.. |issues| image:: https://img.shields.io/github/issues/legumeinfo/click_loguru.svg\n    :target:  https://github.com/legumeinfo/click_loguru/issues\n    :alt: Issues reported\n\n\n.. |depend| image:: https://api.dependabot.com/badges/status?host=github&repo=legumeinfo/click_loguru\n     :target: https://app.dependabot.com/accounts/legumeinfo/repos/236847525\n     :alt: dependabot dependencies\n',
    'author': 'Joel Berendzen',
    'author_email': 'joelb@ncgr.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/legumeinfo/click_loguru',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
