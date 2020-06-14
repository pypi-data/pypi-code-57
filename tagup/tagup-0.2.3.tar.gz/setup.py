# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tagup']

package_data = \
{'': ['*']}

install_requires = \
['lark-parser>=0.8.5,<0.9.0']

setup_kwargs = {
    'name': 'tagup',
    'version': '0.2.3',
    'description': 'Reference implementation of the Tagup Language',
    'long_description': '![Travis (.org) branch](https://img.shields.io/travis/Foxbud/tagup/master?label=master&style=flat-square)\n&nbsp;\n![Codecov branch](https://img.shields.io/codecov/c/github/Foxbud/tagup/master?style=flat-square)\n\n# tagup\n\n**tagup** is a Python module which provides a reference implementation of the [Tagup Language](https://fairburn.dev/tagup/).\n\nThis module currently implements [version 1.0.0](https://fairburn.dev/tagup/1.0.0/) of the Tagup Language.\n\n## Quick Start\n\n```python\nfrom tagup import BaseRenderer, TagDictMixin\n\n\nclass TagupRenderer(TagDictMixin, BaseRenderer):\n    pass\n\n\nrenderer = TagupRenderer(\n    # Optional initial markup tags.\n    tags={\n        \'bold\': r\'<span style="font-weight: bold">[\\\\1]</span>\',\n    }\n)\n\n# Manipulate tags using dictionary syntax.\nrenderer[\'link\'] = (\n    r\'<a href="[\\\\1]" [\\if target\\target="_[\\\\target]"]>\'\n    r\'[bold [\\if 2\\[\\\\2]\\[\\\\1]]]\'\n    r\'</a>\'\n)\n\nhtml = renderer.render_markup(\n    r\'Click [link target\\\\blank\\[\\\\url]\\here] to visit [link\\[\\\\url]]\',\n    # Provide optional named (and positional) arguments.\n    named_args={\'url\': \'http://example.com\'}\n)\nprint(html)\n```\n\n## Changelog\n\n**v0.2.3**\n\n- Added "StaticTagMixin," "TagDictMixin" and "TrimMixin" for "BaseRenderer."\n- Added new errors "ImproperlyConfigured," "NamedArgumentMissing," "PositionalArgumentMissing," "TagNotFound" and "TagupSyntaxError."\n- Renamed "stack_trace" to "tag_stack_trace" for all custom errors.\n- Fixed bug in getitem method of "TagStackTrace."\n\n**v0.2.2**\n\n- Added support for global named arguments.\n- Added max tag depth enforcement.\n- Fixed bug that prevented the positional loop from functioning when not provided an optional default value.\n\n**v0.2.1**\n\n- Added tag prefetching.\n\n**v0.2.0**\n\n- Renamed "Renderer" to "BaseRenderer."\n- Refactored "BaseRenderer" to use method overriding for "get_tag" instead of providing "get_tag_callback" to constructor.\n- Removed "cache_tag_ast_callback" from "BaseRenderer" constructor.\n- Removed "trim_args" from "BaseRenderer" constructor.\n- Added a node pre and post processing hook system.\n- Added test cases.\n- Various internal optimizations.\n\n**v0.1.3**\n\n- Fixed bug where the "trim_args" option didn\'t properly remove leading and trailing whitespace in some situations.\n\n**v0.1.2**\n\n- Fixed bug where code called "trim()" rather than "strip()."\n\n**v0.1.1**\n\n- Added non-standard option to trim whitespace from arguments before tag evaluation.\n- Fixed bug where whitespace was considered when specifying a name/position for argument substitution.\n\n**v0.1.0**\n\n- Initial release.\n',
    'author': 'Garrett Fairburn',
    'author_email': 'garrett@fairburn.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://fairburn.dev/tagup/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
