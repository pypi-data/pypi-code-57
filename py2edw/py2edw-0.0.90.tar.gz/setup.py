from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
        name="py2edw",
        version="0.0.90",
        description="A high level Python wrapper for remotely connecting to SQL databases and querying using pandas dataframes.",
        long_description=readme(),
        long_description_content_type="text/markdown",
        url="https://github.com/renzobecerra/py2edw",
        author="Renzo Becerra",
        author_email="rbecerra@nameless.ai",
        license="MIT",
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
        ],
        packages=["py2edw"],
        include_package_data=True,
        install_requires=["psycopg2-binary", "sshtunnel", "pandas", "mysql-connector-python"],
        entry_points={
            "console_scripts": [
                "py2edw=py2edw.py2edw:main",
            ]
        },
    )