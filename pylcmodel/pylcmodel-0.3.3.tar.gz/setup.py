from setuptools import setup, find_packages

with open("./pylcmodel/_version.py") as f:
    exec(f.read())

setup(
    name='pylcmodel',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/openmrslab/pylcmodel.git',
    license='MIT',
    author='bennyrowland',
    author_email='bennyrowland@mac.com',
    description='Local CLI to forward lcmodel commands to remote machine',
    entry_points={
        "console_scripts": [
            "lcmodel = pylcmodel.cli:lcmodel_cli"
        ]
    },
    install_requires=['parsley', 'cryptography', 'paramiko'],
    extras_require={
        'test': ['pytest-cov', 'coverage', 'pyfakefs']
    }
)
