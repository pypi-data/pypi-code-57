import os
import sys

from setuptools import setup

from drf_case_middleware import __version__


with open('README.rst', encoding='utf-8') as f:
    readme = f.read()


setup(
    name='drf-case-middleware',
    version=__version__,
    description='Camel case to snake case and snake case to camel case for Django REST framework',
    long_description=readme,
    long_description_content_type='text/x-rst',
    author='Jiyoon Ha',
    author_email='punkkid001@gmail.com',
    url='https://github.com/django-breaker/drf-case-middleware',
    packages=['drf_case_middleware'],
    package_dir={'drf_case_middleware': 'drf_case_middleware'},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[],
    license='MIT',
    zip_safe=False,
    keywords='drf-case-middleware',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
