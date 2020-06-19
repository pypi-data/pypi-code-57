# -*- coding:utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst', 'rb') as f:
    readme = f.read().decode('utf-8')

setup(
    name='ossFileField',
    version='1.0.2',
    description='Django Direct File Transfer From Server',
    long_description=readme,
    packages=['ossFileField'],
    author='wollens',
    author_email='zh2017728@163.com',
    install_requires=['django>=1.10',
                      'oss2>=2.3.3'],
    include_package_data=True,
    package_data={
        'static': ['*']
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
    ],
)
