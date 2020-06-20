from distutils.core import setup

with open("VERSION") as vfile:
    version_line = vfile.readline()

version = version_line.strip()

setup(
    name="graafilohi",
    packages=["."],
    version=version,
    license="MIT",
    description="Library for defining runnable pipelines as graphs",
    author="Aki Mäkinen",
    author_email="nenshou.sora@gmail.com",
    url="https://gitlab.com/blissfulreboot/python/graafilohi",
    keywords=["SOME", "MEANINGFULL", "KEYWORDS"],
    install_requires=[
        "networkx",
        "matplotlib"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6"
    ]
)
