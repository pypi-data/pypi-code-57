from setuptools import setup, find_packages

setup(
    name='git power ext',
    version='0.1.63',
    author="Mohamed Farouk",
    author_email="mohamed.farouk173@gmail.com",
    packages=find_packages(),
    install_requires=[
        'Click',
    ],
    entry_points={
        "console_scripts": [
            "git-power-ext = powerext.git_power_ext:cli",
        ]
    }
)