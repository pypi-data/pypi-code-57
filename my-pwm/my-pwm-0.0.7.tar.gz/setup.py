# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['my_pwm']
install_requires = \
['fire>=0.3.1,<0.4.0', 'pyperclip>=1.8.0,<2.0.0', 'qrcode>=6.1,<7.0']

entry_points = \
{'console_scripts': ['pw = my_pwm:main']}

setup_kwargs = {
    'name': 'my-pwm',
    'version': '0.0.7',
    'description': 'Passward maneger',
    'long_description': 'mypwgen\n=======\n\nPassward generator\n\nHow to Use\n----------\n',
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
