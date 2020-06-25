#!/usr/bin/env python3

'''
AstroAtmosphere: A python package to evaluate refractive indices, refraction
                 and dispersion of the atmosphere. It was written for astronomic 
                 applications, but it can probably be used for other applications
                 as well.
'''
from setuptools import setup


with open('README.md') as f:
    __readme__ = f.read()

with open('LICENSE.txt') as f:
    __license__ = f.read()


def setup_package():
    # Rewrite the version file every time
    # write_version_py()

    setup(name='AstroAtmosphere',
          version='1.0',
          description='Collection of equations for refractive index, refraction and dispersion calculations of atmospheric air.',
          long_description=__readme__,
          long_description_content_type='text/markdown',
          author='Joost van den Born',
          author_email='born@astron.nl',
          url='https://gitlab.astro-wise.org/micado/atmosphericmodel',
          download_url='https://gitlab.astro-wise.org/micado/atmosphericmodel/-/archive/v1/atmosphericmodel-v1.tar.gz',
          license='GNU General Public License v3',
          data_files = [('',['LICENSE.txt'])],
          package_dir={'AstroAtmosphere': 'AstroAtmosphere'},
          package_data={'AstroAtmosphere': ['data/*.txt']},
          include_package_data=True,
          packages=['AstroAtmosphere'],
          keywords=['REFRACTION','REFRACTIVITY','ATMOSPHERE','DISPERSION','CIDDOR'],
          install_requires=['numpy',
                            'scipy'],
          extras_require={'slalib':['pyslalib>=1.0.4']},
          classifiers=['Programming Language :: Python :: 3',
                       'Operating System :: OS Independent',
                       'Intended Audience :: Science/Research',
                       'Topic :: Scientific/Engineering :: Astronomy', ]
          )


if __name__ == '__main__':
    setup_package()