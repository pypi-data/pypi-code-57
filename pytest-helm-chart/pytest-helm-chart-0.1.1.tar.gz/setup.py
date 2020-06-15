# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_helm_charts', 'pytest_helm_charts.apps']

package_data = \
{'': ['*']}

install_requires = \
['pykube-ng>=20.5.0,<21.0.0', 'pytest>=5.4.2,<6.0.0']

entry_points = \
{'pytest11': ['kube-provider = pytest_helm_chart']}

setup_kwargs = {
    'name': 'pytest-helm-chart',
    'version': '0.1.1',
    'description': 'A plugin to provide different types and configs of Kubernetes clusters that can be used for testing.',
    'long_description': '# pytest-kube-provider\n\nA plugin to provide different types and configs of Kubernetes clusters that can be used for testing.\n\n---\n\n\n\n## Features\n\n* TODO\n\n\n## Requirements\n\n* TODO\n\n\n## Installation\n\nYou can install "pytest-kube-provider" via `pip` from `PyPI`:\n\n```\n$ pip install pytest-kube-provider\n```\n\n\n## Usage\n\n* TODO\n\n## Contributing\n\nContributions are very welcome. Tests can be run with `tox`_, please ensure\nthe coverage at least stays the same before you submit a pull request.\n\n## License\n\nSee [LICENSE](LICENSE).\n\n## Issues\n\nIf you encounter any problems, please [file an issue](https://github.com/piontec/pytest-kube-provider/issues) along with a detailed description.\n\n',
    'author': 'Łukasz Piątkowski',
    'author_email': 'lukasz@giantswarm.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/giantswarm/pytest-helm-chart',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
