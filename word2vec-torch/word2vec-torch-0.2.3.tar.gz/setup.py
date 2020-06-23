from setuptools import setup, find_packages

setup(
    name='word2vec-torch',
    version='0.2.3',
    description='Skip-gram PyTorch implementation',
    packages=find_packages(include=['word2vec']),
    install_requires=[],
)

