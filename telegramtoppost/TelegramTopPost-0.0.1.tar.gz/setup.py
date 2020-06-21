from setuptools import find_packages,setup

setup(
name="TelegramTopPost",
version="0.0.1",
author="Meysam Kheyrollah",
author_email="meysamkheyrollahnejad@gmail.com",
install_requires=[
   'pymysql',
   'pandas',
   'json',
   'requests'
],
py_modules=["similarity","dbconnector"],
package_dir={'': "module"},

)
