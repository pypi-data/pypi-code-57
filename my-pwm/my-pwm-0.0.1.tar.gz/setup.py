# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['my_pwm']
install_requires = \
['black>=19.10b0,<20.0',
 'fire>=0.3.1,<0.4.0',
 'flake8>=3.8.3,<4.0.0',
 'isort>=4.3.21,<5.0.0',
 'mypy>=0.780,<0.781',
 'pytest>=5.4.3,<6.0.0']

entry_points = \
{'console_scripts': ['pw = my_pwm:main']}

setup_kwargs = {
    'name': 'my-pwm',
    'version': '0.0.1',
    'description': 'Passward maneger',
    'long_description': 'mypwgen\n=======\n\nPassward generator\n',
    'author': 'Daisuke Oku',
    'author_email': 'w.40141@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
