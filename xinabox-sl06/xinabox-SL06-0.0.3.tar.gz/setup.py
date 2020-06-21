import setuptools
import sys
with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = list()
if sys.path == "linux":
    install_requires = ["smbus2", "xinabox-CORE",]
else:
    install_requires = ["xinabox-CORE",]

setuptools.setup(
    name="xinabox-SL06",
    version="0.0.3",
    author="Luqmaan Baboo",
    author_email="luqmaanbaboo@gmail.com",
    description="Proximity, gesture, light and colour sensor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xinabox/Python-SL06",
    install_requires=install_requires,
    py_modules=["xSL06",],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
