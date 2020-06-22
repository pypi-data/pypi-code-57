from setuptools import setup, find_packages
import snapsheets

fname = 'README.md'
with open(fname, 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='snapsheets',
    version=snapsheets.__version__,
    packages=find_packages(),
    package_data={'snapsheets' : ['*.yml']},
    install_requires=['pyyaml'],
    author='shotakaha',
    author_email='shotakaha+py@gmail.com',
    description='Wget snapshots of Google spreadsheets',
    long_description=readme,
    long_description_content_type='text/markdown',
    keywords='wget curl google spreadhsheet',
    url='https://shotakaha.gitlab.io/snapsheets/',
    project_urls={
        'Documentation': 'https://shotakaha.gitlab.io/snapsheets/',
        'Source Code': 'https://gitlab.com/shotakaha/snapsheets/'
        },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Japanese",
        "Programming Language :: Python :: 3.7",
        ],
    python_requires='>=3.7',
)
