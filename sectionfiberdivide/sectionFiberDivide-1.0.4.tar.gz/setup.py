from setuptools import setup, find_packages
from setuptools.extension import Extension
from os import path
import numpy

setup(
    name='sectionFiberDivide',  # Required

    version='1.0.4',  # Required

    description='Section fiber element generate program based on python language',  # Optional
    url='https://github.com/Junjun1guo/sectionFiberGenerate',  # Optional

    author='Junjun Guo',  # Optional
    author_email='guojj01@gmail.com',  # Optional

    classifiers=[  # Optional
 
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='fiber element, section mesh',  # Optional

    packages=find_packages(),  # Required
    python_requires='>=3.6',

    install_requires=[
		'numpy>=1.17.4',
		'matplotlib>=3.1.2',
		'pygmsh>=6.0.2',
		'meshio>=3.3.1',
		'scipy>=1.4.1'
	],  # Optional 
#	setup_requires=[
#		'setuptools>=18.0',
#		'cython>=0.28.4',
#		],
    package_data={  # Optional
        '':['*.exe'],
    },
	zip_safe=False
)