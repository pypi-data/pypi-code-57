from torchtrace.__init__ import __author__
from setuptools import setup, find_packages

print(find_packages())

setup(
    name = 'torchtrace',
    version='0.1',
    description='A simple autograd implementation based on PyTorch',
    url='https://github.com/gusye1234/PyTrace',
    author = __author__,
    author_email='jianbaiye@outlook.com',
    license='MIT',
    packages=find_packages(),
    install_required = [
        'torch>= 1.4.0',
        'numpy>=1.16.4',
        'rich>=2.2.3'
    ]
)