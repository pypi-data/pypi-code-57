from setuptools import setup


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='siametrics-deepmap',
    version='0.0.2',
    packages=['siametrics', 'siametrics.deepmap', 'siametrics.deepmap.dataset'],
    url='',
    license='Apache 2.0',
    author='SSripilaipong',
    author_email='santhapon.s@siametrics.com',
    description='',
    install_requires=requirements,
)
