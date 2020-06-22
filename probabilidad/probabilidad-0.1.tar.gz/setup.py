from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(  name='probabilidad',
        version='0.1',
        description='Probabilidad usando distribucion de Gauss/ normal y distribucion binomial',
        packages=['probabilidad'],
        long_description=long_description,
        long_description_content_type="text/markdown",
        author='Jose MARIN',
        author_email= 'josermarinr18@gmail.com',
        python_requires='>=3.4^',
        zip_safe=False
    )