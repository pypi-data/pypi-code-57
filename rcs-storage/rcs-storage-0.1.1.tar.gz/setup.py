from setuptools import find_packages, setup

setup(
    name='rcs-storage',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'rcs-storage = rcs_storage.scripts.main:cmd',
        ],
    },
    version='0.1.1',
    license='MIT',
    description='Client for the Research Data Storage Registry, '
                'Research Computing Services, University of Melbourne.',
    author='Elyas Khan',
    author_email='elyas.khan@unimelb.edu.au',
    url='https://gitlab.unimelb.edu.au/resplat-data/rcs-storage',
    keywords=['unimelb'],
    install_requires=[
        'requests',
        'prettytable',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
