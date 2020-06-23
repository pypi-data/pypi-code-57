#!/usr/bin/env python
import os
import shutil
import sys

import jeffy

from setuptools import Command, find_packages, setup

if sys.argv[-1] == "publish":
    os.system("python setup.py upload")
    sys.exit()


class UploadCommand(Command):

    user_options = []

    def initialize_options(self): pass
    def finalize_options(self):   pass

    def run(self):
        try:
            cwd = os.path.join(os.path.abspath(os.path.dirname(__file__)))
            shutil.rmtree(os.path.join(cwd, 'dist'))
        except FileNotFoundError:
            pass

        os.system("python setup.py sdist")
        os.system('twine upload dist/*')
        os.system('git tag v{0}'.format(jeffy.__version__))
        os.system('git push --tags')
        sys.exit()


setup_options = dict(
    name='jeffy',
    version=jeffy.__version__,
    description='Event and Contract Driven Serverless "Application" Framework',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Serverless Operations',
    author_email='info@serverless-operations.com',
    url='https://github.com/serverless-operations/jeffy',
    packages=find_packages(exclude=['tests*', 'handler']),
    install_requires=['jsonschema', 'boto3'],
    license="MIT License",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    keywords='aws lambda serverless faas',
    cmdclass={
        'upload': UploadCommand,
    },
)

setup(**setup_options)
