from setuptools import setup, find_packages

setup(name='AutoTool',
      version='0.1',
      description='Automatisation package',
      long_description='GWInstek spectrum analyzer remote control package',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.0',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='spectrum analyzer remote control',
      author='Simatov A.V.',
      author_email='vadim.simatov2016@yandex.ru',
      packages=find_packages(),
      install_requires=[
          'vxi11',
      ],
      include_package_data=True,
      zip_safe=False)
