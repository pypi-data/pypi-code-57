import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="IsPycharmRun",
    version="0.8",
    author="Boxuan Shi",
    author_email="shi425@126.com",
    description="Define a decorator, identify the pycharm running environment, and call the same method in different ways",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/shi_bo_xuan/testSuite",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)