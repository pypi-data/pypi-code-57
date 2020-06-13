from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='mPowerGait',
    version='0.0.1',
    description='python package wrapper for mpower data pipeline',
    py_modules=["pdkit_wrapper"],
    package_dir={'': 'PDkit'},
    install_requires=["numpy",
                      "pandas",
                      "scipy",
                      "pdkit",
                      "scikit-learn", ]
)
