from setuptools import setup, find_packages
import os

with open('README.md', "r") as fh:
    long_desc = fh.read()

current_dir = os.path.abspath(os.path.dirname(__file__))
setup_reqs = ['Cython', 'numpy']
with open(os.path.join(current_dir, 'requirements.txt')) as fp:
    install_reqs = [r.rstrip() for r in fp.readlines() if not r.startswith('#') and not r.startswith('git+')]

setup(
    name='atml',
    version='0.0.1',
    author='ahhuisg',
    author_email='yanhui79@gmail.com',
    description='Automation Toolkit for Machine Learning',
    long_description=long_desc,
    install_requires=install_reqs,
    include_package_data=True,
    long_description_content_type='text/markdown',
    url='https://github.com/ahhuisg/atml',
    packages=find_packages()
)