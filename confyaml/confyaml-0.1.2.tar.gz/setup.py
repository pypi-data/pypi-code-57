from setuptools import setup, Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='confyaml',
    packages=['confyaml'],
    version='0.1.2',
    license='MIT',
    description='Deals with configuration files in yaml',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Lucas Coelho',
    author_email='hello@lucascoelho.net',
    url='https://github.com/lucascoelhof/confyaml',
    download_url='https://github.com/lucascoelhof/confyaml/archive/v0.1.2-beta.tar.gz',
    keywords=['configuration', 'yaml', 'config'],
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
