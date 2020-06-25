import setuptools
import sys
with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = list()
if sys.platform == "linux2" or sys.platform == "linux":
    install_requires = ["smbus2",]

if sys.platform == "esp8266":
    sys.path.pop(0)
    sys.path.append("..")

setuptools.setup(
    name="xinabox-CORE",
    version="0.0.10",
    author="Luqmaan Baboo",
    author_email="luqmaanbaboo@gmail.com",
    description="I2C Core for CC03/CS11/CW03, CW02, CW01, Raspberry Pi and Microbit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xinabox/Python-CORE",
    install_requires=install_requires,
    py_modules=["xCore",],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
