# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['forge_template',
 'forge_template.exception',
 'forge_template.handler',
 'forge_template.templates.databricks.jobs',
 'forge_template.templates.databricks.notebooks',
 'forge_template.templates.databricks.setup',
 'forge_template.templates.infra_scripts',
 'forge_template.util']

package_data = \
{'': ['*'],
 'forge_template': ['schema/*',
                    'templates/github_workflows/*',
                    'templates/pipelines/*',
                    'templates/powerbi/datasets/*',
                    'templates/powerbi/reports/*']}

install_requires = \
['cerberus>=1.3,<2.0',
 'click>=7.0,<8.0',
 'colorama==0.4.1',
 'databricks-api>=0.3.0,<0.4.0',
 'google-cloud-storage>=1.28.0,<2.0.0',
 'google.cloud>=0.34.0,<0.35.0',
 'jinja2>=2.11.2,<3.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'requests>=2.22,<3.0',
 'ruamel.yaml>=0.16.5,<0.17.0',
 'termcolor>=1.1.0,<2.0.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['forge-template = forge_template.main:cli']}

setup_kwargs = {
    'name': 'cognite-forge-template',
    'version': '0.10.0',
    'description': 'Automation of software used for data science in Cognite, including Databricks, PowerBI, Git and Grafana',
    'long_description': None,
    'author': 'Magnus Moan',
    'author_email': 'magnus.moan@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
