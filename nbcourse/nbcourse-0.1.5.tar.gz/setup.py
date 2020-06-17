# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nbcourse']

package_data = \
{'': ['*']}

install_requires = \
['IPython>=7.15.0,<8.0.0',
 'bookbook>=0.2,<0.3',
 'bs4>=0.0.1,<0.0.2',
 'doit>=0.32.0',
 'jinja2>=2.11.2,<3.0.0',
 'jupyter_contrib_nbextensions>=0.5.1,<0.6.0',
 'latex>=0.7.0,<0.8.0',
 'markdown>=3.2.2,<4.0.0',
 'python-frontmatter>=0.5.0,<0.6.0',
 'pyyaml>=5.3.1,<6.0.0',
 'rise>=5.6.1,<6.0.0']

entry_points = \
{'console_scripts': ['nbcourse = nbcourse:main']}

setup_kwargs = {
    'name': 'nbcourse',
    'version': '0.1.5',
    'description': 'Create a minisite to publish a course based on Jupyter notebooks',
    'long_description': '# nbcourse: publish your course based on Jupyter notebooks\n\n## Features\n\n`nbcourse` helps you building a static website to publish your course content in the form of jupyter notebooks (one notebook for one chapter).\n\nMain features:\n\n- all the configuration is described by a single `nbcourse.yml` file\n- it is based on [doit](https://pydoit.org) in order to build efficently the html files\n- chapters can be displayed in *preview mode* only so attendees can see the whole course program without being able to access content of the lessons to come\n- notebooks can be:\n    - rendered as static html files,\n    - rendered as static reveal slideshows,\n    - packaged with all their material in a downloadable archive,\n    - compiled in a single pdf book using [bookbook](https://github.com/takluyver/bookbook)\n- the theme can be easily customized (html files are templated using jinja)\n\nSee [this python course](https://mm2act.pages.math.unistra.fr/cours-python/) (in French) as an example.\n\n## Installation\n\n```bash\npip install nbcourse\n```\n\n## Usage\n\n### Initiate an empty nbcourse project\n\n```bash\nnbcourse --init\n```\n\n### Configure your website\n\n- Put your notebooks file in the `notebook/` directory\n- Edit the `nbcourse.yml` file created by the `nbcourse --init` command.\n\n### Build your website\n\n```bash\nnbcourse\n```\n\nResulting files are in the `build/` directory.\n\n### Get help\n\n```bash\nnbcourse --help\n```\n\n### Publish\n\nPublishing with [GitLab Pages](https://docs.gitlab.com/ee/user/project/pages/) is as simple as adding a `.gitlab-ci.yml` file such as:\n\n```yaml\npages:\n  image: boileaum/jupyter\n  script:\n    - pip install nbcourse\n    - nbcourse -n 5\n    - mv build public\n  artifacts:\n    paths:\n      - public\n```\n',
    'author': 'Matthieu Boileau',
    'author_email': 'matthieu.boileau@math.unistra.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.math.unistra.fr/boileau/nbcourse',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
