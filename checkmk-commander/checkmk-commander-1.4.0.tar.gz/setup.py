"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='checkmk-commander',
    version='1.4.0',
    description='Curses interface to Checkmk Raw.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/larsfp/checkmk-commander',

    author='Lars Falk-Petersen',
    author_email='dev@falkp.no',

    license='GPLv3+',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: System Administrators',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        # Specify the Python versions you support here.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Topic :: System :: Networking",
        "Environment :: Console :: Curses",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
        "Topic :: System :: Networking :: Monitoring"
    ],
    keywords='monitoring',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['urwid', 'requests', 'appdirs', 'wheel', 'simplejson'],
    scripts=['bin/chkcom'],
    # setup_requires=['install_freedesktop'],
    # entry_points = {
    #     'console_scripts': ['chk=checkmkcommander.command_line:main'],
    # },
    # desktop_entries={
    #     'chkcom': {
    #         'Name': 'chkcom',
    #         'GenericName': 'checkmk-commander',
    #         'Categories': 'Network;',
    #     },
    # },
    data_files=[
        ('share/applications', ['applications/checkmk-commander.desktop']),
        ('share/icons/hicolor/48x48/apps', ['icons/48x48/checkmk-commander.png']),
        ('share/icons/hicolor/256x256/apps', ['icons/256x256/checkmk-commander.png']),

    ],
    python_requires='>=3.6',
    test_suite = 'tests',
)

