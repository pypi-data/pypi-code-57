# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywebcat']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.5,<2.0.0',
 'opencv-python>=4.2.0,<5.0.0',
 'pandas>=1.0.4,<2.0.0',
 'tqdm>=4.46.1,<5.0.0']

entry_points = \
{'console_scripts': ['pywebcat = pywebcat.cli:main']}

setup_kwargs = {
    'name': 'pywebcat',
    'version': '0.1.0',
    'description': 'Python tool for working with the NOAA NOS Web Camera Applications Testbed (WebCAT)',
    'long_description': '# PyWebCAT\n\n[![PyPI](https://img.shields.io/pypi/v/pywebcat)](\nhttps://pypi.org/project/pywebcat)\n[![Documentation Status](https://readthedocs.org/projects/pywebcat/badge/?version=latest)](https://pywebcat.readthedocs.io/en/latest/?badge=latest)\n\nThis repository provides a Pythonic way to interface with the NOAA National Ocean Service Web Camera Applications \nTestbed (WebCAT). The real-time data is hosted on the [SECOORA site](https://secoora.org) \n(The Southeast Coastal Ocean Observing Regional Association), on the dedicated [WebCAT page](https://secoora.org/webcat/).\nHistoric data can also be accessed by retrieving files using specific HTTP requests (using a pattern described on the \n[WebCAT page](https://secoora.org/webcat/)). \n\nMore details about WebCAT are available in this Open Access paper:\n\n>Dusek, G., Hernandez, D., Willis, M., Brown, J. A., Long, J. W., Porter, D. E., & Vance, T. C. (2019). WebCAT: Piloting the development of a web camera coastal observing network for diverse applications. Frontiers in Marine Science, 6, 353, 25 June 2019 | https://doi.org/10.3389/fmars.2019.00353\n\n## Install\n\n```{sh}\npip install pywebcat\n```\n\n## Usage\n\n### CLI\n\nA key workflow for utilising WebCAT videos is to split videos into frames for further analysis. As a result, this functionality is exposed as a CLI with the command line argument `pywebcat`.\n\n```{sh}\n$ pywebcat --help\nusage: webcat_utils.py [-h] -dir DIRECTORY -s STATION [STATION ...] -y YEAR\n                       [YEAR ...] -m MONTH [MONTH ...] -d DAY [DAY ...] -t\n                       TIME [TIME ...] [-i INTERVAL] [-n] [-v]\n\nCLI for saving frames of webCAT video(s).\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -i INTERVAL, --interval INTERVAL\n                        Interval in seconds between video frames to save\n                        (default: 10).\n  -n, --no_meta         Don\'t save .csv file of metadata of saved video\n                        frames.\n  -v, --verbose         Print program status.\n\nrequired arguments:\n  -dir DIRECTORY, --directory DIRECTORY\n                        Absolute path of directory to save frames in.\n  -s STATION [STATION ...], --station STATION [STATION ...]\n                        The station name, e.g., buxtoncoastalcam.\n  -y YEAR [YEAR ...], --year YEAR [YEAR ...]\n                        The video year(s), e.g., 2019 2020.\n  -m MONTH [MONTH ...], --month MONTH [MONTH ...]\n                        The video month(s), e.g., 9 10 11.\n  -d DAY [DAY ...], --day DAY [DAY ...]\n                        The video day(s) e.g., 1 11 21.\n  -t TIME [TIME ...], --time TIME [TIME ...]\n                        The video time(s), e.g., 1000 1330 1510.\n```\n\nThe CLI facilitates efficiently looping over input arguments to locate one or more WebCAT videos and split them into a desired number of frames which are then saved locally. Here\'s an example looping over several videos from the Buxton coastal camera on 13th Nov 2019 at different times (a 10 second interval is specified for saving the frames and verbosity is turned on):\n\n```{sh}\n$ pywebcat -dir /Users/tbeuzen/Downloads -s buxtoncoastalcam -y 2019 -m 11 -d 13 -t 1000 1210 1530 -i 100 -v\nSaving frames of buxtoncoastalcam_2019_11_13_1000...\n100%|██████████████████████████████████████████████| 62/62 [00:14<00:00,  4.22it/s]\nSaving frames of buxtoncoastalcam_2019_11_13_1210...\n100%|██████████████████████████████████████████████| 62/62 [00:13<00:00,  4.51it/s]\nSaving frames of buxtoncoastalcam_2019_11_13_1530...\n100%|██████████████████████████████████████████████| 62/62 [00:14<00:00,  4.38it/s]\n```\n\nThe resultant directory structure looks like:\n\n```{sh}\nUsers/tbeuzen/Downloads\n                └── buxtoncoastalcam\n                    ├── buxtoncoastalcam_2019_11_13_1000\n                    │   ├── buxtoncoastalcam_2019_11_13_1000.csv\n                    │   └── jpg\n                    │       ├── frame_0.jpg\n                    │       ├── frame_280.jpg\n                    │       ├── ...\n                    ├── buxtoncoastalcam_2019_11_13_1210\n                    │   ├── ...\n                    └── buxtoncoastalcam_2019_11_13_1530\n                        ├── ...\n```\n\nThe outputted .csv file contains metadata for the saved frames:\n\n| url        | name           | frame  | path|\n| ------------- |-------------| -----|---|\n|http://webcat-video.axds.co/buxtoncoastalcam/raw/2019/2019_11/2019_11_13/buxtoncoastalcam.2019-11-13_1000.mp4|buxtoncoastalcam_2019_11_13_1000|0|/Users/tbeuzen/Downloads/buxtoncoastalcam/buxtoncoastalcam_2019_11_13_1000/jpg/frame_0.jpg|\n|http://webcat-video.axds.co/buxtoncoastalcam/raw/2019/2019_11/2019_11_13/buxtoncoastalcam.2019-11-13_1000.mp4|buxtoncoastalcam_2019_11_13_1000|280|/Users/tbeuzen/Downloads/buxtoncoastalcam/buxtoncoastalcam_2019_11_13_1000/jpg/frame_280.jpg|\n|...|...|...|...|\n\n### Module\n\nThe pywebcat utilities can also be imported through the `pywebcat.utils` for use in other libraries or workflows. See the [demo Jupyter notebook](notebooks/pywebcat_demo.ipynb) for a worked example.\n\n```{python}\nfrom pywebcat.utils import WebCAT\nwc = WebCAT()\nwc.generate_url("buxtoncoastalcam", 2019, 11, 13, 1000)  # create the video url\n\n# attributes\nwc.url     # the created url\nwc.name    # unique name for the video object\nwc.width   # frame width in pixels\nwc.height  # frame height in pixels\nwc.frames  # total frames in video\nwc.fps     # frames per second\n\n# methods\nwc.download_url()        # download the video at the url\nwc.save_frames()         # save video frames as .jpg\nwc.plot_frames()         # plot select video frames\nwc.plot_average_frame()  # plot time-averaged frame\n```\n\n## Contributing\n\nContributions are welcome and greatly appreciated! If you\'re interested in contributing to this project, take a look at the [contributor guide](docs/contributing.rst).\n\n## Contributors\n\nAll contributions are welcomed and recognized! You can see a list of current contributors in the [contributors tab](https://github.com/UNCG-DAISY/WebCAT-Utilities/graphs/contributors).\n\n## Acknowledgements\n\nThanks to the [Southeast Coastal Ocean Observing Regional Association (SECOORA)and the WebCAT project](https://secoora.org/webcat/) for making camera footage publicly available and supporting open science and data.\n',
    'author': 'Tomas Beuzen',
    'author_email': 'tomas.beuzen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/UNCG-DAISY/WebCAT-Utilities',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
