from setuptools import find_packages, setup

setup(
    name='netbox-oxidized',
    version='0.3.2',
    description='A plugin that integrates oxidized into netbox',
    url='https://github.com/ragnra/netbox-oxidized',
    author='Paul Denning',
    license='Apache 2.0',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.4',
)