from setuptools import setup, find_packages

setup(
    name='catacomb-ai',
    version='0.1.20',
    description="Build tools for Catacomb's model hosting suite.",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['Click', 'docker', 'requests', 'pyyaml', 'flask-cors', 'flask'],
    entry_points='''
        [console_scripts]
        catacomb=catacomb.cli:cli
    '''
)
