from setuptools import setup, find_packages

setup(
   name='wavelengthlib2',
   version='0.1.24',
   description='Wavelength library 2',
   author='Simon',
   author_email='simon.elliott@wavelength.law',
   classifiers=[
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.7'
          ],
   install_requires=[
         'pyodbc==4.0.30',
         'python-dateutil',
         'configparser',
         'pandas',
         'numpy',
         'datetime',
         'requests',
         'Unidecode',
         'openpyxl==3.0.3',
         'python_docx==0.8.10',
         'PyPDF2==1.26.0',
         'pdf2image==1.6.0',
         'matplotlib',
         'docx',
         'PyMuPDF==1.16.18',
         'python_dateutil',
         'Pillow'
   ],
   python_requires='>=3.7',
   package_dir={'': '.'},
   packages=['wllib2','wllib2.lib_tests','wllib2.env_lib','wllib2.az_lib','wllib2.db_lib','wllib2.pdf_lib','wllib2.img_lib','wllib2.test_lib']
)