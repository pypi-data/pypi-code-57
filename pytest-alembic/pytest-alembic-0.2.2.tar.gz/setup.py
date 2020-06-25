# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_alembic', 'pytest_alembic.plugin']

package_data = \
{'': ['*']}

install_requires = \
['alembic', 'pytest>=1.0', 'sqlalchemy']

extras_require = \
{':python_version <= "3.7"': ['dataclasses']}

entry_points = \
{'pytest11': ['pytest_alembic = pytest_alembic.plugin']}

setup_kwargs = {
    'name': 'pytest-alembic',
    'version': '0.2.2',
    'description': 'A pytest plugin for verifying alembic migrations.',
    'long_description': '![CircleCI](https://img.shields.io/circleci/build/gh/schireson/pytest-alembic/master) [![codecov](https://codecov.io/gh/schireson/pytest-alembic/branch/master/graph/badge.svg)](https://codecov.io/gh/schireson/pytest-alembic) [![Documentation Status](https://readthedocs.org/projects/pytest-alembic/badge/?version=latest)](https://pytest-alembic.readthedocs.io/en/latest/?badge=latest)\n\n\n## Introduction\n\nA pytest plugin to test alembic migrations (with default tests) and which enables\nyou to write tests specific to your migrations.\n\n```bash\n$ pip install pytest-alembic\n$ pytest --test-alembic\n\n...\n::pytest_alembic/tests/model_definitions_match_ddl <- . PASSED           [ 25%]\n::pytest_alembic/tests/single_head_revision <- . PASSED                  [ 50%]\n::pytest_alembic/tests/up_down_consistency <- . PASSED                   [ 75%]\n::pytest_alembic/tests/upgrade <- . PASSED                               [100%]\n\n============================== 4 passed in 2.32s ===============================\n```\n\n\n## The pitch\n\nHave you ever merged a change to your models and you forgot to generate a migration?\n\nHave you ever written a migration only to realize that it fails when there\'s data in the table?\n\nHave you ever written a **perfect** migration only to merge it and later find out that someone\nelse merged also merged a migration and your CD is now broken!?\n\n`pytest-alembic` is meant to (with a little help) solve all these problems and more. Note, due to\na few different factors, there **may** be some [minimal required setup](http://pytest-alembic.readthedocs.io/en/latest/setup.html);\nhowever most of it is boilerplate akin to the setup required for alembic itself.\n\n### Built-in Tests\n\n* **test_single_head_revision**\n\n  Assert that there only exists one head revision.\n\n  We\'re not sure what realistic scenario involves a diverging history to be desirable. We\n  have only seen it be the result of uncaught merge conflicts resulting in a diverged history,\n  which lazily breaks during deployment.\n\n\n* **test_upgrade**\n\n  Assert that the revision history can be run through from base to head.\n\n\n* **test_model_definitions_match_ddl**\n\n  Assert that the state of the migrations matches the state of the models describing the DDL.\n\n  In general, the set of migrations in the history should coalesce into DDL which is described\n  by the current set of models. Therefore, a call to `revision --autogenerate` should always\n  generate an empty migration (e.g. find no difference between your database (i.e. migrations\n  history) and your models).\n\n\n* **test_up_down_consistency**\n\n  Assert that all downgrades succeed.\n\n  While downgrading may not be lossless operation data-wise, there’s a theory of database\n  migrations that says that the revisions in existence for a database should be able to go\n  from an entirely blank schema to the finished product, and back again.\n\n\n### Custom Tests\n\nFor more information, see the docs for [custom tests](http://pytest-alembic.readthedocs.io/en/latest/custom_tests.html)\n(example below) or [custom static data](http://pytest-alembic.readthedocs.io/en/latest/custom_data.html)\n(to be inserted automatically before a given revision).\n\nSometimes when writing a particularly knarly data migration, it helps to be able to practice a\nlittle timely TDD, since there\'s always the potential you\'ll trash your actual production data.\n\nWith `pytest-alembic`, you can write tests directly, in the same way that you would normally,\nthrough the use of the `alembic_runner` fixture.\n\n```python\ndef test_knarly_migration_xyz123(alembic_engine, alembic_runner):\n    # Migrate up to, but not including this new migration\n    alembic_runner.migrate_up_before(\'xyz123\')\n\n    # Perform some very specific data setup, because this migration is sooooo complex.\n    # ...\n    alembic_engine.execute(table.insert(id=1, name=\'foo\'))\n\n    alembic_runner.migrate_up_one()\n```\n\n`alembic_runner` has a number of methods designed to make it convenient to change the state of\nyour database up, down, and all around.\n\n\n## Installing\n\n```bash\npip install "pytest-alembic"\n```\n',
    'author': 'Dan Cardin',
    'author_email': 'ddcardin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/schireson/pytest-alembic',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4',
}


setup(**setup_kwargs)
