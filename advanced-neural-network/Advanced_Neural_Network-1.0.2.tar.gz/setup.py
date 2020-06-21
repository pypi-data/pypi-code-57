from setuptools import setup

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    name="Advanced_Neural_Network",
    version="1.0.2",
    description="Advanced use of neural networks",
    py_modules=["ANN"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    extras_require={
        "dev":[
            "pytest>=3.7",
        ],
    },
    url="https://github.com/alix59/NN",
    author="Hamidou Alix",
    author_email="alix.hamidou@gmail.com",
    
)