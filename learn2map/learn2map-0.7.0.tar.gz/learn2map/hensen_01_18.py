import os
import glob
import sys
import time
import subprocess
from osgeo import gdal
import raster_tools as rt

data_path = '/Volumes/MyBookThunderboltDuo/gfc_gain_loss_v16'
os.chdir(data_path)
# # for i in range (1):
# #     year=2001+i0
#   out_file = 'globe_forest_loss_30m_{}.vrt'.format(year)
#   ref_file = '/Users/xuliang/Downloads/global_mask_100m.tif'
# # # #     new_file = '/Volumes/MyBookThunderboltDuo/hensen_data/output/global_hensen_100m{}_0110.tif'.format(year)
# # # #     rt.raster_clip(ref_file, out_file, new_file, resampling_method='average', srcnodata='nan', dstnodata='nan')
#
#   new_file1 = '/Volumes/MyBookThunderboltDuo/hensen_data/output/global_hensen_100m_0110.tif'
#   in_file = glob.glob('*.tif')
#   rt.raster_clip(ref_file, in_file, new_file1, resampling_method='average', srcnodata='nan', dstnodata='nan')

# data_path = '/Volumes/MyBookThunderboltDuo/modis/mod44b/input'
# os.chdir(data_path)

ref_file = '/Volumes/MyBookThunderboltDuo/fire_data/globe_BAF_P_500m_2014.tif'
in_file = glob.glob('gfc_lossyear_30m-*')
out_file = '/Volumes/MyBookThunderboltDuo/gfc_gain_loss_v16/output/globe_hensen_30m.vrt'
in_file_string = ' '.join('"{}"'.format(i) for i in in_file)
gdal_expression = 'gdalbuildvrt "{}" {}'.format(out_file, in_file_string)
print(gdal_expression)
subprocess.check_output(gdal_expression, shell=True)
print(in_file)
for i in range (17, 18):
    year=2001+i
    # out_file = 'globe_250m_vcf{}.vrt'
    new_file = '/Volumes/MyBookThunderboltDuo/gfc_gain_loss_v16/output/global_hensen_30m_tf_{}.tif'.format(year)
    expression0 = f'A=={i+1}'
    gdal_expression = (
      'gdal_calc.py --creation-option COMPRESS=LZW --creation-option PREDICTOR=2 '
      #'gdal_calc.py '
      ' --creation-option BIGTIFF=YES --overwrite --type=Byte -A "{}" --outfile="{}" --calc="{}"'
    ).format(out_file, new_file, expression0)
    print(gdal_expression)
    subprocess.check_output(gdal_expression, shell=True)
    time.sleep(1.5)
    output_x = '/Volumes/MyBookThunderboltDuo/gfc_gain_loss_v16/output/global_hensen_500m_pct_{}.tif'.format(year)
    rt.raster_clip(ref_file, new_file, output_x, resampling_method='average', srcnodata='nan', dstnodata='nan')