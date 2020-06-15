from setuptools import setup, find_packages

setup(
    name="mlogic",
    version="0.1",
    author="Brendon Lin",
    author_email="brendon.lin@outlook.com",
    description="Useful functions for machine learning",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        "numpy>=1.18.4",
        "pandas>=1.0.3",
        "scikit-learn>=0.23.1",
        "scipy>=1.4.1",
    ],
    # entry_points={"console_scripts": ["runit = package.view:main"]},
)
