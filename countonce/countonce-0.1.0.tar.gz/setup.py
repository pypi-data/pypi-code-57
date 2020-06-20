from io import open
from setuptools import setup

with open('README.md') as read_me:
    long_description = read_me.read()

setup(
    name='countonce',
    version='0.1.0',
    author='CountOnce',
    url='https://github.com/countonce/countonce-python',
    packages=['countonce'],
    install_requires=['requests'],
    python_requires='>=3.5',
    description='Wrapper for the countonce API',
    long_description='',
    long_description_content_type='text/markdown',
    keywords=['countonce', 'api']
)
