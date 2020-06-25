# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jiradata']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'pandas>=1.0.5,<2.0.0']

entry_points = \
{'console_scripts': ['jiradata = jiradata.jiradata:cli']}

setup_kwargs = {
    'name': 'jiradata',
    'version': '1.1.2',
    'description': 'Simple JIRA data manipulation',
    'long_description': '# Jira data\n\n> Cause sometimes you need to sort out your issues\n\nProgrammatic way to pull out your issues.\n\n## Install\n\n`pip install jiradata`\n\n## How to use ?\n\nWrite a csv report\n\n```shell\ncat response.json | jiradata myreport.csv\n```\n\nWith some \'Epic\' and issue related to it :\n\n```shell\ncat response.json |jiradata --epic-field customfield_10000 report.csv\n```\n\n## Hold up what is this `reponse.json` ?\n\nIssues in json format from the JIRA REST API.\n\nWhat I found convenient is to use the [search API](https://developer.atlassian.com/cloud/jira/platform/rest/v2/#api-rest-api-2-search-post)) with JQL.\n\nYou can chain unix style arguments using [httpie](https://httpie.org/)\n\nconfig.json\n\n```json\n{\n  "jql": "project = QA",\n  "startAt": 0,\n  "maxResults": 2,\n  "fields": ["id", "key"]\n}\n```\n\nCommand line (redirect stdout to the right location)\n\n```sh\ncat config.json|http -a myusername post \'https://<site-url>/rest/api/2/search\'\n```\n\n##\xa0Related\n\n- Built in jira : [Export results to microsoft Excel](https://confluence.atlassian.com/jira061/jira-user-s-guide/searching-for-issues/working-with-search-result-data/exporting-search-results-to-microsoft-excel)\n- https://github.com/pycontribs/jira',
    'author': 'Khalid CK',
    'author_email': 'fr.ckhalid@gmail.com',
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
