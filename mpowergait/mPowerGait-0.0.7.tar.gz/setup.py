from setuptools import setup

setup(
    name='mPowerGait',
    version='0.0.7',
    description='python package wrapper for mpower data pipeline',
    py_modules=["pdkit_wrapper"],
    package_dir={'': 'PDkit'},
    install_requires=["numpy",
                      "pandas==1.0.3",
                      "scipy",
                      "pdkit==1.2",
                      "scikit-learn",
                      "tsfresh",
                      "future",
                      "matplotlib",
                      "pandas_validator"]
)
