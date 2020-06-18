import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / 'README.md').read_text()

setup(
    name = 'mypassword',
    packages = ['mypassword'],
    version = '0.1.2',
    description = 'Tools for generating strong passwords',
    long_description=README,
    long_description_content_type='text/markdown',
    author = 'Vicente Gutiérrez',
    author_email = 'vinzegtz@gmail.com',
    url = 'https://github.com/vinzegtz/mypassword',
    download_url = 'https://github.com/vinzegtz/mypassword/archive/v0.1.2-beta.tar.gz',
    keywords = ['password', 'pass', 'password-manager'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)