from setuptools import setup, find_packages

setup(
    name="private",
    description="Python modules and distribution encryption tool",
    author="Omer Sarig",
    author_email="omer@sarig.co.il",
    packages=find_packages(),
    install_requires=["pyaes", "fire"],
    package_data={"private": ["*.txt"]},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "private = private:main"
        ]
    }
)
