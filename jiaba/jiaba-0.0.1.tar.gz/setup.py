from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fin:
    long_description = fin.read()

setup(
    name='jiaba',
    version='0.0.1',
    author='labusi',
    long_description = long_description,
    packages=find_packages(),
    package_data={
        'jiaba':['datas/saved_models/bilstm_crf/*.*']
    }
)