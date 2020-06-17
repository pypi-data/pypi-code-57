import setuptools
import obs as package


setuptools.setup(
    name="huawei_obs",
    version="0.0.1",
    author="sheng_xc",
    author_email="sheng_xc@126.com",
    description="huawei yun obs client",
    long_description="huawei yun obs client",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5'
)
