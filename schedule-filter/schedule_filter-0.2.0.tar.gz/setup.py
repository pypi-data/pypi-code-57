"""
Publish a new version:
$ git tag X.Y.Z -m "Release X.Y.Z"
$ git push --tags
$ # edit setup.py for new version
$ pip install --upgrade twine wheel
$ python setup.py sdist bdist_wheel --universal
$ twine upload dist/*
"""
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = '0.2.0'
DOWNLOAD_URL = (
    'https://github.com/ruru4143/schedule_filter/' + VERSION
)

setup(
    name='schedule_filter',
    packages=['schedule_filter'],
    version=VERSION,
    url='https://github.com/ruru4143/schedule_filter',
    license='GPLv3',
    author='ruru4143',
    author_email='pypi@ruru.pw',
    description='Create advanced dbader/schedule with schedule-filters',
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url=DOWNLOAD_URL,
    keywords=[
        'schedule', 'periodic', 'jobs', 'scheduling', 'clockwork',
        'cron', 'scheduler', 'job scheduling'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Natural Language :: English',
    ],
)
