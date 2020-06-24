from setuptools import setup

setup(
    name='AGDPK',
    version='1.1.4',
    author='Viktor Xu',
    author_email='viktorxu@qq.com',
    maintainer='Viktor Xu',
    maintainer_email='viktorxu@qq.com',
    url='',
    license='',
    description='a advanced geoscience data processing kit.',
    long_description='',
    platforms=['Windows', 'Ubuntu'],
    packages=[],
    py_modules=['raster_pro', 'vector_pro'],
    requires=[
        'GDAL',
        'imageio',
        'numpy',
        'tqdm'
    ],
    zip_safe=False
)

'''
python setup.py sdist
python setup.py install
twine upload dist/*
'''