# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cvlog']

package_data = \
{'': ['*']}

install_requires = \
['opencv-python>=3.3']

setup_kwargs = {
    'name': 'opencv-log',
    'version': '1.4.0',
    'description': 'OpenCV based visual logger for debugging,logging and testing image processing code',
    'long_description': '.. figure:: https://user-images.githubusercontent.com/20145075/78172497-c8f85380-7473-11ea-9eb6-8963fc879a42.png\n\n.. image:: https://img.shields.io/pypi/v/opencv-log.svg\n   :target: https://pypi.org/project/opencv-log\n   :alt: Pypi Version \n.. image:: https://img.shields.io/circleci/build/github/navarasu/opencv-log\n   :target: https://circleci.com/gh/navarasu/opencv-log\n   :alt: Build Status\n.. image:: https://img.shields.io/coveralls/github/navarasu/opencv-log/master\n   :target: https://coveralls.io/github/navarasu/opencv-log?branch=master\n   :alt: Coverage Status\n.. image:: https://img.shields.io/pypi/l/opencv-log\n   :target: https://github.com/navarasu/opencv-log/blob/master/LICENSE\n   :alt: MIT License\n\n|\n\nAn `OpenCV <https://opencv.org/>`_ based visual logger for debugging, logging and testing reporting an image processing code.\n\nWhy opencv-log?\n###############\n\n.. image:: https://user-images.githubusercontent.com/20145075/81455232-3eaaba00-91ac-11ea-9213-7dd1c705f213.png\n   :target: https://blog.francium.tech/visually-debug-log-and-test-an-image-processing-code-using-opencv-and-python-36e2d944ebf2\n   :alt: Visually Debug, Log and Test an Image Processing Code using OpenCV and Python\n\nInstallation\n############\nUse the package manager `pip <https://pip.pypa.io/en/stable/>`_ to install.\n\n.. code-block:: sh\n\n   pip install opencv-log\n\n\n**Documentation:**  `<https://navarasu.github.io/opencv-log>`_\n\nA Simple Usage\n##############\n\n.. code-block:: python\n\n   import cvlog as log\n   import cv2\n\n   # image read using opencv\n   img = cv2.imread("sample.png")\n\n   log.image(log.Level.ERROR, img)\n\nJust by switching mode, you can use the same line of code for logging and debugging. \nAlso you can log houghlines, countour and more.\n\nRefer `docs <https://navarasu.github.io/opencv-log>`_ to get started.\n\nContributing\n############\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\nRefer `Guidelines <https://github.com/navarasu/opencv-log/blob/master/CONTRIBUTION.md>`_ for more information.\n\nLicense\n#######\n\n`MIT <https://choosealicense.com/licenses/mit/>`_\n',
    'author': 'Navarasu',
    'author_email': 'navarasu@outlook.com',
    'url': 'https://navarasu.github.io/opencv-log',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
