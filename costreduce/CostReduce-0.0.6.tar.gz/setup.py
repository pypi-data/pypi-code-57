# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['costreduce',
 'costreduce.core',
 'costreduce.core.providers',
 'costreduce.core.services',
 'costreduce.core.services.aws',
 'costreduce.utils']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.13.6',
 'click-log>=0.3.2',
 'click>=7.1.2',
 'python-dotenv>=0.13.0',
 'texttable>=1.6.2']

entry_points = \
{'console_scripts': ['costreduce = costreduce.main:cli']}

setup_kwargs = {
    'name': 'costreduce',
    'version': '0.0.6',
    'description': '',
    'long_description': '# CostReduce\n\n![Tests](https://github.com/CostReduce/cli/workflows/Tests/badge.svg?branch=master&event=push)\n[![Requirements Status](https://requires.io/github/CostReduce/cli/requirements.svg?branch=master)](https://requires.io/github/CostReduce/cli/requirements/?branch=master)\n[![codecov](https://codecov.io/gh/costreduce/cli/branch/master/graph/badge.svg)](https://codecov.io/gh/costreduce/cli)\n![GitHub](https://img.shields.io/github/license/costreduce/cli)\n\n## Usage\n### Install\nFor use this project, you need to install :\n```\npip install costreduce\n```\nAfter install is complete. You can use the `costreduce --help` command.\n\n### First Run\nCheck that you have correctly configured the [AWS cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).\n```\ncostreduce analyze --provider aws --service ec2 --region us-east-1\n```\n## Developement\n### Requirements\nCheck that you have correctly configured the [AWS cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).\nFor install requirements.\n```\npoetry install\n```\nFor launch virtual env.\n```\npoetry shell\n```\n### Analyze cli\n```\npython costreduce/main.py analyze --provider aws --service ec2 --region us-east-1\n```\n',
    'author': 'Maxence Maireaux',
    'author_email': 'maxence@maireaux.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
