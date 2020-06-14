import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='horofns',  
     packages=['horofns'],
     version='0.1',
     author="Joel Horowitz",
     author_email="joelhoro@gmail.com",
     description="A Python utility package of Horo fns",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/joelhoro",
 #    packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )



