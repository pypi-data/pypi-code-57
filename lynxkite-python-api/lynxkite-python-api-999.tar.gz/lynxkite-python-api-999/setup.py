from setuptools import find_namespace_packages, setup
import os

setup(
    name='lynxkite-python-api',
    version=os.environ.get('VERSION', 'snapshot'),
    install_requires=[
        'lynxkite-client',
    ],
    python_requires='>=3.6',
    author='Lynx Analytics',
    author_email='lynxkite@lynxanalytics.com',
    description='Python API for LynxKite [obsolete]',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url='https://lynxkite.com/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Development Status :: 7 - Inactive',
    ],
)
