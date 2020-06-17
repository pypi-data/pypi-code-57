import setuptools
import io

fh = io.open("README.md",mode="r",encoding="utf-8")
long_description = fh.read()



setuptools.setup(
    name='ConfigEnv',
    version='1.2.4',
    author="Théo \"Nydareld\" Guerin",
    author_email="theo.guerin.pro@gmail.com",
    description="Gestionnaire de configuration en json, ini avec overide possible en variable d’environnement",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nydareld/ConfigEnv",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)
