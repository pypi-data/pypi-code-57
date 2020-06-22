import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
import drf_case_middleware

setup(
    name='drf-case-middleware',
    version=drf_case_middleware.__version__,
    description='Camel case to snake case and snake case to camel case for Django REST framework',
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
