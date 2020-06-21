# minimal setup.py to install in develop mode

from setuptools import setup, find_packages

REQUIRED_MODULES = [
    'numpy',
    'Pillow',
    'PySide2'
]

from saqqarah import version

__version__ = version()

# read the contents of the README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="saqqarah",
    version=__version__,
    long_description=long_description,
    long_description_content_type='text/markdown',   
    author="Yves Combe",
    author_email="yves@ycombe.net",
    url = "https://framagit.org/ycombe/saqqarah",
    description="Calculation pyramid generator",
    packages=find_packages(),
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Console',
                 'Environment :: X11 Applications :: Qt',
                 'Intended Audience :: Education',
                 'License :: DFSG approved',
                 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                 'Topic :: Education',
                 ],
    package_data={'': ['fonts/*.ttf', 'ui/*.ui', '*.txt', 'LICENSE']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'saqqarah = saqqarah.__main__:main',
        ],
        'gui_scripts' : [
            'saqqarahW = saqqarah.__QT5__:main'
        ]
    },
    install_requires=REQUIRED_MODULES,
    python_requires='>=3.6',
    keywords=["mathematics", "addition", "pyramid","school"]
    )
