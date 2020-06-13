from distutils.core import setup
    
setup(
  name = 'bytearray1',         
  packages = ['bytearray1'],   
  version = '0.2',    
  description = 'A project with bytearray',   
  author = 'Lucas',                
  py_modules=["bytearray1"],  
  author_email = 'lucasbosspro2@gmail.com',      
  url = 'https://github.com/lucasbosspro',   
  license='MIT',    
  install_requires=[      
          'setuptools',
          'beautifulsoup4',
      ],
  classifiers=[
		"Environment :: Console",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
  ],
)