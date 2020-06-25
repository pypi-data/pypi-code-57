# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['statsservice',
 'statsservice.api.v1',
 'statsservice.commands',
 'statsservice.lib',
 'statsservice.models',
 'statsservice.views']

package_data = \
{'': ['*']}

install_requires = \
['Flask-SQLAlchemy>=2.4.3,<3.0.0',
 'Flask>=1.1.2,<2.0.0',
 'flask_restx>=0.2.0,<0.3.0',
 'jsonschema>=3.2.0,<4.0.0',
 'pandas>=1.0.4,<2.0.0',
 'psycopg2-binary>=2.8.5,<3.0.0',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['monarc-stats-service = runserver:run']}

setup_kwargs = {
    'name': 'statsservice',
    'version': '0.1.3',
    'description': 'Stats Service for MONARC.',
    'long_description': '# Stats Service for MONARC\n\n[![License](https://img.shields.io/github/license/monarc-project/stats-service.svg?style=flat-square)](https://www.gnu.org/licenses/agpl-3.0.html)\n[![Contributors](https://img.shields.io/github/contributors/monarc-project/stats-service.svg?style=flat-square)](https://github.com/monarc-project/stats-service/graphs/contributors)\n[![Workflow](https://github.com/monarc-project/stats-service/workflows/Python%20application/badge.svg?style=flat-square)](https://github.com/monarc-project/stats-service/actions?query=workflow%3A%22Python+application%22)\n[![Documentation Status](https://readthedocs.org/projects/monarc-stats-service/badge/?version=latest&style=flat-square)](https://monarc-stats-service.readthedocs.io/en/latest/?badge=latest)\n\n## Presentation\n\n[This component](https://github.com/monarc-project/stats-service) provides an API\nin order to collect statistics from one or several\n[MONARC](https://github.com/monarc-project/MonarcAppFO) instances. It can be\ndeployed just next to MONARC (eventually in a virtual machine) or on a\ndedicated server.\n\nThese aggregated statistics can then be sent to a central instance.\n\n\n## Deployment\n\nThe following assumes you have already installed ``git``, ``poetry``,  and\n``Python >= 3.8``.\n\n```bash\n$ sudo apt install postgresql\n$ git clone https://github.com/monarc-project/stats-service\n$ cd stats-service/\n$ cp instance/production.py.cfg instance/production.py\n$ poetry install\n$ poetry shell\n$ export FLASK_APP=runserver.py\n$ export FLASK_ENV=development\n$ flask db_create\n$ flask db_init\n\n$ flask create_organization --name CASES\nName: CASES\nToken: SylsDTZTBk2zAkg016vW_aCuO1XQDXPsxrLuI1TG7z5sYvUfRlVf5R4g6kDnLI_o-c5iqrswrWzPANDKXmtV7Q\nCreated at: 2020-06-16 14:25:32.947745\n\n$ flask run\n * Serving Flask app "runserver.py" (lazy loading)\n * Environment: development\n * Debug mode: on\n * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)\n * Restarting with stat\n * Debugger is active!\n * Debugger PIN: 268-178-811\n```\n\nFor production you can use [Gunicorn](https://gunicorn.org) or ``mod_wsgi``.\n\n\n## Documentation\n\nA [documentation is available](https://monarc-stats-service.readthedocs.io).\n\n\n## License\n\n[Stats Service](https://github.com/monarc-project/stats-service) is under the\n[GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html).\n',
    'author': 'Cédric Bonhomme',
    'author_email': 'cedric@cedricbonhomme.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/monarc-project/stats-service',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
