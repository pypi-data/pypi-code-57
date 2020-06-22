import os
import glob
import time
import subprocess
import learn2map.raster_tools as rt


# data_path = '/Volumes/MyBookThunderboltDuo/ALOS2_out/alos_10km'
# data_path = '/Users/xuliang/Downloads/TRMM_3B43.7/2018'
# os.chdir(data_path)
# input_mask = '/Users/xuliang/Documents/yy/global_biomass/inputdata/globe_lc_map.tif'
#
# # Raster to Raster (creating all tif files into geotiff with the same dimension and projection as the reference)
# for i in range (17):
#     year=2017+i
#     # in_file = '/Volumes/LACIE01/yy/globe_biomass/output/basemap_rgb.tif'
#     # out_file='basemap_usa.tif'
#     in_file='globe_mcd64_500m_rvdeforet_{}.tif'.format(year)
#     print(in_file)
#     out_file = 'globe_mcd64_10km_rvdeforet_{}.tif'.format(year)
#
#     # expression0 = '(A>0) * (A<6) + (A==8)'
#     # gdal_expression = (
#     #     'gdal_calc.py --creation-option COMPRESS=DEFLATE --creation-option ZLEVEL=9 --creation-option PREDICTOR=2 '
#     #      ' --creation-option BIGTIFF=YES --overwrite --NoDataValue=0 --type=Byte -A "{}" --outfile="{}" --calc="{}"'
#     #      ).format(in_file[0], out_file, expression0)
#     # print(gdal_expression)
#     # subprocess.check_output(gdal_expression, shell=True)
#     # time.sleep(1.5)
#     # output_x = '{}_10km.tif'.format(os.path.splitext(out_file)[0])
#     rt.raster_clip(input_mask, in_file, out_file, resampling_method='average')

# input_mask = '/Volumes/MyBookThunderboltDuo/globbiomass_output/output/Kalimantan_agb_10km.tif'
# infile = '/Volumes/MyBookThunderboltDuo/globbiomass_output/output/global_agb_2014.tif'
# outfile = '/Volumes/MyBookThunderboltDuo/globbiomass_output/output/kalimantan_agb.tif'
# rt.raster_clip(input_mask, infile, outfile, resampling_method='average')
#
# input_mask = '/Volumes/MyBookThunderboltDuo/globbiomass_output/output/GABON_10km.tif'
# infile='/Volumes/MyBookThunderboltDuo/globbiomass_output/output/global_agb_2014.tif'
# outfile='/Volumes/MyBookThunderboltDuo/globbiomass_output/output/gabon_agb.tif'
# rt.raster_clip(input_mask, infile, outfile, resampling_method='average')
#
# input_mask = '/Volumes/MyBookThunderboltDuo/globbiomass_output/output/DRC_10km.tif'
# infile = '/Volumes/MyBookThunderboltDuo/globbiomass_output/output/global_agb_2014.tif'
# outfile = '/Volumes/MyBookThunderboltDuo/globbiomass_output/output/drc_agb.tif'
# rt.raster_clip(input_mask, infile, outfile, resampling_method='average')
#
#
# input_mask = '/Volumes/MyBookThunderboltDuo/globbiomass_output/output/Kalimantan_agb_10km.tif'
# infile = '/Users/xuliang/Documents/yy/global_biomass/inputdata/globe_lc_map.tif'
# outfile = '/Volumes/MyBookThunderboltDuo/globbiomass_output/output/kalimantan_lc.tif'
# rt.raster_clip(input_mask, infile, outfile, resampling_method='average')
#
# input_mask = '/Volumes/MyBookThunderboltDuo/globbiomass_output/output/GABON_10km.tif'
# infile='/Users/xuliang/Documents/yy/global_biomass/inputdata/globe_lc_map.tif'
# outfile='/Volumes/MyBookThunderboltDuo/globbiomass_output/output/gabon_lc.tif'
# rt.raster_clip(input_mask, infile, outfile, resampling_method='average')
#
# input_mask = '/Volumes/MyBookThunderboltDuo/globbiomass_output/output/DRC_10km.tif'
# infile = '/Users/xuliang/Documents/yy/global_biomass/inputdata/globe_lc_map.tif'
# outfile = '/Volumes/MyBookThunderboltDuo/globbiomass_output/output/drc_lc.tif'
# rt.raster_clip(input_mask, infile, outfile, resampling_method='average')

