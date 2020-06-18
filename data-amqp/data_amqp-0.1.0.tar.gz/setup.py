from setuptools import setup, find_packages

setup(name='data_amqp',
      version='0.1.0',
      description='DataDBS for RabbitMQP',
      url='http://www.gitlab.com/dpineda/data_amqp',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='MIT',
      packages=["data_amqp"],
      install_requires=["networktools",
                        "tasktools",
                        "basic_logtools",
                        "basic_queuetools",
                        "ujson"],      
      package_dir={'data_amqp': 'data_amqp'},
      package_data={
          'data_amqp': ['../doc', '../docs', '../requeriments.txt']},
      zip_safe=False)
