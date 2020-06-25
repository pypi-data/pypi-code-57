import setuptools
# TODO: (prio 2) migrate to tensorflow 2.0 and use keras integrated with tensorflow

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vidtrain",
    version="0.1.4",
    author="Thawn",
    author_email="webmaster@korten.at",
    description="Deep learning annotation training and prediction workflow for microscopy video data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Thawn/vidtrain",
    install_requires=['tensorflow<2',
                      'keras<2.4',
                      'scikit-learn>=0.22',
                      'numpy>=1.18',
                      'matplotlib>=3',
                      'pandas>=1',
                      'pandastable>=0.12',
                      'tifffile>=2020.5',
                      'micdata>=0.1',
                      'pydot>=1'],
    extras_require={'bioformats': ['python-bioformats>=1.5',
                                   'javabridge>=1.0.18', ]},
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.7.0, <3.8.0',
)
