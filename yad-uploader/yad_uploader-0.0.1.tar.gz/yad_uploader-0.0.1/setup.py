from setuptools import setup, find_packages

from __init__ import __version__

setup(
    name='yad_uploader',
    version=__version__,
    author='Ruzzy Rullezz',
    author_email='ruslan@lemimi.ru',
    packages=find_packages(),
    package_dir={'yad_uploader': 'yad_uploader'},
    install_requires=[
        'telegram-log==1.0.12',
        'yadisk==1.2.14'
    ],
)
