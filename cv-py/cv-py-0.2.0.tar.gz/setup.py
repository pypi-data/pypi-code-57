# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cv_py', 'cv_py.resources', 'cv_py.tools']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.5.0,<2.0.0',
 'dask[complete]>=2.13.0,<3.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pyarrow>=0.16.0,<0.17.0',
 'requests>=2.23.0,<3.0.0',
 'scikit-learn>=0.22.2,<0.23.0',
 'semantic_version>=2.8.5,<3.0.0',
 'tqdm>=4.43.0,<5.0.0']

extras_require = \
{'flair': ['flair>=0.4.5,<0.5.0'],
 'spacy': ['textacy>=0.10.0,<0.11.0', 'scispacy>=0.2.4,<0.3.0'],
 'viz': ['holoviews[recommended]>=1.13.2,<2.0.0',
         'seaborn>=0.10.0,<0.11.0',
         'panel>=0.9.5,<0.10.0']}

entry_points = \
{'console_scripts': ['cv-download = cv_py.resources.datapackage:download_cli']}

setup_kwargs = {
    'name': 'cv-py',
    'version': '0.2.0',
    'description': 'Collection of tools and techniques to kick-start analysis of the COVID-19 Research Challenge Dataset ',
    'long_description': None,
    'author': 'Thurston Sexton',
    'author_email': 'thurston.sexton@nist.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
