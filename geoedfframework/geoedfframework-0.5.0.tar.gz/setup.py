from setuptools import setup,find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='geoedfframework',
      version='0.5.0',
      description='GeoEDF Connector Processor Framework',
      url='https://geoedf.github.io/geoedf/',
      author='Rajesh Kalyanam',
      author_email='rkalyanapurdue@gmail.com',
      license='MIT',
      python_requires='~=3.6',
      packages=find_packages(),
      scripts=['bin/run-connector-plugin.py','bin/run-processor-plugin.py','bin/merge.py','bin/collect.py','bin/gen-keypair.py','bin/run-workflow-stage.sh'],
      install_requires=['pyyaml','regex','cffi','cryptography'],
      include_package_data=True,
      zip_safe=False)
