import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='utilidades',  
     version='1.0',
     scripts=['utilidades.py'] ,
     author="Thiago Henrique Martinelli",
     author_email="thiago.henrique.martinelli@gmail.com",
     description="several usefull common functions",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
