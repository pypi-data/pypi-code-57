import setuptools

with open('VERSION', 'r') as fh:
    version = fh.read().strip()

with open('cli/__version__.py', 'w+') as f:
    f.write('VERSION="{}"'.format(version))

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wowtool",
    version=version,
    install_requires=[
      "setuptools",
      "click",
      "wowpy",
      "click-option-group"
    ],
    entry_points='''
        [console_scripts]
        wowtool=cli.wowtool:cli
    ''',
    author="Daniel Barragan",
    author_email="dbarragan1331@gmail.com",
    description="Wowza python management tool - wowtool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/d4n13lbc/wowtool",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)