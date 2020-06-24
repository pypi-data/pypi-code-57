from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

INSTALL_REQUIRES = [
    'pandas>=1.0.0',
    'jupyter>=1.0.0',
    'ipywidgets>=7.5.1'
]

setup(
    name='classypandas',
    version='0.1',
    description='Quickly annotate/label your data using jupyter widgets and pandas.',
    url='https://github.com/TMMV/classypandas',
    author='Tiago Vieira',
    author_email='email@tiagovieira.pt',
    license='MIT',
    packages=['classypandas'],
    install_requires=INSTALL_REQUIRES,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Jupyter",
        "Topic :: Scientific/Engineering"
    ],
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
