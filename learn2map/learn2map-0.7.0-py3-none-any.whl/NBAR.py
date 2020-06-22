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
# for i in range (2,19):
#     year = 2000 + i
#     # modis et
#     in_file = glob.glob('mod16a2_ET_1km_monthly_{}-*'.format(year))
#     out_file0 = 'ET_1km_{}.vrt'.format(year)
#     in_file_string = ' '.join('"{}"'.format(i) for i in in_file)
#     gdal_expression = 'gdalbuildvrt "{}" {}'.format(out_file0, in_file_string)
#     print(gdal_expression)
#     subprocess.check_output(gdal_expression, shell=True)
#     out_file = '/Volumes/MyBookThunderboltDuo/modis/ET_1km/Modis_ET_1km_{}.tif'.format(year)
#     rt.raster_clip(ref_file, out_file0, out_file, resampling_method='average', srcnodata='nan', dstnodata='nan')
#     # modis lst

# data_path = '/Volumes/MyBookThunderboltDuo/NBAR_500m'
# os.chdir(data_path)
#
# for i in range(11, 19):
#     year = 2000 + i
#     in_file = glob.glob('mcd43a4_nbarnir_winter_500m_{}*'.format(year))
#     out_file0 = '/Volumes/MyBookThunderboltDuo/modis/NBAR_500m/NBAR_winter_500m_{}.vrt'.format(year)
#     in_file_string = ' '.join('"{}"'.format(i) for i in in_file)
#     gdal_expression = 'gdalbuildvrt "{}" {}'.format(out_file0, in_file_string)
#     print(gdal_expression)
#     subprocess.check_output(gdal_expression, shell=True)
#     out_file = '/Volumes/MyBookThunderboltDuo/modis/NBAR_500m/NBAR_winter_500m_{}.tif'.format(year)
#     rt.raster_clip(ref_file, out_file0, out_file, resampling_method='average', srcnodata='nan', dstnodata='nan')



# data_path = '/Volumes/MyBookThunderboltDuo/NBAR_500m'
# os.chdir(data_path)
#
# for i in range(9, 13):
#     year = 2000 + i
#     in_file = glob.glob('mcd43a4_nbarnir_summer_500m_{}*'.format(year))
#     out_file0 = '/Volumes/MyBookThunderboltDuo/modis/NBAR_500m/NBAR_summer_500m_{}.vrt'.format(year)
#     in_file_string = ' '.join('"{}"'.format(i) for i in in_file)
#     gdal_expression = 'gdalbuildvrt "{}" {}'.format(out_file0, in_file_string)
#     print(gdal_expression)
#     subprocess.check_output(gdal_expression, shell=True)
#     out_file = '/Volumes/MyBookThunderboltDuo/modis/NBAR_500m/NBAR_summer_500m_{}.tif'.format(year)
#     rt.raster_clip(ref_file, out_file0, out_file, resampling_method='average', srcnodata='nan', dstnodata='nan')




# data_path = '/Volumes/MyBookThunderboltDuo/NBAR_500m'
# os.chdir(data_path)
# #
# for i in range(19, 20):
#     year = 2000 + i
#     in_file = glob.glob('mcd43a4_nbarnir_mean_500m_{}*'.format(year))
#     out_file0 = 'NBAR_mean_500m_{}.vrt'.format(year)
#     in_file_string = ' '.join('"{}"'.format(i) for i in in_file)
#     gdal_expression = 'gdalbuildvrt "{}" {}'.format(out_file0, in_file_string)
#     print(gdal_expression)
#     subprocess.check_output(gdal_expression, shell=True)
#     out_file = '/Volumes/MyBookThunderboltDuo/modis/NBAR_500m/NBAR_mean_500m_{}.tif'.format(year)
#     rt.raster_clip(ref_file, out_file0, out_file, resampling_method='average', srcnodata='nan', dstnodata='nan')

# data_path = '/Volumes/MyBookThunderboltDuo/NBAR_500m'
# os.chdir(data_path)
#
# for i in range(0, 20):
#     year = 2000 + i
#     in_file = glob.glob('mcd43a4_nbarnir_std_500m_{}*'.format(year))
#     out_file0 = 'NBAR_std_500m_{}.vrt'.format(year)
#     in_file_string = ' '.join('"{}"'.format(i) for i in in_file)
#     gdal_expression = 'gdalbuildvrt "{}" {}'.format(out_file0, in_file_string)
#     print(gdal_expression)
#     subprocess.check_output(gdal_expression, shell=True)
#     out_file = '/Volumes/MyBookThunderboltDuo/modis/NBAR_500m/NBAR_std_500m_{}.tif'.format(year)
#     rt.raster_clip(ref_file, out_file0, out_file, resampling_method='average', srcnodata='nan', dstnodata='nan')

data_path = '/Volumes/MyBookThunderboltDuo/modis/NBAR_500m'
os.chdir(data_path)

input_mask = '/Volumes/MyBookThunderboltDuo/modis/reference_500.tif'
in_file = glob.glob('*.tif')

for i in range(0, len(in_file)):
  infile=in_file[i]
  outfile=infile.replace(".tif", "_new.tif")
  rt.raster_clip(input_mask, infile, outfile, resampling_method='average')