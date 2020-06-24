from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="PyCmdex",
    version="1.1.17",
    description="The PyCmdex is a package used to control microcontroller board running the Cmdex firmware.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/drsanti/PyCmdex",
    author="Asst.Prof.Dr.Santi Nuratch",
    author_email="santi.inc.kmutt@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8"
    ],
    python_requires='>=3.8',
    packages=["PyCmdex"],
    include_package_data=True,
    install_requires=["pyserial", "keyboard", "websocket-client"],
    entry_points={
        "console_scripts": [
            "pycmdex=PyCmdex.cmdex:main",
        ]
    },
)
