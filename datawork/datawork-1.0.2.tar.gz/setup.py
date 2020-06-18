from setuptools import setup

setup(name='datawork',
      version='1.0.2',
      description='Data Work system gather all data from a database to make analysis and charts',
      url='http://gitlab.csn.uchile.cl/dpineda/datawork',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='MIT',
      packages=['datawork'],
      keywords = ["collector","gnss", "scheduler", "async", "multiprocess"],
      install_requires=["networktools",
                        "tasktools",
                        "basic_logtools",
                        "basic_queuetools",
                        "data_rdb",
                        "data_geo",
                        "data_amqp",
                        "gnsocket",
                        "uvloop",
                        "click",
                        "numpy",
                        "ujson"],
      entry_points={
        'console_scripts':["datawork = datawork.scripts.run_datawork:run_datawork",]
        },
      include_package_data=True,      
      zip_safe=False)
