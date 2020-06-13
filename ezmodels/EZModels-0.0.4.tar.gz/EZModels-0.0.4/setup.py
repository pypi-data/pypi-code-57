from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='EZModels',  
    version='0.0.4',  

    description='Streamlining Common Model Builds for Quick Development and Deployment', 
    long_description=long_description,  
    long_description_content_type='text/markdown',
    author='Preston Ward',  
    author_email='prestonsward@gmail.com',  

   
    keywords='data science machine learning model building',  

    packages=find_packages(),  
    
    install_requires=['keras'],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
 
)
