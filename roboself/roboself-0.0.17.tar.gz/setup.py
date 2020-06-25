import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="roboself",
    version="0.0.17",
    author="Razvan Dinu",
    author_email="razvan@roboself.com",
    description="The roboself python client.",
    long_description="The roboself python client.",
    long_description_content_type="text/markdown",
    url="https://github.com/roboself/roboself-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['roboself=roboself.cli.cli:run'],
    },
    python_requires='>=3.6',
    install_requires=[
        "click",
        "redis",
        "requests",
        "python-socketio[client]",
        "pyyaml"
    ]
)
