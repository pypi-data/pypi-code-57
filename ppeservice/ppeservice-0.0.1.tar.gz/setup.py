import os
import re
# """
# This is an personal website generator(could be any website or small services generator)
# It control build, deploy, url generation and all process needed by having a webpage
# """
from setuptools import setup, find_packages

packages_required = []
with open("requirements.txt", "r") as f:
    for line in f:
        packages_required.append(line[:-1])



setup(
    name='ppeservice',
    version="0.0.1",
    license='GPLv3',
    author='Ye Zhang, Junqi Zhang',
    author_email="zhangforchat@gmail.com",
    url="https://github.com/JunqiZhang0/py-production-experiment",
    description='Personal website generator(could be any website or small services generator)',
    long_description="asd",
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
