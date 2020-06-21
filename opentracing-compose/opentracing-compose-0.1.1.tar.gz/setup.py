# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opentracing_compose']

package_data = \
{'': ['*']}

install_requires = \
['opentracing']

setup_kwargs = {
    'name': 'opentracing-compose',
    'version': '0.1.1',
    'description': 'Opentracing tracer that composes other tracers',
    'long_description': '# opentracing-compose\n\nAn Opentracing tracer that composes multiple other tracers.\nUsed to trace to multiple Opentracing implementations at once.\n\n## License\n\nMIT.\n\n---\nCopyright (c) 2020 Brian Downing\n',
    'author': 'Brian Downing',
    'author_email': 'bdowning@lavos.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bdowning/opentracing-compose',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
