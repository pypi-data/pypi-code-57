import setuptools

with open("README.md","r") as fh:
	long_description = fh.read()
	
setuptools.setup(
  name = "TakeAicHelper",
  version = "0.0.8",
  author = "Caio Souza",
  author_email = "caios@take.net",
  description = "Pacote para auxiliar na geração de métricas para analisar dados conversacionais",
  long_description = long_description,
  long_description_content_type="text/markdown",
  packages=['TakeAicHelper'],
  keywords = [],
  install_requires=[
  'pandas',
  'plotly',
  'koalas'
  ],
  classifiers=[  
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: MIT License",
	"Operating System :: OS Independent",
    "Programming Language :: Python :: 3"
  ]
)