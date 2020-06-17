from os.path import join, dirname

from setuptools import setup

import elmicpy

setup(
    name='elmicpy',
    version=elmicpy.__version__,
    packages=['elmicpy'],
    url='',
    license='MIT',
    author='leomaxwell',
    author_email='java.leon@mail.ru',
    description='This module needs for make microservices elitem assistents',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    zip_safe=False,
)
