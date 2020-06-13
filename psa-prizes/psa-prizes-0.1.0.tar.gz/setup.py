# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['psa_prizes']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'html5lib>=1.0.1,<2.0.0',
 'pandas>=1.0.4,<2.0.0',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['psa-prizes = psa_prizes.psa_scrape:main']}

setup_kwargs = {
    'name': 'psa-prizes',
    'version': '0.1.0',
    'description': 'The PSA prizes project.',
    'long_description': '.. image:: https://badge.fury.io/py/psa-prizes.svg\n  :target: https://pypi.org/project/psa-prizes\n\n.. image:: https://github.com/tostenzel/psa-prizes/workflows/Continuous%20Integration/badge.svg?branch=master\n  :target: https://github.com/tostenzel/psa-prizes/actions\n\n.. image:: https://readthedocs.org/projects/psa-prizes/badge/?version=latest\n   :target: https://psa-prizes.readthedocs.io/en/latest/?badge=latest\n\n.. image:: https://codecov.io/gh/tostenzel/psa-prizes/branch/master/graph/badge.svg\n  :target: https://codecov.io/gh/tostenzel/psa-prizes\n\n.. image:: https://api.codacy.com/project/badge/Grade/87ad6f0069fd45d9afd5ad97a579329b\n   :alt: Codacy Badge\n   :target: https://app.codacy.com/manual/tostenzel/psa-prizes?utm_source=github.com&utm_medium=referral&utm_content=tostenzel/psa-prizes&utm_campaign=Badge_Grade_Dashboard',
    'author': 'Tobias Stenzel',
    'author_email': 'tobias.stenzel@mailbox.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tostenzel/psa-prizes',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
