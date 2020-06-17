from setuptools import setup

from aws_ecs_services._version import __version__


setup(
    name="aws_ecs_services",
    version=__version__,
    description=(
        "Get ECS service info (e.g. EC2 instance id) by a given service name."
    ),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Norman Moeschter-Schenck",
    author_email="norman.moeschter@gmail.com",
    url="https://github.com/normoes/aws_ecs_services",
    download_url=f"https://github.com/normoes/aws_ecs_services/archive/{__version__}.tar.gz",
    install_requires=["boto3>=1.14.4"],
    # py_modules=["xmrto_wrapper"],
    packages=["aws_ecs_services"],
    scripts=["bin/aws_ecs_services"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
    ],
)
