# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcane']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-error-reporting==0.34.0']

setup_kwargs = {
    'name': 'arcane-stackdriver',
    'version': '0.1.0',
    'description': 'Override stackdriver client',
    'long_description': '# Arcane Stackdriver\n\nThis package is based on [google-cloud-error-reporting](https://pypi.org/project/google-cloud-error-reporting/).\n\n## Get Started\n\n```sh\npip install arcane-stackdriver\n```\n\n## Example Usage\n\n```python\nfrom arcane import stackdriver\nclient = stackdriver.Client()\n```\n\nor\n\n```python\nfrom arcane import stackdriver\n\n# Import your configs\nfrom configure import Config\n\nclient = stackdriver.Client.from_service_account_json(Config.KEY, project=Config.GCP_PROJECT)\n```\n',
    'author': 'Arcane',
    'author_email': 'product@arcane.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
