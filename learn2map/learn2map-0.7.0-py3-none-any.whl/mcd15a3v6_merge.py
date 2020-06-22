import os
import glob
import sys
import subprocess
from osgeo import gdal
import raster_tools as rt

data_path = '/Volumes/MyBookThunderboltDuo/modis/mcd15a3v6'
os.chdir(data_path)

# input_mask = '/Users/yanyang/Documents/data/gloabal/reference_cut.tif'

for i in range(13):
        year = i + 2003
        in_file = glob.glob('mcd15a3v6_day_1km_monthly_{}-*'.format(year))
        print(in_file)
        if len(in_file) > 0:
            in_file_string = ' '.join('"{}"'.format(file) for file in in_file)
            out_file = 'mcd15a3v6_monly_{}.vrt'.format(year)
            gdal_expression = (
                'gdalbuildvrt "{}" {}').format(
                out_file, in_file_string)
            print(gdal_expression)
            subprocess.check_output(gdal_expression, shell=True)

            merge_file = 'globe_mcd15a3v6_1km_{}.tif'.format(year)
            gdal_expression = (
                'gdal_merge.py -co COMPRESS=LZW -co BIGTIFF=YES -of GTiff -o "{}" {}').format(
                merge_file, in_file_string)
            print(gdal_expression)
            subprocess.check_output(gdal_expression, shell=True)