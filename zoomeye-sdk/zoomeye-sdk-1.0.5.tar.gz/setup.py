from distutils.core import setup

setup(name='zoomeye-sdk',
      version='1.0.5',
      url="https://www.zoomeye.org/doc",
      description='ZoomEye is a search engine for cyberspace that lets the user find specific network components(ip, services, etc.).',
      long_description=open('README.rst').read(),
      author='Zoomeye Team',
      maintainer='Nixawk',
      author_email='team@zoomeye.org',
      py_modules=['zoomeye'],
      license='GPL-2.0',

      install_requires=[
          'requests',
      ]
     )
