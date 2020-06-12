# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitreload', 'gitreload.tests']

package_data = \
{'': ['*'], 'gitreload.tests': ['data/*']}

install_requires = \
['flask>=1.1.2,<2.0.0', 'gitpython>=3.1.3,<4.0.0', 'gunicorn>=20.0.4,<21.0.0']

entry_points = \
{'console_scripts': ['gitreload = gitreload.web:run_web']}

setup_kwargs = {
    'name': 'gitreload',
    'version': '0.2.5',
    'description': 'Service for triggering edX course imports from Github webhooks',
    'long_description': '<!-- markdown-extras: code-friendly, footnotes, fenced-code-blocks -->\ngitreload\n=========\n[![Build Status](http://img.shields.io/travis/mitodl/gitreload.svg?style=flat)](https://travis-ci.org/mitodl/gitreload)\n[![Coverage Status](http://img.shields.io/coveralls/mitodl/gitreload.svg?style=flat)](https://coveralls.io/r/mitodl/gitreload)\n[![PyPi Downloads](http://img.shields.io/pypi/dm/gitreload.svg?style=flat)](https://pypi.python.org/pypi/gitreload)\n[![PyPi Version](http://img.shields.io/pypi/v/gitreload.svg?style=flat)](https://pypi.python.org/pypi/gitreload)\n[![License AGPLv3](http://img.shields.io/badge/license-AGPv3-blue.svg?style=flat)](http://www.gnu.org/licenses/agpl-3.0.html)\n\ngitreload is a Flask/WSGI application for responding to github\ntriggers asynchronously.  Out of the box it is primarily intended for\nuse with the [edx-platform](https://github.com/edx/edx-platform), but\ncould be used for generally updating local git repositories based on a\ntrigger call from github using its `/update` url.\n\nThe general workflow is that a github trigger is received (push),\ngitreload checks if the respository and branch are already checked\nout in the configured location, and then either\nimports that repository into the edx-platform via a `... manage.py lms\n--settings=... git_add_course <repo_dir> <repo_name>` command, or if\nthe trigger is set to go to `/update` instead of `/` or `/gitreload`,\nit will simply fetch the newset version of the currently checked out\nbranch from the `origin` remote. Authorization is generally expected\nto be provided by the Web server in front of it (using basic\nauthentication), as it currently doesn\'t support the use of github\nsecrets. An additional layer of security is provided by the fact that\na repository must be cloned on gitreload\'s host before it will accept\npayloads from github for said repository.\n\n## Installation ##\n\n`pip install gitreload`\n\nor to use the latest github version it would\nbe:\n\n`pip install -e git+https://github.com/mitodl/gitreload`\n\n## Usage ##\n\ngitreload is a flask application, and thus can be run either in debug\nmode by directly using the `gitreload` command, or by\nusing a wsgi application server.  For more information on running a\nflask app in a production mode, see the excellent\n[flask documentation](http://flask.pocoo.org/docs/0.10/deploying/wsgi-standalone/).\nWe generally have run it using gunicorn and supervisord in a similar\nmanner that [edx/configuration](https://github.com/edx/configuration)\nroles follow, and eventually we plan on submitting a role to install\nthis via their ansible plays.\n\nUpon running `gitreload` via command line, you should see that it\nstarts up listening on port 5000. You can verify that it is working by\ngoing to the queue status page at `http://localhost:5000/queue`.\nIf all is well, you should be greeted with some lovely json that looks\nlike:\n\n```javascript\n{"queue_length": 0, "queue": []}\n```\n\n## Configuration ##\n\nConfiguration is done via a json file stored in order of precedence:\n\n- Path in environment variable: `GITRELOAD_CONFIG`\n- $(pwd)/gr.env.json\n- ~/gr.env.json\n- /etc/gr.env.json\n\nIt isn\'t strictly required, and the defaults are:\n\n```javascript\n{\n    "DJANGO_SETTINGS": "aws",\n    "EDX_PLATFORM": "/edx/app/edxapp/edx-platform",\n    "LOG_LEVEL": null,\n    "NUM_THREADS": 1,\n    "REPODIR": "/mnt/data/repos",\n    "VIRTUAL_ENV": "/edx/app/edxapp/venvs/edxapp"\n}\n```\n\nThis setup means that it looks for the git repositories to be cloned\nin `/mnt/data/repos`, and expects the edx-platform settings to be the\ncurrent [edx/configuration](https://github.com/edx/configuration)\ndefaults.  It also leaves the LOG_LEVEL set to the default which\nis `WARNING`, and provides only one worker thread to process the\nqueue of received triggers from github.\n\n## Use Cases ##\n\nThis is currently in use at MITx primarily for the following reasons.\n\n### Rapid Centralized Course Development ###\n\nOne of our primary uses of this tool is to enable rapid shared XML\nbased edx-platform course development.  It is basically the continuous\nintegration piece for our courseware, such that when a commit gets\npushed to a github repo on a specific branch (say devel), the changes\nare quickly and automatically loaded up with the use of this hook\nconsumer.\n\n### Course Deployment Management ###\n\nAlong the lines of the rapid course development, we also use this\nmethod for controlling which courses get published on our production\nstudent facing LMS.  For raw github XML developers, this means that we\nhook up our student facing LMS to a specific branch intended for\nproduction (say master or release). We use this to monitor that branch\nfor changes they have vetted in their development branch and are ready\nto deploy to students.\n\nWe don\'t limit our usage of gitreload to XML development though, as we\nalso gate our Studio course teams with this same method. There is a\nfeature in the platform that allows course teams to export their course\nto Git. We use this function to control student access, allowing our\nStudio course authors to push at will to production once the trigger\nand repositories are setup for their course.\n\n### Update of external course graders ###\n\nWe use the regular `/update` feature to automatically update external\ncode graders that are served via\n[xqueue-watcher](https://github.com/edx/xqueue-watcher) or\n[xserver](https://github.com/edx/xserver).  We use this in a similar\nvain as the previous two cases and manages a development and\nproduction branch for the repository that contains the graders.\n',
    'author': 'MIT Open Learning',
    'author_email': 'mitx-devops@mit.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mitodl/gitreload',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
