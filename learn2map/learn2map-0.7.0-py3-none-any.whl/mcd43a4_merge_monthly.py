import os
import glob
import sys
import subprocess
from osgeo import gdal
import raster_tools as rt

data_path = '/Volumes/MyBookThunderboltDuo/modis/mcd43a4'
os.chdir(data_path)

# input_mask = '/Users/yanyang/Documents/data/gloabal/reference_cut.tif'

for i in range(12):
        mon = i + 1
        in_file = glob.glob('mcd43a4_0110_mon{}-*'.format(mon))
        print(in_file)
        if len(in_file) > 0:
            in_file_string = ' '.join('"{}"'.format(file) for file in in_file)
            out_file = 'mcd43a4_0110_mon{}.vrt'.format(mon)
            gdal_expression = (
                'gdalbuildvrt "{}" {}').format(
                out_file, in_file_string)
            print(gdal_expression)
            subprocess.check_output(gdal_expression, shell=True)

            merge_file = 'globe_mcd43a4_1km_mon{}_new.tif'.format(mon)
            gdal_expression = (
                'gdal_merge.py -co COMPRESS=LZW -co BIGTIFF=YES -of GTiff -o "{}" {}').format(
                merge_file, in_file_string)
            print(gdal_expression)
            subprocess.check_output(gdal_expression, shell=True)