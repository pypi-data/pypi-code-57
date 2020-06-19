from setuptools import setup, find_packages

description = "python micro tool"

setup(
    name='micro-py',
    version="1.0.7",
    author='yyl',
    author_email='1906600192@qq.com',
    url='https://github.com/yylany/py-micro.git',
    description=description,
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "grpcio==1.27.2",
        "protobuf==3.10.0",
        "grpcio-tools==1.27.2",
        "python-consul==1.1.0",
    ],
)
