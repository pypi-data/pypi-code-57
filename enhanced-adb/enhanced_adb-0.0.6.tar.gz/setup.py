import os

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="enhanced_adb",
    version="0.0.6",
    author="roy.fu",
    author_email="fuzhongqing1995@gmail.com",
    description="enhancement adb",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/royfu/enhanced-adb/src",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        'Development Status :: 3 - Alpha',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['eadb = enhanced_adb.command_line:main'],
    },
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
        "enhanced_adb": ["bin/*", "res/*"]
    },
    install_requires=['whichcraft', 'rich', 'pyyaml', 'pysmb'],
    py_modules=[],
)
