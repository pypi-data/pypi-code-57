# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['happier']

package_data = \
{'': ['*']}

install_requires = \
['autoflake>=1.3.1,<2.0.0',
 'black>=19.10b0,<20.0',
 'isort[requirements,pipenv]>=4.3.21,<5.0.0',
 'pylint>=2.5.3,<3.0.0']

entry_points = \
{'console_scripts': ['happier = happier.main:main']}

setup_kwargs = {
    'name': 'happier',
    'version': '0.1.0',
    'description': 'A tool for formatting, checking and testing your code that makes you well, happier',
    'long_description': '#########\nHappier\n#########\n\nA Python development tool that makes you Happier.\n\nHappier formats, lints and sorts your imports. Happier is opinionated,\nsimple and just works, making you hopefully happier.\n\nTo run it just type ``happier`` and your code will be formatted.\n\n*******************\nWhat Happier does\n*******************\n\nHappier does a number of things with your code. First it runs\n``isort`` to sort your imports and properly format them.\n\nAfter having sorted them it runs ``autoflake`` to remove unused things.\n\nFinally having done all of that it runs ``black`` to format the code nicely.\n\n*************\nWhy Happier\n*************\n\nHappier was developed by myself, `William Rudenmalm (https://whn.se)`\nbecause I felt that Python was falling behind on automatically\nformatting and fixing my code. All the parts where already there I\njust needed those 50 lines of code to tie it all together.\n\nWith well-wishes and hopes for brigther days ahead in these troubled\ntimes.\n\n~William Rudenmalm\n\nStockholm, 22 June, 2020\n',
    'author': 'William Rudenmalm',
    'author_email': 'me@whn.se',
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
