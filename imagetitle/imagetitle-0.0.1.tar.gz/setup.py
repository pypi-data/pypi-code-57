# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['imagetitle']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.1.2,<8.0.0',
 'dynaconf>=3.0.0rc1,<4.0.0',
 'filetype>=1.0.7,<2.0.0',
 'typer[all]>=0.2.1,<0.3.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.0,<2.0.0']}

entry_points = \
{'console_scripts': ['imagetitle = imagetitle.imagetitle:app']}

setup_kwargs = {
    'name': 'imagetitle',
    'version': '0.0.1',
    'description': ' Overlay image, top, bottom, left or right, with a title.',
    'long_description': '# Overlay Image Title\n\nThis is a tool, ```imagetitle```, to help overlay a small bit of text over an image.\n\nThis is especially useful to add some credits to images used in presentations for example.\n\n![Image with overlayed title at the bottom](readme-sample-output.png)\n\n```\nimagetitle -i input.png --title="This is title text." -p "bottom"\n```\n\nPhoto credits for the photo above goto **İrfan Simsar [https://unsplash.com/@irfansimsar]**\n\n## Usage\n\n```console\n$ imagetitle [OPTIONS]\n```\n\n**Options**:\n\n* `-i, --input PATH`: Image file name.  [default: input.png]\n* `-o, --output PATH`: Output file name.  [default: output.png]\n* `-p, --position [bottom|top|left|right]`: Where to position the tile.  [default: bottom]\n* `-t, --title TEXT`: Text for title.\n* `-f, --font TEXT`: Font name or path.\n* `-r, --fraction FLOAT RANGE`: What fraction, 0 to 1, of the image edge should be covered by the title?  [default: 0.75]\n* `--version`\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n\n\n## Installation\n\nThere are a number of ways you could install this utility.\n\n### Python\n\nIf you are familiar with the installation of python packages in a virtual environment then you can install with:\n\n```\npip install imagetitle\n```\n\nThis will give you a command line application that you can use at the terminal.\n\n#### Pipx\n\nAnother approach is to use a utility called [Pipx](https://pypi.org/project/pipx/) to install the application.\n\n```console\npipx install imagetitle\nor\npipx install git+https://github.com/rnwolf/overlay_image_title/\n```\n\n### Docker\n\nThe utility is also packaged up in a Docker [image](https://hub.docker.com/r/rnwolf/overlayimagetitle).\n\nIf you have docker installed then you can pull down the application and python all in one image.\n\n```\ndocker pull rnwolf/overlayimagetitle\n```\n\nTo show application help\n```docker run -t -i --rm -v ${PWD}:/app overlayimagetitle:latest```\n\nShow version\n```docker run -t -i --rm -v ${PWD}:/app overlayimagetitle:latest --version```\n\nGiven a file called input.png in current working dir then with this produce output.png in\n```docker run -t -i --rm -v ${PWD}:/app overlayimagetitle:latest -i /app/input.png -f /fnt/Ubuntu-C.ttf```\n\nOpen a bash shell inside of the docker container\n```docker run -t -i --rm --entrypoint /bin/bash -v ${PWD}:/app overlayimagetitle:latest```\n\n### Setup alias for Docker Image\n\nWhen using docker to run command setup a command alias for imagetitle\nIn your powershell profile add the following\n\n```\nfunction imagetitle {\n  docker run -it --rm v ${pwd}:/app overlayimagetitle:latest $args\n }\n ```\n\nOr if you use bash terminal then update .bashrc profilr by adding:\n\n```alias imagetitle=\'docker run -it --rm -v \\`pwd\\`:/app overlayimagetitle:latest\'```\n',
    'author': 'Rudiger Wolf',
    'author_email': 'Rudiger.Wolf@ThroughputFocus.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://rnwolf.github.io/imagetitle/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
