import setuptools
 
with open("README.txt", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    #Here is the module name.
    name="electricalpy",
 
    #version of the module
    version="0.0.14.1",
 
    #Name of Author
    author="iron man",
 
    #your Email address
    author_email="mohammadabdulrehman739@gmail.com",
 
    #Small Description about module
    description="computing functions for electrical engineers",
 
    long_description=long_description,

    install_requires=['numpy','sympy'],
 
    #Specifying that we are using markdown file for description
    long_description_content_type="text/markdown",
 
    #Any link to reach this module, if you have any webpage or github profile
    url="https://github.com/iam-abdul",
    packages=setuptools.find_packages(),
 
    #classifiers like program is suitable for python3, just leave as it is.
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
        
    ],
)
