from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="valid_typing",
    version="0.0.8",
    description="A simple typing validator",
    long_description=long_description,
    url="https://gitlab.com/WilliamWCYoung/valid-typing",
    author="William Young",
    author_email="william.w.c.young@hotmail.com",
    license="MIT",
    packages=["valid_typing"],
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[],
    python_requires=">=3.8",
    download_url="https://gitlab.com/WilliamWCYoung/valid-typing/-/archive/0.0.8/valid-typing-0.0.8.tar.gz",
)
