# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcane']

package_data = \
{'': ['*']}

install_requires = \
['arcane-core>=1.0.2,<2.0.0', 'backoff==1.10.0', 'google-cloud-tasks==1.5.0']

setup_kwargs = {
    'name': 'arcane-tasks',
    'version': '0.2.1',
    'description': 'Overide tasks client',
    'long_description': '# Arcane CloudTask\n\nThis package is base on [google-cloud-cloudtasks](https://pypi.org/project/google-cloud-tasks/).\n\n## Get Started\n\n```sh\npip install arcane-tasks\n\n## Example Usage\n\n```python\nfrom arcane import tasks\n\n# Import your configs\nfrom configure import Config\n\ntasks_client = tasks.Client(adscale_key=Config.KEY, project=Config.GCP_PROJECT)\nbody = {\n    \'attribute\' : value\n}\ntask_name = "My task"\ntasks_client.publish_task(\n    queue=<your-queue>,\n    url=<url-to-triger>,\n    body=body,\n    task_name=task_name\n)\n```\n',
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
