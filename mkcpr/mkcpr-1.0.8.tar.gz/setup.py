# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkcpr']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['mkcpr = mkcpr.command_line:main']}

setup_kwargs = {
    'name': 'mkcpr',
    'version': '1.0.8',
    'description': 'mkcpr is a command line utility that helps you to build your Competitive Programming Reference in PDF.',
    'long_description': '\n\n# mkcpr\n\n### Competitive Programming Reference Builder Tool\n\n## About\n\n```mkcpr``` is a command line utility written in python that helps you to build your *Competitive Programming Reference* in PDF.\n\nThis command will generate a LaTex formatted file, which will be ready to be compiled into your new *Competitive Programming Reference*, using any online or local LaTex compiler of your preference.\n## Usage\n\n- In your working directory run:\n\n```shell\nmkcpr [CONFIG FILE PATH]\n```\nNote: ```[CONFIG FILE PATH]``` is an optional parameter with ```"mkcpr-config.json"``` as default value\n\n## Requirements\n\n- python 3.5+\n- Online or local LaTex compiler\n- Folder containing your codes for programming competitions\n- LaTex template (you can use the one provided in this repository ```template.tex```)\n- Configuration File (described below)\n\n\n## Configuration File Options\n\n```jsonc\n{\n  "codeFolder" : "Code Folder Path", // Path to your actual code for reference\n  "templatePath" : "template.tex", // LaTex template path\n  "outputFilePath" : "output.tex", // path where you want the LaTex code\n  "excluded" : [".vscode", "__pycache__"], // folders not to consider\n  "columns" : 2, // number of columns in your reference\n  "templatePlaceHolder" : "CODE HERE", // text to replace in your template\n  "sortBefore" : ["Data Structures"], // files or folders will appear first\n  "sortAfter" : ["Extras"] // file or folders will appear at the end\n}\n```\n\n## Installation\n\n1. Run:\n  ```shell\n    pip install mkcpr --user\n  ```\n2. Copy the template and configuration files located in the root of this repository ```template.tex``` and ```mkcpr-config.json``` to your working directory\n3. Update ```mkcpr-config.json``` according to the [Configuration file options](#configuration-file-options) section.\n\n## Features\n\n- One single command and your reference will be ready to compile\n- Build it with your own style\n- support for most file extensions. (.cpp, .py, .java, .tex, .sh, ...)\n- Build your reference just from your competitive programming code folder.\n\n<div>\n  <img src="https://codeforces.com/predownloaded/43/53/4353216697913b06f2909ee25b7d7fe586133501.png"/>\n  <img src="https://codeforces.com/predownloaded/35/f5/35f510c1d145e2f3fb9fb147fcbf3febdff3ddf2.png"/>\n</div>\n\n- Forget about undesired line breaks by specifying the lines of code you want together in the same page with a single comment before your lines of code.\n\n\n<div>\n  <div style="width: 100px; height: 10px; background: red;"></div>\n  <img src="https://codeforces.com/predownloaded/29/ea/29ea463f8ac652c6bb5fa20fc1c7690546479333.png"/>\n</div>\n\n<div>\n  <img src="https://codeforces.com/predownloaded/a1/4f/a14f0a93f62f3afb7d3519779c18d7e991948ed7.png" width="400" height="250"/>\n  <img src="https://codeforces.com/predownloaded/f6/1e/f61ec142697979d7ebb5b3ec715e2856ebc2faaf.png" width="400" height="250"/>\n</div>\n\n## Example\n\nYou can see an example of how a working directory would look like [HERE](https://github.com/searleser97/competitive-programming-reference)\n\n## License\n\n```mkcpr``` is licensed under the GNU General Public License v3.0',
    'author': 'searleser97',
    'author_email': 'serchgabriel97@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/searleser97/mkcpr',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
