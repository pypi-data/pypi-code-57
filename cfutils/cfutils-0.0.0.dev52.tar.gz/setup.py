# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfutils']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7.0.0,<8.0.0', 'biopython>=1.70,<2.0', 'matplotlib>=3.0.0,<4.0.0']

entry_points = \
{'console_scripts': ['cfutils = cfutils.cli:cli']}

setup_kwargs = {
    'name': 'cfutils',
    'version': '0.0.0.dev52',
    'description': 'Chromatogram File Utils',
    'long_description': "# cfutils\n\n**Chromatogram File Utils**\n\nFor Sanger sequencing data visualizing, alignment, mutation calling, and trimming etc.\n\n## Demo\n\n![plot chromatogram with mutation](https://raw.githubusercontent.com/yech1990/cfutils/master/data/plot.png)\n\n> command to generate the demo above\n\n```bash\ncfutils mut --query ./data/B5-M13R_B07.ab1 --subject ./data/ref.fa --outdir ./data/ --plot\n```\n\n## How to install?\n\n### form pypi\n\n*(use this way ONLY, if you don't know what's going on)*\n\n```bash\npip install cfutils\n```\n\n### manipulate the source code\n\n- clone from github\n\n```bash\ngit clone git@github.com:yech1990/cfutils.git \n```\n\n- install the dependence\n\n```bash\nmake init\n```\n\n- do unittest\n\n```bash\nmake test\n```\n\n## How to use?\n\n- in the command line\n\n```bash\ncfutils mut --help\n```\n\n- or as a python module\n\n```python\nimport cfutils as cf\n```\n\n## ChangeLog\n\n- build as python package for pypi\n- fix bug that highlighting wrong base\n\n## TODO\n\n- [ ] call mutation by alignment and plot Chromatogram graphic\n- [ ] add a doc\n- [x] change xaxis by peak location\n- [ ] fix bug that chromatogram switch pos after trim\n- [x] wrap as a cli app\n- [ ] return quality score in output\n- [ ] fix issue that selected base is not in the middle\n- [ ] fix plot_chromatograph rendering bug\n\n- [ ] add projection feature to make align and assemble possible   \n",
    'author': 'Ye Chang',
    'author_email': 'yech1990@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yech1990/cfutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
