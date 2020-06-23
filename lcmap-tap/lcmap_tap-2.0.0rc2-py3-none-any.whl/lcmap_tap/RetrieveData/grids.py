"""
grid - provide capability to retrieve tile grid information.
"""
import os
from cytoolz import first
import lcmap_tap
from lcmap_tap.RetrieveData import http_client
from lcmap_tap.storage import local

config_file = os.path.join(lcmap_tap.top_dir(), "config.yaml")
main_cfg = local.load_config(config_file)

if main_cfg:
    config = {
        "ard_base_url": os.environ.get("ARD_BASE_URL", main_cfg["ARD_BASE_URL"]),
        "ard_cu": os.environ.get("ARD_CU", main_cfg["ARD_CU"]),
    }
else:
    config = {
        "ard_base_url": os.environ.get("ARD_BASE_URL", "http://localhost:5656"),
        "ard_cu": os.environ.get("ARD_CU", "/"),
    }


##-- User Facing Functions --##
def list_grids():
    """
    List available grids.
    Args: None.
    Returns: A list of grids.
    """
    return ["cu", "ak", "hi"]


##-- Grid Functions --##
def tile_grid(grid, dataset):
    """
    Returns the tile grid information.
    Args:
      grid: String of the grid name. ("cu", "ak", "hi")
      dataset: String of the dataset name. ("ard")
    Returns: A dictionary of the grid info.
    """
    grid_data = grid_info(grid=grid, dataset=dataset)

    return first(list(filter(lambda x: x["name"] == "tile", grid_data)))


def chip_grid(grid, dataset):
    """
    Returns the chip grid information.
    Args:
      grid: String of the grid name. ("cu", "ak", "hi")
      dataset: String of the dataset name. ("ard")
    Returns: A dictionary of the grid info.
    """
    grid_data = grid_info(grid=grid, dataset=dataset)

    return first(list(filter(lambda x: x["name"] == "chip", grid_data)))


def grid_info(grid, dataset):
    """
    Return a grid's information.
    Args:
      grid: String of the grid name. ("cu", "ak", "hi")
      dataset: String of the dataset name. ("ard")
    Returns: A dictionary of the grid information.
    """
    session = http_client.setup_session()
    obj_key = object_key(url_path(config, grid=grid, dataset=dataset) + "/grid", config)

    return http_client.try_download(session, obj_key)


def registry_info(grid, dataset):
    """
    Return registry layer information.
    Args:
      grid: String of the grid name. ("cu", "ak", "hi")
      dataset: String of the dataset name. ("ard")
    Returns: A list of dictionaries of the registry information.
    """
    session = http_client.setup_session()
    obj_key = object_key(
        url_path(config, grid=grid, dataset=dataset) + "/registry", config
    )

    return http_client.try_download(session, obj_key)


def snap_info(grid, dataset, coords):
    """
    Snap an x,y coordinate to the closest upper left pair.
    Args:
      grid: String of the grid name. ("cu", "ak", "hi")
      dataset: String of the dataset name. ("ard")
      coords: A dictionary of the x,y coordinate pair to snap.
    Returns: A dictionary of the closest tile,chip.
    """
    session = http_client.setup_session()
    obj_key = object_key(
        url_path(config, grid=grid, dataset=dataset) + "/grid/snap", config
    )

    return http_client.try_download(session, obj_key, params=coords)


##-- Coordinate Systems Functions --##
def coord_system_meters(grid, dataset):
    """
    Return the well known text (WKT) for Albers Equal Area WGS 84
    projected meters.
    Args:
      grid: String of the grid name. ("cu", "ak", "hi")
      dataset: String of the dataset name. ("ard")
    Returns: A string of the projected well known text.
    """
    return tile_grid(grid=grid, dataset=dataset)["proj"]


def coord_system_geo(grid, dataset):
    """
    Return the well known text (WKT) for WGS 84 geographic. (lat/long)
    Args:
      grid: String of the grid name. ("cu", "ak", "hi")
      dataset: String of the dataset name. ("ard")
    Note: Args are placeholders in order to provide a uniform
          entry point of meters/geo for a higher level function.
    Returns: A string of the geo well known text.
    """
    return (
        'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],'
        'AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSGS","8901"]],UNIT["degree",'
        '0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]'
    )


##-- String Generation Functions --##
def base_url(cfg):
    """
    Return the base url.
    Args: cfg: dictionary config of endpoint url.
    Returns: A string of the base URL.
    """
    return f"{cfg['ard_base_url']}"


def url_path(cfg, grid, dataset):
    """
    Return the dataset/grid path.
    Args:
      cfg: Dictionary config.
      grid: String of the grid name. ("cu", "ak", "hi")
      dataset: String of the dataset name. ("ard")
    Returns: A string of the URL path.
    """
    return f"{cfg[dataset + '_' + grid]}"


def object_key(key, cfg):
    """
    Return the full path to the object in storage.
    Args: key: The object key.
          cfg: Dictionary config of endpoint url.
    Returns: A string of the full path to the object.
    """
    return f"{base_url(cfg)}/{key}"
