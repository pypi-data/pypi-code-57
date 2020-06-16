#!/usr/bin/env python

import setuptools

import rootfinding

with open("README.rst", "r") as f:
    readme = f.read()

extras = {
    'doc': ['sphinx', 'sphinx_rtd_theme'],
    'test': ['pytest-cov', 'check-manifest'],
    'publish': ['setuptools', 'wheel', 'twine']
}
extras['dev'] = extras['doc'] + extras['test'] + extras['publish']

setuptools.setup(
    name='rootfinding',
    version=rootfinding.__version__,
    author="Gabriel S. Gerlero",
    author_email="ggerlero@cimec.unl.edu.ar",
    description=rootfinding.__doc__,
    long_description=readme,
    url="https://github.com/gerlero/rootfinding",
    project_urls={
        'Documentation': "https://rootfinding.readthedocs.io",
        'Bug Tracker': "https://github.com/gerlero/rootfinding/issues",
        'Source Code': "https://github.com/gerlero/rootfinding",
    },
    py_modules=['rootfinding'],
    license='BSD',
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: BSD License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Topic :: Scientific/Engineering :: Mathematics',
                 'Topic :: Software Development :: Libraries',
                 'Operating System :: OS Independent'],
    tests_require=extras['test'],
    extras_require=extras,
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    options={'bdist_wheel': {'universal': '1'}}
)
