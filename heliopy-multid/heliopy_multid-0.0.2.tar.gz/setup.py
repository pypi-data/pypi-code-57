import os, sys
from setuptools import setup, find_packages, Command
from setuptools.extension import Extension


here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="heliopy_multid",
    version="0.0.2",
    author="AIDA Consortium",
    author_email="coordinator.aida@kuleuven.be",
    description="Extension to heliopy to retrieve multi-dimensional heliopheric data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/aidaspace/heliopy_multid",
    license='GNU GPLv3',
    python_requires='>=3.5',
    install_requires=[
         'numpy',
         'pandas',
         'xarray',
         'astropy',
         'heliopy',
         'sunpy',
         'cdflib',
         'requests',
         'wget'
    ],
    tests_require=[
        'pytest'
    ],
    classifier=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Physics'
    ],
    packages=find_packages(exclude=['doc*', 'example*',
                                    'test*', '*egg-info*']),
    data_files=None,
    zip_safe=False,
    include_package_data=True,
    setup_requires=['pytest-runner'],
    test_suite = 'tests',
    ## Uncommend to wrap C/C++/Fortran codes
    #ext_modules=cythonize(extensions),
)
