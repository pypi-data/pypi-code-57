#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.app.ydl',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20200621',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  description =
    'Convenient command line and library wrapper for youtube-dl.',
  long_description =
    ('Convenient command line and library wrapper for youtube-dl.\n'    
 '\n'    
 '*Latest release 20200621*:\n'    
 '* YDL.run: just catch the youtube_dl DownloadError.\n'    
 '* Changes to the default output filename template.\n'    
 '* Other minor internal changes.\n'    
 '\n'    
 'The `youtube-dl` tool and associated `youtube_dl` Python module\n'    
 'are very useful for downloading media from various websites.\n'    
 'However, as an end user who almost never streams because of my\n'    
 'soggy internet link, I find fetching several items is quite serial and\n'    
 'visually noisy.\n'    
 '\n'    
 'This module provides a command line tool `ydl` which:\n'    
 '- runs multiple downloads in parallel with progress bars\n'    
 '- prints the downloaded filename as each completes\n'    
 '\n'    
 'Interactively, I keep this shell function:\n'    
 '\n'    
 '    ydl(){\n'    
 '      ( set -ue\n'    
 '        dldir=${DL:-$HOME/dl}/v\n'    
 '        [ -d "$dldir" ] || set-x mkdir "$dldir"\n'    
 '        cd "$dldir"\n'    
 '        command ydl ${1+"$@"}\n'    
 '      )\n'    
 '    }\n'    
 '\n'    
 'which runs the downloader in my preferred download area\n'    
 'without tedious manual `cd`ing.\n'    
 '\n'    
 '## Function `main(argv=None, cmd=None)`\n'    
 '\n'    
 'Main command line.\n'    
 '\n'    
 '## Class `OverYDL`\n'    
 '\n'    
 'A manager for multiple `YDL` instances.\n'    
 '\n'    
 '## Class `YDL`\n'    
 '\n'    
 'Manager for a download process.\n'    
 '\n'    
 '### Method `YDL.__init__(self, url, *, fstags, upd=None, tick=None, '    
 'over_progress=None, **kw_opts)`\n'    
 '\n'    
 'Initialise the manager.\n'    
 '\n'    
 'Parameters:\n'    
 '* `url`: the URL to download\n'    
 '* `fstags`: mandatory keyword argument, a `cs.fstags.FSTags` instance\n'    
 '* `upd`: optional `cs.upd.Upd` instance for progress reporting\n'    
 '* `tick`: optional callback to indicate state change\n'    
 '* `over_progress`: an `OverProgress` to which to add each new `Progress` '    
 'instance\n'    
 '* `kw_opts`: other keyword arguments are used to initialise\n'    
 '  the options for the underlying `YoutubeDL` instance\n'    
 '\n'    
 '## Class `YDLCommand(cs.cmdutils.BaseCommand)`\n'    
 '\n'    
 '`ydl` command line implementation.\n'    
 '\n'    
 '\n'    
 'Command line usage:\n'    
 '\n'    
 '    Usage: YDLCommand [-f] {URLs|-}...\n'    
 '        -f  Force download - do not use the cache.\n'    
 '\n'    
 '# Release Log\n'    
 '\n'    
 '\n'    
 '\n'    
 '*Release 20200621*:\n'    
 '* YDL.run: just catch the youtube_dl DownloadError.\n'    
 '* Changes to the default output filename template.\n'    
 '* Other minor internal changes.\n'    
 '\n'    
 '*Release 20200615.1*:\n'    
 'Add usage message to docstring.\n'    
 '\n'    
 '*Release 20200615*:\n'    
 '* Initial "daemon" mode, suitable for "tail -f .ydld-queue | ydl -", handy '    
 'for keeping around in a tmux session.\n'    
 '* Assorted small bugfixes.\n'    
 '\n'    
 '*Release 20200521*:\n'    
 'Initial PyPI release.'),
  classifiers = ['Development Status :: 4 - Beta', 'Environment :: Console', 'Operating System :: POSIX', 'Operating System :: Unix', 'Programming Language :: Python', 'Programming Language :: Python :: 3', 'Topic :: Internet', 'Topic :: System :: Networking', 'Topic :: Utilities', 'Intended Audience :: Developers', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  entry_points = {'console_scripts': ['ydl = cs.app.ydl:main']},
  install_requires = ['cs.cmdutils', 'cs.fstags', 'cs.logutils', 'cs.result', 'cs.tagset', 'cs.upd', 'youtube_dl'],
  keywords = ['python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.app.ydl'],
)
