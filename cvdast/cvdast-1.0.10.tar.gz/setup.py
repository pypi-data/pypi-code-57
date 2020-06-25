# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cvdast', 'cvdast.tests', 'cvdast.zaputils', 'cvdast.zaputils.scripts']

package_data = \
{'': ['*'],
 'cvdast': ['assets/*',
            'templates/*',
            'wfuzz/.git/*',
            'wfuzz/.git/hooks/*',
            'wfuzz/.git/info/*',
            'wfuzz/.git/logs/*',
            'wfuzz/.git/logs/refs/heads/*',
            'wfuzz/.git/logs/refs/remotes/origin/*',
            'wfuzz/.git/objects/72/*',
            'wfuzz/.git/objects/8d/*',
            'wfuzz/.git/objects/a4/*',
            'wfuzz/.git/objects/b0/*',
            'wfuzz/.git/objects/db/*',
            'wfuzz/.git/objects/pack/*',
            'wfuzz/.git/refs/heads/*',
            'wfuzz/.git/refs/remotes/origin/*',
            'wfuzz/wordlist/general/*',
            'wfuzz/wordlist/injections/*',
            'wfuzz/wordlist/others/*',
            'wfuzz/wordlist/stress/*',
            'wfuzz/wordlist/vulns/*',
            'wfuzz/wordlist/webservices/*']}

install_requires = \
['PyYAML==5.3.1',
 'curlify==2.2.1',
 'cvapianalyser',
 'dictor==0.1.7',
 'jinja2',
 'openapispecdiff',
 'pytest-cases==1.16.0',
 'pytest-html==2.1.1',
 'pytest==5.4.3',
 'requests==2.22.0',
 'tqdm==4.46.1']

entry_points = \
{'console_scripts': ['cv-dast = cvdast.CloudvectorDAST:main']}

setup_kwargs = {
    'name': 'cvdast',
    'version': '1.0.10',
    'description': 'To regenerate pytest fixtures and test methods dynamically from OpenAPI spec and Cloudvector APIShark events',
    'long_description': '# cv-dast\n\nCV-DAST is a Python library for regenerating the pytest fixtures and test cases dynamically from Open API Spec and Cloudvector APIShark events \n\nVisit https://www.cloudvector.com/api-shark-free-observability-security-monitoring-tool/#apishark\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.\n\n```bash\npip install cv-dast\n```\n\n## Usage\n\n```python cv-dast \n\n****************************************************************************************************\nCloudVector CommunityEdition - Coverage analysis plugin\n****************************************************************************************************\n\nEnter CommunityEdition(CE) host in format <host>:<port> : x.x.x.x:y\nEnter your CommunityEdition(CE) username : sandeep\nCommunityEdition(CE) password:\nEnter absolute path to Old API SPEC: ../input.json\nEnter absolute path to new API SPEC : ../input1.json \nDo you want to process only diff? (Y/N) : \nEnter absolute path to input parameteres json(press Enter for None):\n```\n\ninstead of giving inputs every single time you can also alternatively create a file called my_cesetup.yaml in the path from where you are running the tool\n\n```yaml \nce_host:\nce_username:\n```\nyou can have multiple such my_cesetup.yaml for different CE setup or different recordings and run them from specific paths for its corresponding reports\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)',
    'author': 'Bala Kumaran',
    'author_email': 'balak@cloudvector.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