# input_mask = '/Users/xuliang/Documents/yy/global_biomass/inputdata/globe_lc_map.tif'
# infile = '/Users/xuliang/Documents/yy/global_data/LC/output/globe_land.tif'
# outfile = '/Volumes/MyBookThunderboltDuo/globbiomass_output/output/globe_land_10km.tif'
# rt.raster_clip(input_mask, infile, outfile, resampling_method='average')
# input_mask='/Users/xuliang/Documents/yy/for_cc/input/lc_mask025.tif'
# for i in range (12):
#     mon=801+i
#     # in_file = '/Volumes/LACIE01/yy/globe_biomass/output/basemap_rgb.tif'
#     # out_file='basemap_usa.tif'
#     in_file='3B43.201{}01.7.HDF_t.tif'.format(mon)
#     print(in_file)
#     out_file = 'trmm_amazon{}.tif'.format(mon)
#     rt.raster_clip(input_mask, in_file, out_file, resampling_method='average')
# input_mask='/Users/xuliang/Documents/DownLoad/lc_mask025.tif'
# for i in range (12):
#     mon=801+i
#     # in_file = '/Volumes/LACIE01/yy/globe_biomass/output/basemap_rgb.tif'
#     # out_file='basemap_usa.tif'
#     in_file='3B43.201{}01.7.HDF_t.tif'.format(mon)
#     print(in_file)
#     out_file = 'trmm_amazon{}.tif'.format(mon)
#     rt.raster_clip(input_mask, in_file, out_file, resampling_method='average')
# input_mask = '/Users/xuliang/Downloads/drive-download-20190618T172927Z-001/wd0614_pred_mean.tif'
# infile= '/Users/xuliang/Downloads/consensus_full_class_1.tif'
# outfile='/Users/xuliang/Downloads/lc_tropic_class1.tif'
# rt.raster_clip(input_mask, infile, outfile, resampling_method='mode')
#
# input_mask = '/Users/xuliang/Downloads/drive-download-20190618T172927Z-001/wd0614_pred_mean.tif'
# infile= '/Users/xuliang/Downloads/consensus_full_class_2.tif'
# outfile='/Users/xuliang/Downloads/lc_tropic_class2.tif'
# rt.raster_clip(input_mask, infile, outfile, resampling_method='mode')
#
# input_mask = '/Users/xuliang/Downloads/drive-download-20190618T172927Z-001/wd0614_pred_mean.tif'
# infile= '/Users/xuliang/Downloads/consensus_full_class_3.tif'
# outfile='/Users/xuliang/Downloads/lc_tropic_class3.tif'
# rt.raster_clip(input_mask, infile, outfile, resampling_method='mode')
#
# input_mask = '/Users/xuliang/Downloads/drive-download-20190618T172927Z-001/wd0614_pred_mean.tif'
# infile= '/Users/xuliang/Downloads/consensus_full_class_4.tif'
# outfile='/Users/xuliang/Downloads/lc_tropic_class4.tif'
# rt.raster_clip(input_mask, infile, outfile, resampling_method='mode')
# infile= '/Volumes/LACIE01/srtm/global_srtm3_aster_dem_3sec.int'
# outfile= '/Volumes/MyBookThunderboltDuo/srtm/srtm_1km_25.tif'
# outfile1= '/Volumes/MyBookThunderboltDuo/srtm/srtm_1km_75.tif'
# infile = '/Users/xuliang/Documents/yy/tropic_wood_density/ALOS/globe_alos_100m_0710.tif'
# outfile = '/Users/xuliang/Documents/yy/tropic_wood_density/ALOS/globe_alos_1km_0710.tif'
# rt.raster_clip(input_mask, infile, outfile, resampling_method='q1')
# rt.raster_clip(input_mask, infile, outfile1, resampling_method='q3')

# input_mask = '/Users/xuliang/Documents/yy/wd/reference.tif'
# infile= '/Users/xuliang/Documents/yy/global_data/LC/output/globe_lc_500m_2001.tif'
# outfile='/Users/xuliang/Documents/yy/wd/lc_2001_1km.tif'
# rt.raster_clip(input_mask, infile, outfile, resampling_method='mode')

# input_mask = '/Users/xuliang/Downloads/agb_2005_100m.tif'
# infile= '/Users/xuliang/Documents/yy/wd/TEXMHT_M_sl1_250m_ll.tif'
# outfile='/Users/xuliang/Documents/yy/wd/TEXMHT_M_1km_tropic.tif'
# rt.raster_clip(input_mask, infile, outfile, resampling_method='mode')
# year0=(2005, 2010, 2015, 2016)
#
# for i in range(4):
#     year=year0[i]
#     in_file = glob.glob('/Users/xuliang/Downloads/maxent_conus_agb_v7_tsfilter_v1/maxent_conus_agb_{}_v7_tsfilter_v1.int'.format(year))
#     print(in_file)
#     # out_file = '/Users/xuliang/Downloads/agb_{}.tif'.format(year)
#     output_x = '/Users/xuliang/Downloads/agb_100m_{}.tif'.format(year)
#     print(output_x)
#     rt.raster_clip(input_mask, in_file[0], output_x, resampling_method='average')
#
#
#
# for i in range(4):
#     year=year0[i]
#     in_file = glob.glob('/Users/xuliang/Downloads/maxent_conus_bgb_v7_tsfilter_v1/maxent_conus_bgb_{}_v7_tsfilter_v1.int'.format(year))
#     print(in_file)
#     # out_file = '/Users/xuliang/Downloads/bgb_{}.tif'.format(year)
#     output_x = '/Users/xuliang/Downloads/bgb_100m_{}.tif'.format(year)
#     rt.raster_clip(input_mask, in_file[0], output_x, resampling_method='average')
input_mask = '/Volumes/MyBookThunderboltDuo/sf/sf_2008_250m.tif'
infile= '/Volumes/YangBackup/amazon_alos/amazon_2010_combine_100_out.tif'
outfile='/Volumes/MyBookThunderboltDuo/sf/sf_2010_250m.tif'
rt.raster_clip(input_mask, infile, outfile, resampling_method='average')


