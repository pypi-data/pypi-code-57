#!/usr/bin/env python
 
from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

import apk2java
 
class pre_install(install):
    def run(self):
        if "bdist" in self.install_libbase:
            apk2java.setup("build/lib/" + self.config_vars["dist_name"])
        else:
            apk2java.setup(self.install_libbase + "/" + \
                    self.config_vars["dist_name"])
        subprocess.run(["make", "-C", "apk2java/java"])
        install.run(self)


setup(
    name='apk2java',
    version='0.0.5',
    packages=['apk2java'],
    #data_files=[('apk2java/java', ['java/Class2Java.jar'])],
    package_data={'apk2java': ['java/Class2Java.jar',
                               'java/jd-core-1.1.3.jar']},
    author="MadSquirrel",
    author_email="benoit.forgette@ci-yow.com",
    description="Decompile APK to Java",
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    download_url="https://gitlab.com/MadSquirrels/mobile/apk2java",
    include_package_data=True,
    url='https://ci-yow.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Planning"
    ],
 
    entry_points = {
        'console_scripts': [
            'apk2java=apk2java:main',
        ],
    },
    cmdclass={
        'install': pre_install
    },
    install_requires = [
    ],
    python_requires='>=3.5'
 
)
