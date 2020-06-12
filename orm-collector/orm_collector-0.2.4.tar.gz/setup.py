from pathlib import Path
from setuptools import setup

"""
install gdal first
"""
print("Installing gdal")
filename=str(Path(__file__).parent/"first_install_gdal.sh")
command = "bash %s" %filename
print(command)
import subprocess
results=subprocess.run(command, shell=True, universal_newlines=True, check=True)
print("Resultado de instalar gdal",results.stdout)


setup(name='orm_collector',
      version='0.2.4',
      description='ORM Collector Schemma',
      url='http://gitlab.csn.uchile.cl/dpineda/orm_collector',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      packages=['orm_collector'],
      keywords="collector gnss orm",
      install_requires=["networktools",
                        "basic_logtools",
                        "validators",
                        "shapely",
                        "psycopg2",
                        "sqlalchemy>=1.3.17",
                        "geoalchemy2",
                        "ujson",
                        "django",
                        "click"],
      entry_points={
        'console_scripts':["orm_create_db = orm_collector.scripts.create_db:run_crear_schema",
                           "orm_load_data = orm_collector.scripts.load_data:load_data_orm",]
        },
      include_package_data=True,
      license='MIT',
      zip_safe=False
      )
