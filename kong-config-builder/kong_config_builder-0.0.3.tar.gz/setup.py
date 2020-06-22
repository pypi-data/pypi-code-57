from setuptools import setup, find_packages

libs = ["aws"]
extras = {"all": []}

with open("requirements.txt") as reqs:
    requirements = reqs.read().split("\n")

for lib in libs:
    with open(f"requirements_{lib}.txt") as reqs:
        extras[lib] = reqs.read().split("\n")
        extras["all"] = extras["all"] + extras[lib]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="kong_config_builder",
    version="0.0.3",
    description="Kong declarative configuration builder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Olx",
    license='MIT',
    include_package_data=True,
    url='https://github.com/olxbr/kong-config-builder/',
    download_url='https://github.com/olxbr/kong-config-builder/archive/master.zip',
    install_requires=requirements,
    extra_require=extras,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ],
    packages=find_packages()
)
