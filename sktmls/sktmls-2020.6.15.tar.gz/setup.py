import setuptools
import os

SKTMLS_VERSION = os.getenv("SKTMLS_VERSION")
if not SKTMLS_VERSION:
    raise TypeError("NO SKTMLS_VERSION")


def load_long_description():
    with open("README.md", "r") as f:
        long_description = f.read()
    return long_description


setuptools.setup(
    name="sktmls",
    version=SKTMLS_VERSION,
    author="Colin",
    author_email="colin@sktai.io",
    description="A package for MLS-Models",
    long_description=load_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/sktaiflow/mls-model-registry",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "joblib==0.14.1",
        "lightgbm==2.3.1",
        "numpy==1.18.3",
        "scikit-learn==0.22.2.post1",
        "scipy==1.4.1",
        "xgboost==1.0.2",
        "boto3==1.13.25",
    ],
)
