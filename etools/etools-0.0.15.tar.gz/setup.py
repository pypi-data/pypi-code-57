import setuptools
import etools as package


setuptools.setup(
    name="etools",
    version=package.__version__,
    author="sheng_xc",
    author_email="sheng_xc@126.com",
    description="some useful tools",
    long_description="some useful tools",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        "aiohttp>=3.6.2",
        "requests>=2.23.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5'
)
