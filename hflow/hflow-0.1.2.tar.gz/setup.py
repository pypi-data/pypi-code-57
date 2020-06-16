from setuptools import setup, find_packages
setup(
    name="hflow",
    version="0.1.2",
    
    author='Hien Hoang',
    author_email='hoangchunghien@gmail.com',
    
    packages=find_packages("src"),
    package_dir={"": "src"},

    url="https://github.com/hoangchunghien/flow",
    license='MIT',
)
