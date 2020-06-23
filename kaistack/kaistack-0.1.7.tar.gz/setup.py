from setuptools import setup
from setuptools import find_packages


NAME = 'kaistack'
__version__ = '0.1.7'

REQUIRES = [
    'kfp>=0.5.1',
    'certifi==2019.11.28',
    'auth0-python==3.9.1',
    'Click>=7.0',
]


setup(
    name=NAME,
    version=__version__,
    description='Hypertensor Kaistack SDK',
    author='HypertensorAI',
    install_requires=REQUIRES,
    license='apache-2.0',
    packages=find_packages(include=['kaistack*']),
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.5.3',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'kaistack=kaistack.cli.cli:main',
            'run_notebook=kaistack.tools.run_notebook:main',
        ]
    })
