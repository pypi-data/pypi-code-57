# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nothing_cli', 'nothing_cli.localization', 'nothing_cli.tests']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0',
 'pydantic>=1.4,<2.0',
 'python-slugify>=4.0.0,<5.0.0',
 'ruamel.yaml>=0.16.10,<0.17.0',
 'typer>=0.1.0,<0.2.0',
 'typing-extensions>=3.7.4,<4.0.0']

entry_points = \
{'console_scripts': ['not = nothing_cli.main:app']}

setup_kwargs = {
    'name': 'nothing-cli',
    'version': '0.1.0',
    'description': 'Nothing helps coder be more smarter & less dumber.',
    'long_description': '# Nothing (`not`)\n\nNothing help coder be more smarter, some cooler, less dumber. `not`.\n\n## Inspo & Rationale\n\nOnce upon a time we all read this brief article about ["do-nothing scripting"](https://blog.danslimmon.com/2019/07/15/do-nothing-scripting-the-key-to-gradual-automation/).\n\nVery cool, but even those scripts take time!\n\n[Juxtapose OG example against Recipe version]\n\nMore why:\n\n- Ease automation woes (dotfile scripts lol). Clip your wax wings early before you try to build robots.\n- Fast to use! Build these things rampantly at the project level\n    - Attach them to commit hooks?\n    - Keep yourself accountable\n    - Bring consistency to things u do often\n- Shareable\n\n## Sample\n\nConfigure your Recipe as simple yaml mixed with simple Python templating:\n\n```yaml\n---\ntitle: A sample set of do-nothing instructions\n\n# the user will be prompted to provide these values\n# and the values will persist through the run\ncontext:\n  - current_user_name\n  - what_user_accomplished_today\n\n# a set of steps is most easily represented as block scalar\n# each step is simply denoted as a line break\n# plain python templates are used to interpolate context\nsteps: |-\n  Take a good look at yourself, {current_user_name}.\n\n  I heard you accomplished something great today: {what_user_accomplished_today}.\n  Give yourself a pat on the back!\n\n# https://yaml-multiline.info/#block-scalars\n```\n\nRun it like so:\n\n```shell\nnot do sample\n```\n\nWant a new one?\n\n```shell\nnot new preflight-checks\n# drops you into your $EDITOR if that\'s set\n```\n\nDidn\'t like how it turned out? That\'s fine.\n\n```shell\nnot edit preflight-checks\n```\n\n## Bigger Example\n\n- Uses dictionary syntax in context\n- Higher config\n\n## Features\n\n### Stylish & Modern\n\n- Pleasant interactivity a-la the Nicest CLI tools\n- Colorful & playful since `work_smart == work_less == play_more`\n- Funky (but standard), highly readable YAML format\n- High config\n    - (Give much more thought to where how & when)\n\n### Saving your sweet nothings\n\n- Can be in a project-specific `.nothing/` directory\n- or system level `~/.nothing`\n- or as a local `*.not` file\n',
    'author': 'Ainsley McGrath',
    'author_email': 'mcgrath.ainsley@gmail.com',
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
