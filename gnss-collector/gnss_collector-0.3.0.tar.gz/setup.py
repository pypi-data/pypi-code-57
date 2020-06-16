from setuptools import setup

print("AVISO: Primero instalar ORM_COLLECTOR")

setup(name='gnss_collector',
      version='0.3.0',
      description='Data Collector, for timeseries stations with ip:port address',
      url='http://gitlab.csn.uchile.cl/dpineda/collector',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='MIT',
      packages=['gnss_collector'],
      keywords = ["collector","gnss", "scheduler", "async", "multiprocess"],
      install_requires=["networktools",
                        "tasktools",
                        "basic_logtools",
                        "basic_queuetools",
                        "datadbs",
                        "data_rdb",
                        "data_geo",
                        "dataprotocols",
                        "gnsocket",
                        "uvloop",
                        "orm_collector"],
      entry_points={
        'console_scripts':["collector = gnss_collector.scripts.run_collector:run_collector",]
        },
      include_package_data=True,      
      zip_safe=False)
