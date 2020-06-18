

import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Umar Ali Khan",
    author_email="umarkhan314@outlook.com",
    name='datashop',
    license="MIT",
    description='A collection of handy tools for data science',
    version='v0.0.3',
    long_description=README,
    url='https://github.com/thekhan314/datashop',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=['pandas','matplotlib','numpy','scipy','statsmodels'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)