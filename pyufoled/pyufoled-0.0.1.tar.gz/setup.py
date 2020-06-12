from setuptools import setup

setup(
    name='pyufoled',
    version='0.0.1',
    author='Erik Mayrhofer',
    author_email='obyoxar+pypi@gmail.com',
    url='https://github.com/ErikMayrhofer/pyufoled',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    description='A Python3 wrapper for LD686-compatible LED controllers.',
    install_requires=[],
    packages=['pyufoled'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Home Automation",
        "Operating System :: OS Independent",
    ]
)