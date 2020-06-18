import setuptools

with open("fitsnap3/README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='fitsnap3',  
     version='0.9',
     author="Charles Sievers",
     author_email="charliesievers@cox.net",
     description="Interatomic Potential Machine learning Interface",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/charlessievers/FitSNAP/tree/ObjOrPar/fitsnap3",
     packages=setuptools.find_packages(),
     install_requires=["psutil>=5.6.3", "scipy>=1.3.1", "pandas>=0.25.1", "numpy>=1.17.2"],
     package_data={
         "fitsnap3": ["*/*.py", "*/*/*.py"]
     },
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
