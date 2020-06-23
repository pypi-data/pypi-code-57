from setuptools import setup, find_packages

setup(
    name='SkyHyveLM',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Wrapper for large socket communications',
    long_description=open('README.md').read(),
    install_requires=[

    ],
    url='https://github.com/ThePengwyn/SkyHyveLM',
    author='Matthew Graham',
    author_email='matthewg@skyhyve.xyz'
)
