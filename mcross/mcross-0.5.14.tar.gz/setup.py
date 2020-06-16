# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mcross', 'mcross.gui']

package_data = \
{'': ['*']}

install_requires = \
['curio>=1.2,<2.0']

entry_points = \
{'console_scripts': ['mcross = mcross:run']}

setup_kwargs = {
    'name': 'mcross',
    'version': '0.5.14',
    'description': 'Do you remember www?',
    'long_description': 'McRoss is a minimal and usable [gemini://](https://gemini.circumlunar.space/)\nbrowser written in python and tkinter, meaning it Just Works (tm) on any\nself-respecting desktop OS: Linux, Windows, Mac OS, and maybe the BSDs?\nNever tried one of those.\n\nIt currently looks like this:\n\n![](https://junk.imnhan.com/mcross.png)\n\nSurfing plaintext and gemini content is already working well. The catch is it\ncurrently doesn\'t support downloading binary content and TOFU TLS verification.\nSee feature checklist below for more details.\n\nSee my [blog post][1] for the rationale behind this project.\n\n\n# Installation\n\nYou need python 3.7 or higher. McRoss also uses `idlelib` which is supposed to\nbe included in the standard library but some linux distros split it into a\nseparate package which you\'ll need to install manually. I know at least [Ubuntu\nand Void Linux][2] do this.\n\n```sh\npip install mcross\nmcross\n```\n\nBetter distribution methods to be explored later.\nMaybe it\'s finally time to try nuitka?\n\n# Usage\n\nCLI arguments: `--textfont`, `--monofont`\n\nKeyboard shortcuts:\n\n- `Ctrl-l`: jump to address bar.\n- Hold `Alt` to see possible button shortcuts underlined. This is what Qt calls\n  [Accelerator Keys](https://doc.qt.io/qt-5/accelerators.html).\n\n\n# Development\n\nTo get started:\n\n```sh\npyenv install 3.7.7\npyenv virtualenv 3.7.7 mcross\npyenv activate\npoetry install\nmcross\n\n# to publish, first bump version in pyproject.toml then\npoetry publish --build\n```\n\nThere are 2 McRoss-related mailing lists:\n\n- [~nhanb/mcross-devel](https://lists.sr.ht/~nhanb/mcross-devel): discuss and\n  submit your patches here\n- [~nhanb/mcross-announce](https://lists.sr.ht/~nhanb/mcross-announce):\n  low-volume announcement-only list\n\nIf you\'re not familiar with the mailing list workflow, check out\n[git-send-email.io][3] and [mailing list etiquette][4]. [useplaintext.email][5]\nalso has useful plaintext setup tips for various email clients, though I don\'t\nnecessarily agree with its "plaintext or nothing" stance.\n\n\n# Feature checklist\n\n- [x] back-forward buttons\n- [x] handle redirects\n- [x] non-blocking I/O using curio\n- [x] more visual indicators: waiting cursor, status bar\n- [x] parse gemini\'s advanced line types\n- [ ] properly handle mime types (gemini/plaintext/binary)\n- [ ] configurable document styling\n- [ ] human-friendly distribution\n- [ ] TOFU TLS (right now it always accepts self-signed certs)\n\nLong term high-level goals:\n\n## Easy for end users to install\n\nIf the words `cargo build` exists in the installation guide for your G U I\napplication then I\'m sorry it\'s not software made for people to _use_.\n\n## What-you-see-is-what-you-write\n\nA rendered text/gemini viewport should preserve its original text content.\nThis way once you\'ve read a gemini page on the browser, you already know how to\nwrite one. No "View Source" necessary.\n\n## Responsive & pleasant to use\n\nThe Castor browser doesn\'t have visual indicators at all, for example, when\nclicking on a link it just appears to do nothing until the new page is\ncompletely loaded. That is A Bad Thing (tm).\n\n## Lightweight\n\nIn terms of both disk space & memory/cpu usage.\nThe python/tkinter combo already puts us at a pretty good starting point.\n\n# Server bugs/surprises\n\n## Forces gemini:// in request\n\nSpec says protocol part is optional, but if I omit that one the server will\nrespond with `53 No proxying to other hosts!`.\n\n## Newline\n\nSpec says a newline should be \\r\\n but the server running\ngemini.circumlunar.space just uses \\n every time.\n\n[1]: https://hi.imnhan.com/posts/introducing-mcross-a-minimal-gemini-browser/\n[2]: https://todo.sr.ht/~nhanb/mcross/3\n[3]: https://git-send-email.io/\n[4]: https://man.sr.ht/lists.sr.ht/etiquette.md\n[5]: https://useplaintext.email/\n',
    'author': 'nhanb',
    'author_email': 'hi@imnhan.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://sr.ht/~nhanb/mcross/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
