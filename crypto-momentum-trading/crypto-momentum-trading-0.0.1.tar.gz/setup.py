import os
import setuptools

dist_module = 'crypto.momentum.trading_client'
version_filepath = os.path.join('src', *dist_module.split('.'), 'VERSION')
with open(os.path.join(os.path.dirname(__file__), version_filepath)) as version_file:
    version = version_file.read().strip()

setuptools.setup(
    name='crypto-momentum-trading',
    version=version,
    author='Ryan Krawczyk',
    author_email='ryankrawz11@gmail.com',
    description='A client for trading cryptocurrency with a momentum strategy on the FTX exchange.',
    packages=setuptools.find_namespace_packages(where='src', include=['crypto.*']),
    package_dir={'': 'src'},
    package_data={dist_module: ['VERSION']},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'ccxt>=1.27.35',
        'pandas>=1.0.3',
        'stockstats>=0.3.1',
    ],
    python_requires='>=3.5',
)
