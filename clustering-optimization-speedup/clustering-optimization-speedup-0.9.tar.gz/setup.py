import os

import numpy
from setuptools import Extension, setup, find_packages

ext_modules = [
    Extension('recalculation',
              sources=[os.path.join('clust_opt_turp', 'recalculation.c')],
              libraries=['m'],
              include_dirs=[numpy.get_include()])
]

if __name__ == "__main__":
    setup(name='clustering-optimization-speedup',
          author='Anatoliy Poletaev',
          author_email='Shtepser@yandex.ru',
          version='0.9',
          packages=find_packages(exclude=['*.pyx', '*.c']),
          ext_modules=ext_modules,
          extras_require={
              "Bundled_optimizer": ['cvxpy==1.0.31']
          },
          url='https://github.com/Shtepser/clustering-optimization-speedup',
          long_description='Package for speeding up portfolio optimization using hierarchical clustering',
          python_requires='>=3.8',
          install_requires=['scipy>=1.4.1', 'numpy>=1.18.4']
          )
    print("To use bundled optimizer, install cvxpy (tested on cvxpy 1.0.31)")
