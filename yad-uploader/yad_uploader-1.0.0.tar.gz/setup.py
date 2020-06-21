from setuptools import setup, find_packages

import yad_uploader


setup(
    name='yad_uploader',
    version=yad_uploader.__version__,
    author='ruzzy',
    author_email='ruslan@lemimi.ru',
    packages=find_packages(),
    package_dir={'yad_uploader': 'yad_uploader'},
    install_requires=[
        'telegram-log==1.0.12',
        'yadisk==1.2.14'
    ],
)
