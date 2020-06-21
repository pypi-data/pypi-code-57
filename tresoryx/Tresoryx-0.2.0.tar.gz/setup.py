from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(name='Tresoryx',
      version='0.2.0',
      description='Humble automatisations for treasury using spreadsheets.',
      long_description=readme(),
      long_description_content_type="text/markdown",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Natural Language :: French',
          'Programming Language :: Python :: 3.5',
          'Topic :: Utilities'
      ],
      url='https://gitlab.com/GullumLuvl/tresoryx',
      author='Guitou des Phoenix',
      author_email='guitou.phoenix'+('@')+'mailo.com',
      license='GPLv3',
      packages=['tresoryx'],
      install_requires=[ #find_packages()
          'numpy',
          'pandas',
          'xlrd',
          'xlwt',
          'openpyxl',
          'PyYAML'
      ],
      extras_require={'Graph': ['matplotlib'],
                      'xlsx_style': ['jinja2']},
      entry_points = {
          'console_scripts': ['treso-exercice=tresoryx.auto_exercice:main',
                              'treso-dette=tresoryx.auto_dette:main',
                              'treso-bilan=tresoryx.auto_bilan:main',
                              'treso-datajoueur=tresoryx.datajoueur:main']
      },
      include_package_data=True,
      zip_safe=False)
