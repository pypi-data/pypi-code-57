from setuptools import setup

setup(
    name='mPowerGait',
    version='0.0.4',
    description='python package wrapper for mpower data pipeline',
    py_modules=["pdkit_wrapper"],
    package_dir={'': 'PDkit'},
    install_requires=["numpy",
                      "pandas==1.0.3",
                      "scipy",
                      "pdkit==1.2",
                      "scikit-learn",
                      "tsfresh",
                      "matplotlib",
                      "future == 0.18.2",
                      "pandas_validator"]
)
