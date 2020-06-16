from setuptools import setup

setup(
     name='pymocko',
     version='0.1.2',
     author='datnguye',
     author_email='datnguyen.it09@gmail.com',
     packages=['pymocko'],
     url='https://github.com/datnguye/pymocko',
     license='MIT',
     description='A package to generate mock data',
     long_description_content_type="text/markdown",
     long_description=open('README.md').read(),
     install_requires=[],
     python_requires='>=3.7.5'
)