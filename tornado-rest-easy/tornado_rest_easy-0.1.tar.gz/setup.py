import versioneer
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='tornado_rest_easy',
    packages=find_packages(exclude=['tests']),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='library for easy restful APIs in tornado',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['tornado'],
    author='Richard Postelnik',
    author_email='richard.postelnik@gmail.com',
    url='https://github.com/postelrich/tornado-restful',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False
)