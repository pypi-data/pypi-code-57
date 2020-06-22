#!/usr/bin/env python

#  © Copyright IBM Corporation 2020.

from __future__ import print_function
from setuptools import setup
from setuptools.command.test import test as TestCommand
import os
import sys

with open(os.path.join(os.path.dirname(__file__), 'VERSION'), 'r') as f_ver:
    __version__ = f_ver.read()

if sys.version_info[:2] < (3, 5):
    raise RuntimeError("Python version 3.5 or higher is required.")

if sys.argv[-1] == 'publish-test':
    # test server
    os.system('python setup.py register -r pypitest')
    os.system('python setup.py sdist upload -r pypitest')

    sys.exit()

if sys.argv[-1] == 'publish':
    # test server
    os.system('python setup.py register -r pypitest')
    os.system('python setup.py sdist upload -r pypitest')

    # production server
    os.system('python setup.py register -r pypi')
    os.system('python setup.py sdist upload -r pypi')
    sys.exit()


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long', 'test']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


def read_md(f):
    return open(f, 'rb').read().decode(encoding='utf-8')


setup(
    name='ai-lifecycle-cli',
    version=__version__,
    description='CLI library for importing, exporting and managing IBM Watson Machine Learning assets.',
    license='Apache-2.0',
    python_requires='>=3.5',
    long_description_content_type='text/markdown',
    install_requires=[
        'urllib3==1.25.8',
        'jmespath==0.9.4',
        'requests==2.22.0',
        'flatten_dict==0.2.0',
        'PyGithub==1.46',
        'PyJWT==1.7.1'
    ],
    dependency_links=[],
    tests_require=['responses', 'pytest', 'python_dotenv', 'pytest-rerunfailures', 'tox'],
    cmdclass={'test': PyTest},
    entry_points={'console_scripts': ['ai-lifecycle-cli=ai_lifecycle_cli.main:main']},
    author='IBM Corp',
    author_email='daniel.ryszka@pl.ibm.com',
    long_description=read_md('README.md'),
    url='https://www.ibm.com/cloud/machine-learning',
    packages=['ai_lifecycle_cli'],
    include_package_data=True,
    keywords='watson-machine-learning, watson-studio, ibm-watson',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
    zip_safe=True
)