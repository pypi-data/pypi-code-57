import os
import glob
import sys
import subprocess
from osgeo import gdal
import raster_tools as rt


# data_path= '/Volumes/MyBookThunderboltDuo/ALOS2_out/alos07_10'
# os.chdir(data_path)
#
#
# in_file = glob.glob('alos2a_globe_100m2007_2010*')
# print(in_file)
# out_file = 'globe_alos_100m.vrt'
#
# in_file_string = ' '.join('"{}"'.format(i) for i in in_file)
# gdal_expression = 'gdalbuildvrt "{}" {}'.format(out_file, in_file_string)
# print(gdal_expression)
# subprocess.check_output(gdal_expression, shell=True)
#
# # ref_file = '/Volumes/LACIE01/yy/globe_biomass/inputdata/globe_lc_map.tif'
# merge_file  = '/Users/xuliang/Documents/yy/tropic_wood_density/globe_alos_100m_0710.tif'
# # rt.raster_clip(ref_file, out_file, new_file, resampling_method='average', srcnodata='nan', dstnodata='nan')
#
# # merge_file = '/Users/yanyang/Documents/data/gloabal/LST/output/globe_mod11a2_night_mon{}.tif'.format(mon)
# gdal_expression = (
#   'gdal_merge.py -co COMPRESS=LZW -co BIGTIFF=YES -of GTiff -o "{}" {}').format(
#   merge_file, in_file_string)
# print(gdal_expression)
# subprocess.check_output(gdal_expression, shell=True)
# in_file = glob.glob('p_*')
# print(in_file)
# out_file = 'globe_agb_p_100m.vrt'
#
# in_file_string = ' '.join('"{}"'.format(i) for i in in_file)
# gdal_expression = 'gdalbuildvrt "{}" {}'.format(out_file, in_file_string)
# print(gdal_expression)
# subprocess.check_output(gdal_expression, shell=True)
#
# ref_file = '/Volumes/LACIE01/yy/globe_biomass/inputdata/globe_lc_map.tif'
# new_file = '//Volumes/MyBookThunderboltDuo/ALOS2_out/agb/global_agb_p_10km_2007.tif'
# rt.raster_clip(ref_file, out_file, new_file, resampling_method='average', srcnodata='nan', dstnodata='nan')

# in_file = glob.glob('yeargain_gain_loss*')
# print(in_file)
# out_file = 'globe_forest_gain_30m.vrt'
#
# in_file_string = ' '.join('"{}"'.format(i) for i in in_file)
# gdal_expression = (
#     'gdalbuildvrt "{}" {}').format(
#     out_file, in_file_string)
# print(gdal_expression)
# subprocess.check_output(gdal_expression, shell=True)
#
# ref_file = '/Volumes/LACIE01/yy/globe_biomass/inputdata/globe_lc_map.tif'
# new_file = '/Users/xuliang/Documents/yy/global_data/globe_gfc_10km_gain.tif'
# rt.raster_clip(ref_file, out_file, new_file, resampling_method='average', srcnodata='nan', dstnodata='nan')


# for i in range(16):
#     out_file2 = 'global_hensen_loss_gain_yr{}.tif'.format(i+2000)
#     gdal_expression = (
#         'gdal_calc.py --creation-option="COMPRESS=LZW" -A {} --outfile={} --calc="A=={}"').format(
#         out_file, out_file2, i+1)
#     print(gdal_expression)
#     subprocess.check_output(gdal_expression, shell=True)
#     ref_file = '/Volumes/LACIE01/yy/globe_biomass/inputdata/globe_lc_map.tif'
#     new_file = '/Users/xuliang/Documents/yy/global_data/globe_gfc_10km_yr{}.tif'.format(i+2000)
#     rt.raster_clip(ref_file, out_file2, new_file, resampling_method='average', srcnodata='nan', dstnodata='nan')
#     # subprocess.check_output('rm -f {}'.format(out_file2), shell=True)

data_path = '/Volumes/MyBookThunderboltDuo/modis/NBAR_500m'
os.chdir(data_path)

input_mask = '/Volumes/MyBookThunderboltDuo/modis/reference_500.tif'
in_file = glob.glob('*.tif')

for i in range(0, len(in_file)):
  infile=in_file[i]
  outfile=infile.replace(".tif", "_new.tif")
  rt.raster_clip(input_mask, infile, outfile, resampling_method='average')

