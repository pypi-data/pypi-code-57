import os
import glob
import sys
import time
import subprocess
from osgeo import gdal
import raster_tools as rt

# data_path = '/Volumes/GoogleDrive/My Drive/ET_1km'
# os.chdir(data_path)
ref_file = '/Volumes/MyBookThunderboltDuo/fire_data/globe_BAF_P_500m_2001.tif'


data_path = '/Volumes/MyBookThunderboltDuo'
os.chdir(data_path)

for i in range(1, 2):
    year = 2000 + i
    in_file = [ 'modis/NBAR_500m/NBAR_summer_500m_2001.tif','NBAR_500m/mcd43a4_nbarnir_summer_500m_2001-0000000000-0000000000.tif']
    out_file0 = '/Volumes/MyBookThunderboltDuo/modis/NBAR_500m/NBAR_summer_500m_{}.vrt'.format(year)
    in_file_string = ' '.join('"{}"'.format(i) for i in in_file)
    gdal_expression = 'gdalbuildvrt "{}" {}'.format(out_file0, in_file_string)
    print(gdal_expression)
    subprocess.check_output(gdal_expression, shell=True)
    out_file = '/Volumes/MyBookThunderboltDuo/modis/NBAR_500m/NBAR_summer_500m_{}_new.tif'.format(year)
    rt.raster_clip(ref_file, out_file0, out_file, resampling_method='average', srcnodata='nan', dstnodata='nan')