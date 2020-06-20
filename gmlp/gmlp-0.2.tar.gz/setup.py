
from setuptools import setup, find_packages

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name='gmlp',  # Required
    version="0.2",
    description='Genetic Algorithm for Python',
    long_description=long_description, 
    long_description_content_type='text/markdown', 
    url='https://github.com/CoderWeird/gmlp',
    author='Drew Montooth',
    author_email='drewmontooth@gmail.com',
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],

    packages=find_packages(),  # Required

    python_requires='>=2.7',

    install_requires=[
        'pygame'
    ],

    include_package_data=True
)