import os
import re
import ast
"""
This is an personal website generator(could be any website or small services generator)
It control build, deploy, domain name generation and all process needed by having a website
"""
from setuptools import setup, find_packages
packages_required = []
with open("requirements.txt", "r") as f:
    for line in f:
        packages_required.append(line[:-1])

version = "0.0.0.0"

with open ('ppe/version.py') as f:
    for line in f:
        version = ast.parse(line).body[0].value.s

setup(
    name='ppeservice',
    version=version,
    license='GPLv3',
    author='Ye Zhang, Junqi Zhang',
    author_email="zhangforchat@gmail.com",
    url="https://github.com/JunqiZhang0/py-production-experiment",
    description='Personal website generator(could be any website or small services generator)',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=packages_required,

    classifiers=[
        'Development Status :: 1 - Planning'
    ],
    entry_points={
        'console_scripts': ['ppe=ppe.manage:main']
    }
)
