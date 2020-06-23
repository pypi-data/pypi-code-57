#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages, Command
from sys import platform as _platform
from shutil import rmtree
import sys
import os

here = os.path.abspath(os.path.dirname(__file__))
NAME = 'labelStoma'
REQUIRES_PYTHON = '>=3.0.0'
REQUIRED_DEP = ['pyqt5', 'lxml','imutils==0.5.1','tqdm==4.31.0','opencv_python==4.1.2.30','XlsxWriter==1.2.6','six==1.11.0','numpy']
about = {}

with open(os.path.join(here, 'libs', '__init__.py')) as f:
    exec(f.read(), about)

readme = ""
#with open('README.md') as readme_file:
#    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


# OS specific settings
SET_REQUIRES = []
if _platform == "linux" or _platform == "linux2":
   # linux
   print('linux')
elif _platform == "darwin":
   # MAC OS X
   SET_REQUIRES.append('py2app')

required_packages = find_packages()
required_packages.append('labelStoma')
required_packages.append('notebooks')
required_packages.append('predict')
required_packages.append('fichs')
required_packages.append('resources/strings')
required_packages.append('resources/icons')

APP = [NAME + '.py']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'resources/icons/app.icns'
}

class UploadCommand(Command):
    """Support setup.py upload."""

    description=readme + '\n\n' + history,

    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            self.status('Fail to remove previous builds..')
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system(
            '{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag -d v{0}'.format(about['__version__']))
        os.system('git tag v{0}'.format(about['__version__']))
        # os.system('git push --tags')

        sys.exit()


setup(
    app=APP,
    name=NAME,
    version="0.1.17",
    description="labelStoma is a graphical tool for using and creating detection stoma models",
    long_description="labelStoma is a graphical tool for using and creating detection stoma models",
    author="Angela Casado",
    author_email='angela.casado@unirioja.es',
    url='https://github.com/ancasag/labelStoma',
    python_requires=REQUIRES_PYTHON,
    package_dir={'labelStoma': '.'},
    packages=required_packages,
    entry_points={
        'console_scripts': [
            'labelStoma=labelStoma.labelStoma:main'
        ]
    },
    include_package_data=True,
    install_requires=REQUIRED_DEP,
    license="MIT license",
    zip_safe=False,
    keywords='labelStoma detection deeplearning',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    package_data={'data/predefined_classes.txt': ['data/predefined_classes.txt'],'notebooks': ['notebooks/*.ipynb'],
'fichs/vocEstomas.names': ['fichs/vocEstomas.names'],'fichs/yolov3Estomas.cfg': ['fichs/yolov3Estomas.cfg'],'resources/strings': ['resources/strings/*'],'resources/icons': ['resources/icons/*']},
    options={'py2app': OPTIONS},
    setup_requires=SET_REQUIRES,
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    }
)
