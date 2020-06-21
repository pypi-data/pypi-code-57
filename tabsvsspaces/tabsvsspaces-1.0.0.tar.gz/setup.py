import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='tabsvsspaces',
    version='1.0.0',
    author="Roman Gräf",
    author_email="romangraef@gmail.com",
    description="A tool for counting spaces vs tabs in a codebase",
    license="MIT",
    keywords="tabs spaces linecount counting commandline",
    packages=['tabsvsspaces'],
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/romangraef/tabsvsspaces",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Religion',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Typing :: Typed',
    ],
    entry_points=dict(
        console_scripts='tabsvsspaces=tabsvsspaces:main'
    )
)
