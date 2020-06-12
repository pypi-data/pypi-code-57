# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iscc_cli', 'iscc_cli.commands', 'iscc_cli.tika']

package_data = \
{'': ['*']}

install_requires = \
['click-default-group>=1.2,<2.0',
 'click>=7.0,<8.0',
 'colorama>=0.4,<0.5',
 'imageio-ffmpeg>=0.4,<0.5',
 'iscc==1.0.5',
 'lxml>=4.4,<5.0',
 'mobi>=0,<1',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['iscc = iscc_cli.cli:cli']}

setup_kwargs = {
    'name': 'iscc-cli',
    'version': '0.9.11',
    'description': 'ISCC CLI - Creates ISCC Codes from Media Files',
    'long_description': '# iscc-cli  - Command Line Tool\n\n[![Linux/Windows/macOS Tests](https://github.com/iscc/iscc-cli/workflows/Tests/badge.svg)](https://github.com/iscc/iscc-cli/actions?query=workflow%3ATests)\n[![Version](https://img.shields.io/pypi/v/iscc-cli.svg)](https://pypi.python.org/pypi/iscc-cli/)\n[![Downloads](https://pepy.tech/badge/iscc-cli)](https://pepy.tech/project/iscc-cli)\n\n> A command line tool that creates **ISCC Codes** for digital media files based on the [reference implementation](<https://github.com/iscc/iscc-specs>).\n\n## Table of Contents\n\n- [Background](#background)\n- [Install](#install)\n- [Usage](#usage)\n- [Maintainers](#maintainers)\n- [Contributing](#contributing)\n- [License](#license)\n\n## Background\n\nThe **International Standard Content Code** is a proposal for an [open standard](https://en.wikipedia.org/wiki/Open_standard) for decentralized content identification. **ISCC Codes** are generated algorithmically **from the content itself** and offer many powerful features like content similarity clustering and partial integrity checks. If you want to learn more about the **ISCC** please check out https://iscc.codes.\n\nThis tool offers an easy way to generate ISCC codes from the command line. It supports content extraction via [Apache Tika](https://tika.apache.org/) and uses the [ISCC reference implementation](https://github.com/iscc/iscc-specs).\n\n\n### Supported Media File Types\n\n#### Text\n\ndoc, docx, epub, html, odt, pdf, rtf, txt, xml, ibooks, md, xls, mobi ...\n\n\n#### Image\n\ngif, jpg, png, tif, bmp, psd, eps ...\n\n**Note**: EPS (postscript) support requires [Ghostscript](https://www.ghostscript.com/download.html) to be installed on your system and available on your PATH. (Make sure you can run `gs` from your command line.)\n\n\n#### Audio\n\naif, mp3, ogg, wav ...\n\n\n**Note**: Support for the Audio-ID is experimentel and not yet part of the [specification](https://iscc.codes/specification/)\n\n\n#### Video\n\n3gp, 3g2, asf, avi, flv, gif, mpg, mp4, mkv, mov, ogv, webm, wmv ...\n\n\n**Note**: Support for the Video-ID is experimentel and not yet part of the [specification](https://iscc.codes/specification/)\n\n## Requirements\n\n| NOTE: Requires JAVA to be installed and on your path! |\n| --- |\n\n**iscc-cli** is tested on Linux, Windows, and macOS with Python 3.6/3.7/3.8.\n\nThis tool depends on [tika-python](https://github.com/chrismattmann/tika-python).  [Tika](https://tika.apache.org/) is used for extracting metadata and content from media files before generating ISCC Codes. On first execution of the `iscc` command line tool it will automatically download and launch the Java Tika Server in the background (this may take some time). Consecutive runs will access the existing Tika instance. You may explicitly pre-launch the Tika server with `$ iscc init`\n\n## Install\n\nThe ISCC command line tool is published with the package name `iscc-cli` on the [Python Package Index](https://pypi.python.org/pypi/iscc-cli) and can be installed with pip:\n\n```console\n$ pip3 install iscc-cli\n```\n\nSelf-contained Windows binary executables are available for download at:\n<https://github.com/iscc/iscc-cli/releases/>\n\n## Usage\n\n### Getting Help\n\nShow help overview by calling `iscc` without any arguments:\n\n```console\n$ iscc\nUsage: iscc [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --version  Show the version and exit.\n  --help     Show this message and exit.\n\nCommands:\n  gen*   Generate ISCC Code for FILE.\n  batch  Create ISCC Codes for all files in PATH.\n  dump   Dump Tika extraction results for PATH (file or url path).\n  info   Show information about environment.\n  init   Inititalize and check environment.\n  sim    Estimate Similarity of ISCC Codes A & B.\n  test   Test conformance with latest reference data.\n  web    Generate ISCC Code from URL.\n```\n\nGet help for a specific command by entering `iscc <command>`:\n\n```console\n$ iscc gen\nUsage: iscc gen [OPTIONS] FILE\n\n  Generate ISCC Code for FILE.\n\nOptions:\n  -g, --guess       Guess title (first line of text).\n  -t, --title TEXT  Title for Meta-ID creation.\n  -e, --extra TEXT  Extra text for Meta-ID creation.\n  -v, --verbose     Enables verbose mode.\n  -h, --help        Show this message and exit.\n```\n\n### Generating ISCC Codes\n\n#### For local files\n\nThe `gen` command generates an ISCC Code for a single file:\n\n```console\n$ iscc gen tests/image/demo.jpg\nISCC:CC1GG3hSxtbWU-CYDfTq7Qc7Fre-CDYkLqqmQJaQk-CRAPu5NwQgAhv\n```\n\nThe `gen` command is default so you can skip it and simply do `$ iscc tests/demo.jpg`\n\nTo get a more detailed result use the `-v` (`--verbose`) option:\n\n```console\n$ iscc -v tests/image/demo.jpg\nISCC:CC1GG3hSxtbWU-CYDfTq7Qc7Fre-CDYkLqqmQJaQk-CRAPu5NwQgAhv\nNorm Title: concentrated cat\nTophash:    7a8d0c513142c45f417e761355bf71f11ad61d783cd8958ffc0712d00224a4d0\nFilepath:   tests/image/demo.jpg\nGMT:        image\n```\n\nSee `iscc batch` for help on how to generate ISCC codes for multiple files at once.\n\n#### For web urls\n\nThe `web` command allows you to create ISCC codes from URLs:\n\n```console\n$ iscc web https://iscc.foundation/news/images/lib-arch-ottawa.jpg\nISCC:CCbUCUSqQpyJo-CYaHPGcucqwe3-CDt4nQptEGP6M-CRestDoG7xZFy\n```\n\n### Similarity of ISCC Codes\n\nThe `sim` command computes estimated similarity of two ISCC Codes:\n\n```console\n$ iscc sim CCUcKwdQc1jUM CCjMmrCsKWu1D\nEstimated Similarity of Meta-ID: 78.00 % (56 of 64 bits match)\n```\n\nYou may also compare full four-component ISCC Codes.\n\n### Using from your python code\n\nWhile this package is not built to be used as a library, some of the high level commands to generate ISCC Codes are exposed as vanilla python functions:\n\n```python\nfrom iscc_cli import lib\nfrom pprint import pprint\n\npprint(lib.iscc_from_url("https://iscc.foundation/news/images/lib-arch-ottawa.jpg"))\n\n{\'gmt\': \'image\',\n \'iscc\': \'CCbUCUSqQpyJo-CYaHPGcucqwe3-CDt4nQptEGP6M-CRestDoG7xZFy\',\n \'norm_title\': \'library and archives canada ottawa\',\n \'tophash\': \'e264cc07209bfaecc291f97c7f8765229ce4c1d36ac6901c477e05b2422eea3e\'}\n```\n\n## Maintainers\n\n[@titusz](https://github.com/titusz)\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\nYou may also want join our developer chat on Telegram at <https://t.me/iscc_dev>.\n\n## Change Log\n\n### [0.9.11] - 2020-06-12\n- Update dependencies\n- Remove support for creating ISCC codes from youtube urls\n\n### [0.9.10] - 2020-05-19\n- Fixed issue with mime-type detection\n- Changed wording of similarity output\n- Added CSV-compatible output for batch command\n- Added debug option for batch command\n- Updated dependencies\n\n### [0.9.9] - 2020-05-18\n- Fixed issue with tika & macOS\n- Added macOS ci testing\n- Updated dependencies\n\n### [0.9.8] - 2020-05-13\n- Updated Content-ID-Audio for robustness against transcoding (breaking change)\n- Changed similarity calculation to match with web demo\n- Fixed bug in mime-type detection\n- Updated dependencies\n\n### [0.9.7] - 2020-05-01\n- Add support for flac and opus audio formats\n- Update dependencies\n\n### [0.9.6] - 2020-04-24\n- Support urls with dump command\n- Updated tika 1.24 and fpcalc 1.50\n- Use filename for meta-id as last resort\n- Switch to signed audio fingerprint (breaking change)\n- Bugfixes and stability improvements\n\n### [0.9.5] - 2020-03-02\n- Support mobi7\n- Support mobi print replica\n- Support mobi with web command\n\n### [0.9.4] - 2020-03-02\n- Add experimental support for mobi files\n\n### [0.9.3] - 2020-02-18\n- Add support for XHTML\n- Fix error on unsupported media types\n\n### [0.9.2] - 2020-01-30\n- Add support for bmp, psd, xls, xlsx\n- Add tika server live testing\n- Fix error with title guess on image files\n\n### [0.9.1] - 2020-01-05\n- Fix issue with APP_DIR creation\n\n### [0.9.0] - 2020-01-05\n- Add experimental support for Video-ID\n- Add special handling of YouTube URLs\n- Add support for more Media Types (try & error)\n- Add support for Python 3.8\n- Remove support for Python 3.5\n\n### [0.8.2] - 2019-12-22\n- Add new `test` command for confromance testing\n- Add support for .md (Markdown) files\n- Update to ISCC v1.0.5\n- Update to Apache Tika 1.23\n- Fix issue with non-conformant Meta-ID\n\n### [0.8.1] - 2019-12-13\n- Add support for tif files\n- Add support for eps files\n- Set application directory to non-roaming path\n\n### [0.8.0] - 2019-11-23\n- Add new `dump` command (dumps extraction results)\n- Add support for iBooks files\n- Fix error with tika 1.22 dependency\n- Store tika server in non-volatile storage\n\n### [0.7.0] - 2019-09-12\n- Expose commands as python API\n- Fix title guessing bug\n\n### [0.6.0] - 2019-06-11\n\n- Added new `web` command (creates ISCC Codes for URLs)\n\n### [0.5.0] - 2019-06-06\n\n- Added experimental support for aif, mp3, ogg, wav\n- More verbose batch output\n- Fix batch output default Meta-ID\n\n### [0.4.0] - 2019-06-03\n\n- Added support for html, odt, txt, xml, gif\n- Added optional guessing of title (first line of text)\n- Added new `info` command\n- Fixed wrong detection of identical Instance-ID\n\n### [0.3.0] - 2019-06-01\n\n- Add `sim` command similarity comparison of ISCC Codes\n\n### [0.2.0] - 2019-05-31\n\n- Add support for doc, docx and rtf documents\n- Update to ISCC 1.0.4 (fixes whitespace bug)\n\n### [0.1.0] - 2019-05-31\n\n- Basic ISCC Code creation\n- Supported file types: jpg, png, pdf, epub\n\n## License\n\nMIT © 2019-2020 Titusz Pan\n\n',
    'author': 'Titusz Pan',
    'author_email': 'tp@py7.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://iscc.codes/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
