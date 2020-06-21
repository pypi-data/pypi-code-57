from setuptools import setup, find_packages

setup(
    name="diffdir",
    version="0.5",
    description="Diff directories",
    license="MIT Licence",
    author="cdb",
    author_email="kjgfcdb@126.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "colorama",
        "path"
    ],
    scripts=[],
    entry_points={"console_scripts": ["diffdir = diffdir.main:main"]},
)
