import setuptools
import os

this_directory = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

# 获取依赖
def read_file(filename):
    with open(os.path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]

setuptools.setup(
    name="PythonPluginFramework", # Replace with your own username
    version="0.0.9",
    author="bobo.yang",
    author_email="ybb_y1b1b1@163.com",
    description="Python plugin framework based QT",
    long_description= "Python plugin framework based QT",
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://gitee.com/imlaji/PythonPluginFW",
    packages=setuptools.find_packages(),
    install_requires=[
        'certifi==2018.8.24',
        'PyQt5==5.15.0',
        'PyQt5-sip==12.8.0',
        'QScintilla==2.11.5',
        'six==1.15.0',
        'wincertstore==0.2'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)