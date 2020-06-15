from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    README = readme.read()

setup(
    name="buz",
    version="0.4.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    author="Luis Pintado Lozano",
    author_email="luis.pintado.lozano@gmail.com",
    description="Light, simple and extensible implementations of event, command and query buses",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT License",
    url="https://github.com/Feverup/buz",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Typing :: Typed",
    ],
    python_requires=">=3.6",
    install_requires=['dataclasses;python_version<"3.7.0"'],
    extras_require={"pypendency": ["pypendency~=0.1.0"]},
    include_package_data=True,
)
