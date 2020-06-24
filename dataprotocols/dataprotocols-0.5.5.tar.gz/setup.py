from setuptools import setup, find_packages

setup(name='dataprotocols',
      version='0.5.5',
      description='DataProtocols is a set of classes that implement protocols for data acquisition',
      url='http://gitlab.csn.uchile.cl/dpineda/dataprotocols',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      install_requires=['Click','networktools', 'basic-logtools'],
      scripts=[
          'dataprotocols/scripts/gsof.py',
          'dataprotocols/scripts/eryo.py',
          'dataprotocols/scripts/protocol.py',                    
      ],      
      entry_points={
        'console_scripts':["gsof = dataprotocols.scripts.gsof:run_gsof",
                           "eryo = dataprotocols.scripts.eryo:run_eryo",
                           "protocol = dataprotocols.scripts.protocol:run_protocol"]
        },
      packages=find_packages(),
      include_package_data=True,
      license='MIT',
      zip_safe=False)
