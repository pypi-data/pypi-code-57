import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="MLDatasetBuilder",
  version="0.0.7",
  author="Karthick Nagarajan",
  author_email="karthick965938@gmail.com",
  description="MLDatasetBuilder is a python package which is helping to prepare the image for your ML dataset.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  keywords='imagedataset preparedataset prepareimage dataset mldataset datasetbuilder mldatasetbuilder',
  license='MIT',
  url="https://github.com/karthick965938/ML-Dataset-Builder",
  packages=setuptools.find_packages(),
  install_requires=[
    'matplotlib',
    'opencv-python',
    'pandas',
    'art',
    'termcolor',
    'progress',
  ],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)