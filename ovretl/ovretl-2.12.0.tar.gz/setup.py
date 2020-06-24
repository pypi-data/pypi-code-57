# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ovretl',
 'ovretl.billings_utils',
 'ovretl.billings_utils.tests',
 'ovretl.computed_quotations_utils',
 'ovretl.computed_quotations_utils.tests',
 'ovretl.containers_utils',
 'ovretl.containers_utils.tests',
 'ovretl.employees_utils',
 'ovretl.employees_utils.tests',
 'ovretl.loads_utils',
 'ovretl.loads_utils.tests',
 'ovretl.prices_utils',
 'ovretl.prices_utils.features_functions',
 'ovretl.prices_utils.tests',
 'ovretl.shipments_utils',
 'ovretl.shipments_utils.tests',
 'ovretl.shipowners_utils',
 'ovretl.shipowners_utils.__tests__',
 'ovretl.tracking_utils',
 'ovretl.tracking_utils.tests',
 'ovretl.transit_times',
 'ovretl.transit_times.tests']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.3,<2.0.0']

setup_kwargs = {
    'name': 'ovretl',
    'version': '2.12.0',
    'description': 'Python package for Ovrsea ETL',
    'long_description': '',
    'author': 'nicolas67',
    'author_email': 'nicolas@ovrsea.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
