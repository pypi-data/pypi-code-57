from setuptools import setup, find_packages, Extension
import numpy

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md',encoding='utf-8') as f:
    readme = f.read()

ext = [
      Extension(name="gmtb.util.distance.kendall_tau_dist_cy",
                sources=["gmtb/util/distance/kendall_tau_dist_cy.pyx"],
                include_dirs=[numpy.get_include()])
]

setup(name='gmtb',
      install_requires=requirements,
      setup_requires=[
          'setuptools>=18.0',
          'cython>=0.28.4',
      ],
      version='1.0.5',
      description='Python version of the Generalized Median Toolbox.',
      long_description_content_type='text/markdown',
      long_description=readme,
      author='Andreas Nienkötter',
      author_email='a.nienkoetter@uni-muenster.de',
      url='https://www.uni-muenster.de/PRIA/en/forschung/dpe.html',
      license='MIT',
      packages=find_packages(exclude=('test', 'docs')),
      ext_modules=ext,
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3",
      ]
      )
