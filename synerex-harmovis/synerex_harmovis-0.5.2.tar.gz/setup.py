""" Synerex_HarmoVIS package
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

def _requires_from_file(filename):
    return open(filename).read().splitlines()

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='synerex_harmovis', 
    version='0.5.2',
    description='Python library for Synerex and HarmoViS',  
    long_description=long_description, 
    long_description_content_type='text/markdown', 
    url='https://github.com/synerex/python_Synerex-HarmoVIS',
    author='Nobuo Kawaguchi',
    author_email='kawaguti@synerex.net',
    classifiers=[  
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='visualization synerex harmoware-vis',
    packages=['synerex_harmovis', 'synerex_harmovis.proto', 'synerex_harmovis.examples'],
    python_requires='>=3.7, <4',

    install_requires=_requires_from_file('requirements.txt'),
    
#    extras_require={  # Optional
#        'dev': ['check-manifest'],
#        'test': ['coverage'],
#    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.
 #   package_data={  # Optional
 #       'sample': ['package_data.dat'],
 #   },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
#    data_files=[('my_data', ['data/data_file'])],  # Optional

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
#    entry_points={  # Optional
#        'console_scripts': [
#            'graphdemo=graphdemo:main',
#        ],
#    },

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/synerex/python_Synerex-HarmoVIS/issues',
        'Source': 'https://github.com/synerex/python_Synerex-HarmoVIS/',
    },
)
