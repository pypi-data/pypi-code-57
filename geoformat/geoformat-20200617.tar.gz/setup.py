from setuptools import setup

import geoformat

markdown_path = 'README.md'

with open(markdown_path) as read_me_file:
    read_me_file_txt = read_me_file.read()

setup(
    name='geoformat',
    version=str(geoformat.version(verbose=False)),
    url='https://framagit.org/Guilhain/Geoformat',
    license='MIT',
    author='Guilhain Averlant',
    author_email='g.averlant@mailfence.com',
    description='Geoformat is a GDAL/OGR library overlayer',
    long_description=read_me_file_txt,
    long_description_content_type='text/markdown',
    py_modules=['geoformat',
                'geoformat_lib.conf.driver_variable',
                'geoformat_lib.conf.geometry_variable',
                'geoformat_lib.conversion.bytes_conversion',
                'geoformat_lib.conversion.geolayer_conversion',
                'geoformat_lib.conversion.geometry_conversion',
                'geoformat_lib.db.db_request',
                'geoformat_lib.explore_data.print_data',
                'geoformat_lib.explore_data.random_geometry',
                'geoformat_lib.geoprocessing.connectors.operations',
                'geoformat_lib.geoprocessing.connectors.predicates',
                'geoformat_lib.geoprocessing.geoparameters.bbox',
                'geoformat_lib.geoprocessing.geoparameters.boundaries',
                'geoformat_lib.geoprocessing.geoparameters.lines',
                'geoformat_lib.geoprocessing.distance',
                'geoformat_lib.geoprocessing.line_merge',
                'geoformat_lib.geoprocessing.surface',
                ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: GIS",
    ]
)
