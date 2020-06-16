# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['intake_dal', 'intake_dal.tests']

package_data = \
{'': ['*'], 'intake_dal.tests': ['data/*']}

install_requires = \
['deepmerge==0.1.0',
 'intake-nested-yaml-catalog==0.1.0',
 'intake==0.5.4',
 'pandavro>=1.5.1,<2.0.0',
 'pyarrow>=0.15.1,<0.16.0',
 'pyyaml==5.1.2',
 'toolz>=0.10.0,<0.11.0',
 'vcver>=0.2.10']

entry_points = \
{'intake.drivers': ['dal = intake_dal.dal_source:DalSource',
                    'dal-online = intake_dal.dal_online:DalOnlineSource',
                    'dal_cat = intake_dal.dal_catalog:DalCatalog',
                    'in-memory-kvs = intake_dal.in_memory_kv:InMemoryKVSource']}

setup_kwargs = {
    'name': 'intake-dal',
    'version': '0.1.8',
    'description': 'Intake single YAML hierarchical catalog.',
    'long_description': '.. image:: https://travis-ci.org/zillow/intake-dal.svg?branch=master\n    :target: https://travis-ci.org/zillow/intake-dal\n\n.. image:: https://coveralls.io/repos/github/zillow/intake-dal/badge.svg?branch=master\n    :target: https://coveralls.io/github/zillow/intake-dal?branch=master\n\n.. image:: https://readthedocs.org/projects/intake-dal/badge/?version=latest\n    :target: https://intake-dal.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n\nWelcome to Intake DAL (data access layer) plugin\n==================================================\nThis `Intake <https://intake.readthedocs.io/en/latest/quickstart.html>`_ plugin helps\nabstract a dataset over disparate storage systems (eg: bulk, streaming, serving, ...).\nIt also provides an easy way to specialize a\n`hierarchical catalog <https://github.com/zillow/intake-nested-yaml-catalog/>`_\nto a default DAL storage system.\n\n\nSample Catalog source entry:\n\n.. code-block:: yaml\n\n    user_events:\n      driver: dal\n      args:\n        default: \'local\'\n        storage:\n          local: \'csv://{{ CATALOG_DIR }}/data/user_events.csv\'\n          serving: \'in-memory-kv://foo\'\n          batch: \'parquet://{{ CATALOG_DIR }}/data/user_events.parquet\'\n\nExample code using sample catalog:\n\n.. code-block:: python\n\n  # Specialize the catalog dal default storge mode datasources\n  # to be "serving".\n  cat = DalCatalog(path, storage_mode="serving")\n\n  # reads from the serving storage system\n  # using the in-memory-kv Intake plugin\n  df = cat.user_events.read()\n\n\n',
    'author': 'Zillow AI Platform',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
