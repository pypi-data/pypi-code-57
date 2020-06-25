from setuptools import setup

setup(
    name='litenet',
    version='0.2.3',
    packages=['litenet'],
    url='https://github.com/GrandMoff100/LiteNet',
    license='',
    author='Quantum_Wizard',
    author_email='',
    description='A CL version of LiteNet',
    install_requires=["click", "keyboard"],
    entry_points={
        "console_scripts": ["litenet=litenet.cli:cli"]
    }
)
