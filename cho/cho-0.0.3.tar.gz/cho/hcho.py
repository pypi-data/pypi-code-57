import os
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
from pathlib import Path

def retrieve_hcho(date_range, download_folder = "data/hcho"):
    download_folder = Path.cwd().joinpath(download_folder)
    if not download_folder.exists(): os.makedirs(download_folder.as_posix())

    URL = 'https://s5phub.copernicus.eu/dhus/'
    product_type = 'L2__HCHO__'

    roi = geojson_to_wkt(read_geojson('roi.geojson'))
    api = SentinelAPI(user='s5pguest', password='s5pguest', api_url='https://s5phub.copernicus.eu/dhus')
    # aoi = 'POINT (41.9 12.5)'

    products = api.query(roi,
                         date = date_range,
                         producttype = product_type
    )


    # convert to Pandas DataFrame
    products_df = api.to_dataframe(products)

    # download sorted and reduced products
    api.download_all(products_df.index,  directory_path = download_folder.as_posix())


# # example
# retrieve_hcho(['20190101','20190131'], download_folder = "data/hcho")