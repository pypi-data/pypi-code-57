# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['nbmediasplit']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9,<5.0', 'click>=7.1,<8.0', 'lxml>=4.5,<5.0']

entry_points = \
{'console_scripts': ['nbmediasplit = nbmediasplit.nbmediasplit:main']}

setup_kwargs = {
    'name': 'nbmediasplit',
    'version': '0.2.0',
    'description': '',
    'long_description': '![pytest](https://github.com/wrist/nbmediasplit/workflows/pytest/badge.svg)\n\n# nbmediasplit\n\n`nbmediasplit` is a script to extract base64 encoded image and audio PCM embedded in .ipynb file and save them into specified directories.\n`nbmediasplit` also converts ipynb file to a new one which refers to stored image and audio files.\n\n## install\n\n`pip install nbmediasplit`\n\n## usage\n\n### extract image files from ipynb\n\n`nbmediasplit input.ipynb -i image_out_dir`\n\nor\n\n`nbmediasplit input.ipynb --imgdir image_out_dir`\n\nThe above command extract image files from `input.ipynb` and store them to `image_out_dir`.\n`-i` or `--imgdir` specifies a directory to store image files.\nFilenames of the stored image are numbered in sequential order(`0.png`, ...).\n\n### extract audio files from ipynb\n\n`nbmediasplit input.ipynb -w wav_out_dir`\n\nor\n\n`nbmediasplit input.ipynb --wavdir wav_out_dir`\n\nThe above command extract audio files from `input.ipynb` and store them to `wav_out_dir`.\n`-w` or `--wavdir` specifies a directory to store audio files.\nFilenames of the stored audio are numbered in sequential order(`0.wav`, ...).\n\n### extract image and audio files from ipynb\n\n`nbmediasplit input.ipynb -i image_out_dir -w wav_out_dir`\n\nor\n\n`nbmediasplit input.ipynb --imgdir image_out_dir --wavdir wav_out_dir`\n\nThe above command does below things.\n\n* extract image files from `input.ipynb` and store them to `image_out_dir`\n* extract audio files from `input.ipynb` and store them to `wav_out_dir`.\n\n`-i` or `--imgdir` specifies a directory to store image files.\n`-w` or `--wavdir` specifies a directory to store audio files.\nFilenames of the stored image are numbered in sequential order(`0.png`, ...).\nFilenames of the stored audio are numbered in sequential order(`0.wav`, ...).\n\n### extract image and audio files from ipynb and convert ipynb\n\nIf you use `-o` or `--output` option like below command,\nyou can convert `input.ipynb` to new ipynb file which refers to stored image files and audio files directly.\n\n`nbmediasplit input.ipynb -i image_out_dir -w wav_out_dir -o converted.ipynb`\n\nor\n\n`nbmediasplit input.ipynb --imgdir image_out_dir --wavdir wav_out_dir --output converted.ipynb`\n\nThe above command extract image files and audio files, and store them to specified directories, and generate new ipynb file `converted.ipynb`.\n`converted.ipynb` includes same content as `input.ipynb`, but base64 encoded image and audio data are replaced to HTML tag refers to stored files directly like below.\n\n* image tag\n    * `<img src="${image_out_dir}/${n}.png" />`\n* audio tag\n    * `<audio controls preload="none"><source  src="${wav_out_dir}/${n}.wav" type="audio/wav" /></audio>`\n\nAlso, you can use `--img-prefix` and `--wav-prefix` options.\nThese options can change the path embeded in src attribute of output html like below(actual files are stored `image_out_dir` and `wav_out_dir`).\n\n* image tag\n    * `<img src="${img-prefix}/${n}.png" />`\n* audio tag\n    * `<audio controls preload="none"><source  src="${wav-prefix}/${n}.wav" type="audio/wav" /></audio>`\n\n### show help\n\n`nbmediasplit --help`\n\n## note ##\n\nUnless you trust the notebook converted by nbmediasplit in jupyter, you can\'t load audio source because of html sanitization.\nTo trust notebook in jupyterlab, go to command pallet in the left sidebar(on osx, type `shift+cmd+c`) and execute `trust notebook`,\nthen you\'ll load audio source if the source path is correct.\n',
    'author': 'wrist',
    'author_email': 'stoicheia1986@gmail.com',
    'url': 'https://github.com/wrist/nbmediasplit',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
