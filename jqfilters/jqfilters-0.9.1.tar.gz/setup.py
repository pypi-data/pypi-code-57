import setuptools

from jqfilters import __version__

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='jqfilters', # Replace with your own username
    version=__version__,
    author='apastors',
    author_email='a.pastor.sanchez@gmail.com',
    description='Easy filtering based on jq syntax',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/apastors/filters',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=['pyjq']
)
