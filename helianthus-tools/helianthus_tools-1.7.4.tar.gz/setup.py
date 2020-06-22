
#!/usr/bin/env python3
# coding=utf-8
 
from setuptools import setup, find_packages
 
__author__ = 'HeliantHuS'
__date__ = '2020/06/22'
 
setup(
    name='helianthus_tools',
    version='1.7.4',
    description=(
        'HeliantHuS-Tools ~ wow awesome!' +
        'Change AWD plugin BUG(input host error.)' +
        'self use tools `﹀`γ'
    ),
    long_description=open('README.txt').read(),
    author='HeliantHuS',
    author_email='1984441370@qq.com',
    maintainer='HeliantHuS',
    maintainer_email='1984441370@qq.com',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/L-HeliantHuS/helianthus-tools',
    install_requires=['requests', 'paramiko'],
    include_package_data=True,
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
)