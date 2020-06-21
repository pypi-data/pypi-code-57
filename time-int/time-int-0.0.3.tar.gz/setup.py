# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['time_int']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=5.4.2,<6.0.0']

setup_kwargs = {
    'name': 'time-int',
    'version': '0.0.3',
    'description': 'Subclass of integer representing seconds since UNIX epoch',
    'long_description': '# time-int\nInteger subclass to represent naive time since epoch.\n\n### The Idea\nUNIX has a venerable tradition of representing time as seconds since the\nstart of 1970. This has its limitations, but it is sometimes desirably\nsimple. This package sub-classes int to give a little handy functionality\nto this simple approach.\n\n### Important Limitations\n* Supported range starts at 0 or TimeInt.MIN on Jan 1, 1970\n* Supported range ends at a 32-bit limit or TimeInt.MAX on Apr 2, 2106\n* Values are rounded off to the nearest second.\n* Values do not track what time-zone they represent.\n\n### Quick Example\n```python\nfrom time_int import TimeInt\n\nstart_time = TimeInt.utcnow()\nsome_slow_operation()\nend_time = TimeInt.utcnow()\n\nprint(f"Operation started at {start_time.get_pretty()}")\nprint(f"Operation ended  at  {end_time.get_pretty()}")\nprint(f"Operation took {end_time - start_time} seconds")\n```\n\n',
    'author': 'Andrew Allaire',
    'author_email': 'andrew.allaire@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aallaire/time-int',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
