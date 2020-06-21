#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['numpy>=1.17.2',
                'pandas>=0.25.1',
                'matplotlib>=3.1.1',
                'seaborn>=0.9.0']

setup_requirements = ['pytest-runner',
                      'numpy>=1.17.2',
                      'pandas>=0.25.1',
                      'matplotlib>=3.1.1',
                      'seaborn>=0.9.0']

test_requirements = ['pytest>=3',
                     'numpy>=1.17.2',
                     'pandas>=0.25.1',
                     'matplotlib>=3.1.1',
                     'seaborn>=0.9.0']

long_description = '''

Simple class and methods for the Bayesian estimation and comparison of proportions.  i.e. a simple Bayesian AB test of proportions.  

- A user can input the results from two samples, A and B, and get estimates of the posterior density and their difference.  

- Estimation is from simple simulation from the conjugate posterior distributions.  

- Provides summary statistics and visualisations for the estimated parameters.

- The prior distribution, sample count, random seed, credible intervals and parameter names can all be customised.

'''


setup(
    author="Oliver Chipperfield",
    author_email='omc0dev@googlemail.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description='Class method for the Bayesian estimation and comparison of proportions',
    install_requires=requirements,
    license="MIT license",
    long_description=long_description,  #readme + '\n\n' + history,
    include_package_data=True,
    keywords='bayespropestimation',
    name='bayespropestimation',
    packages=find_packages(include=['bayespropestimation', 'bayespropestimation.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/oli-chipperfield/bayespropestimation',
    version='0.1.4',
    zip_safe=False,
)
