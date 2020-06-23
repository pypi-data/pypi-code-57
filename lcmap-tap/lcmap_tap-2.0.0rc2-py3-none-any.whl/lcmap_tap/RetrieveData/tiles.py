"""
tile - Tile conversion/manipulation functions.
"""
from itertools import repeat
from cytoolz import first
from cytoolz import second
import numpy as np
from osgeo import ogr
from osgeo import osr
from lcmap_tap.RetrieveData.grids import chip_grid
from lcmap_tap.RetrieveData.grids import coord_system_geo
from lcmap_tap.RetrieveData.grids import coord_system_meters
from lcmap_tap.RetrieveData.grids import registry_info
from lcmap_tap.RetrieveData.grids import snap_info
from lcmap_tap.RetrieveData.grids import tile_grid
from lcmap_tap.RetrieveData.tile_list import ak_tiles
from lcmap_tap.RetrieveData.tile_list import cu_tiles
from lcmap_tap.RetrieveData.tile_list import hi_tiles


##-- User Facing Functions --##
def list_tiles(grid):
    """
    List available tiles from a given grid.
    Args:
      grid: A string of the grid to get tiles from.
    Returns: A list of tiles.
    """
    grid_tiles = {"cu": cu_tiles, "ak": ak_tiles, "hi": hi_tiles}

    return grid_tiles.get(grid.lower(), [])()


def hv_longlat(grid, dataset):
    """
    Generate a list of tile h,v with all four longitude,latitude corner coordinates.
    Args:
      grid: A string of the grid to get tiles from.
            ("cu", "ak", "hi")
      dataset: String of the dataset name. ("ard")
    Returns:
      A data structure containing each tile's h,v and
      corner coordinates (ul, ur, lr, ll) in long,lat.
      Example first entry (cu ard):
        [({'h': 32, 'v': 3},
          {'tile_ul': {'x': -66.88687358195142, 'y': 45.66670475157042},
           'tile_ur': {'x': -65.06382101099217, 'y': 45.247388249191694},
           'tile_lr': {'x': -65.663840908373, 'y': 43.969944528447435},
           'tile_ll': {'x': -67.45610994454883, 'y': 44.38016421334179}}),
    """
    # Convert the tile id list to h,v
    tiles_hv = list(map(string_to_tile, list_tiles(grid)))

    # Generate the tile long,lat list
    tile_coords = list(map(to_xy, repeat(grid), repeat(dataset), list_tiles(grid)))
    tile_corners = list(map(xy_corners, repeat(grid), repeat(dataset), tile_coords))
    tile_longlat = list(
        map(
            convert_corners,
            repeat(grid),
            repeat(dataset),
            tile_corners,
            repeat("meters"),
            repeat("latlong"),
        )
    )

    # Combine the hv and longlat lists
    return list(zip(tiles_hv, tile_longlat))


def to_xy(grid, dataset, tile_id):
    """
    Get the x,y coordinates of a tile.
    Args:
      grid: String of the grid name. ("cu", "ak", "hi")
      dataset: String of the dataset name. ("ard")
      tile_id: String of the tile id to convert.
    Returns: Dictionary of the tile's upper left x,y coordinates.
    """
    tg = tile_grid(grid, dataset)
    tg_info = {
        "rx": tg["rx"],
        "ry": tg["ry"],
        "tx": tg["tx"],
        "ty": tg["ty"],
        "sx": tg["sx"],
        "sy": tg["sy"],
    }

    h_v = string_to_tile(tile_id)

    return to_projection(tg_info, h_v)


def xy_to_tile(grid, dataset, coords):
    """
    Get the tile id given x,y coordinates.
    Args:
      grid: String of the grid name. ("cu", "ak", "hi")
      dataset: String of the dataset name. ("ard")
      coords: Dictionary of x,y values.
    Returns: String of the tile id.
    """
    snap_xy = snap_info(grid=grid, dataset=dataset, coords=coords)["tile"]
    snap_x = int(first(snap_xy["grid-pt"]))
    snap_y = int(second(snap_xy["grid-pt"]))
    return tile_to_string({"h": snap_x, "v": snap_y})


def pixel_index(grid, dataset, pixel_coords):
    """
    Determine the index of a pixel in a flattened chip array.
    Args:
      grid: String of the grid name. ("cu", "ak", "hi")
      dataset: String of the dataset name. ("ard")
      pixel_coords: Dictionary of pixel x,y values.
    Returns: An integer of the pixel index.
    """
    # Determine the upper left coordinate of the chip, given a pixel coord
    snap_xy = snap_info(grid=grid, dataset=dataset, coords=pixel_coords)["chip"]
    snap_x = int(first(snap_xy["proj-pt"]))
    snap_y = int(second(snap_xy["proj-pt"]))

    # Gather the pixel size and count for row/col index calculations
    px_size = pixel_size(grid, dataset)
    px_count = second(chip_size(grid, dataset)) / second(px_size)

    # Find the index of the pixel in a flattened chip array
    pixel_col = abs((snap_x - pixel_coords["x"]) / first(px_size))
    pixel_row = abs(((snap_y - pixel_coords["y"]) / second(px_size)) * px_count)
    pixel_pos = int(pixel_col + pixel_row)

    return pixel_pos


def chip_size(grid, dataset):
    """
    Determine the chip size inside of the tile.
    Args:
      grid: String of the grid name. ("cu", "ak", "hi")
      dataset: String of the dataset name. ("ard")
    Returns: A tuple of the chip size. (sx, sy)
    """
    chip_info = chip_grid(grid, dataset)
    return chip_info["sx"], chip_info["sy"]


def pixel_size(grid, dataset):
    """
    Determine the pixel size inside of the chip.
    Args:
      grid: String of the grid name. ("cu", "ak", "hi")
      dataset: String of the dataset name. ("ard")
    Returns: A tuple of the pixel size. (sx, sy)
    """
    size_chip = chip_size(grid, dataset)
    pixels_in_chips = first(registry_info(grid, dataset))["data_shape"]
    pixels_x = first(size_chip) / first(pixels_in_chips)
    pixels_y = second(size_chip) / second(pixels_in_chips)
    return pixels_x, pixels_y


def convert_xy_latlong(grid, dataset, coords, src, dest):
    """
    Get the latitude,longitude given x,y coordinates or
    the x,y coordinates given latitude,longitude.
    Args:
      grid: String of the grid name. ("cu", "ak", "hi")
      dataset: String of the dataset name. ("ard")
      coords: Dictionary of x,y values.
      src: The source unit given. ("latlong" or "meters")
      dest: The unit to convert to. ("latlong" or "meters")
    Returns: A dictionary with 'x' and 'y' keys.
    """
    units = {"meters": coord_system_meters, "latlong": coord_system_geo}

    in_srs = osr.SpatialReference()
    in_srs.ImportFromWkt(units[src](grid=grid, dataset=dataset))

    out_srs = osr.SpatialReference()
    out_srs.ImportFromWkt(units[dest](grid=grid, dataset=dataset))

    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(coords["x"], coords["y"])

    transform = osr.CoordinateTransformation(in_srs, out_srs)
    point.Transform(transform)

    return {"x": point.GetX(), "y": point.GetY()}


def xy_corners(grid, dataset, tile_xy):
    """
    Get a tile's x,y coordinates of each corner.
    Args:
      grid: String of the grid name. ("cu", "ak", "hi")
      dataset: String of the dataset name. ("ard")
      tile_xy: A dictionary of tile x/y coordinates.
    Returns: A dictionary of x,y coordinates.
    """
    xy_intervals = interval(grid=grid, dataset=dataset)

    # Ensure the passed in x,y tile coordinate is a true upper left coordinate
    snap_xy = snap_info(grid=grid, dataset=dataset, coords=tile_xy)["tile"]
    snap_x = first(snap_xy["proj-pt"])
    snap_y = second(snap_xy["proj-pt"])

    # Build the tile corner coordinates
    tile_ul = {"x": snap_x, "y": snap_y}
    tile_ur = {"x": snap_x + xy_intervals["x_int"], "y": snap_y}
    tile_lr = {"x": snap_x + xy_intervals["x_int"], "y": snap_y + xy_intervals["y_int"]}
    tile_ll = {"x": snap_x, "y": snap_y + xy_intervals["y_int"]}

    return {
        "tile_ul": tile_ul,
        "tile_ur": tile_ur,
        "tile_lr": tile_lr,
        "tile_ll": tile_ll,
    }


def convert_corners(grid, dataset, tile_corners, src, dest):
    """
    Convert a tile's x,y points from either meters/lat,long to either lat,long/meters.
    Args:
      grid: String of the grid name. ("cu", "ak", "hi")
      dataset: String of the dataset name. ("ard")
      tile_corners: A dictionary of tile ul,ur,lr,ll x,y points.
      src: The source unit given. ("latlong" or "meters")
      dest: The unit to convert to. ("latlong" or "meters")
    Returns: A dictionary of the converted values.
    Example data structure for input/output:
       {'tile_ul': {'x': 2084415.0, 'y': 2414805.0},
        'tile_ur': {'x': 2234415.0, 'y': 2414805.0},
        'tile_lr': {'x': 2234415.0, 'y': 2264805.0},
        'tile_ll': {'x': 2084415.0, 'y': 2264805.0}}
    """
    conv_tile = {}

    for corner in tile_corners:
        conv_tile[corner] = convert_xy_latlong(
            grid=grid, dataset=dataset, coords=tile_corners[corner], src=src, dest=dest
        )

    return conv_tile


##-- Tile Transformations --##
def to_projection(tg, h_v):
    """
    Convert a tile to projected x/y coordinates.
    Args:
      tg: A dictionary of tile grid information.
      h_v: A dictionary of the horizontal/vertical tile id.
    Returns: a dictionary of the x/y projected coordinates.
    """
    pm = point_matrix(h_v)
    tm = transform_matrix(tg)

    matrix_inversed = np.linalg.inv(tm)
    matrix_mul = matrix_inversed.dot(pm)

    return {"x": first(first(matrix_mul)), "y": first(second(matrix_mul))}


def point_matrix(h_v):
    """
    Return a matrix given a dictionary of h/v ids.
    Args: A dictionary of a tile id horizontal, vertical numbers.
    Returns: A numpy array of the horizontal,vertical nums and a constant.
    """
    return np.array([[h_v["h"]], [h_v["v"]], [1]])


def transform_matrix(tile_grid_info):
    """
    Generate the transform matrix from a given grid spec.
    Args: A dictionary containing the tile grid coordinate information.
    Returns: A numpy array of transform data.
    """
    rx = tile_grid_info["rx"]
    ry = tile_grid_info["ry"]
    sx = tile_grid_info["sx"]
    sy = tile_grid_info["sy"]
    tx = tile_grid_info["tx"]
    ty = tile_grid_info["ty"]

    return np.array([[(rx / sx), 0, (tx / sx)], [0, (ry / sy), (ty / sy)], [0, 0, 1.0]])


def string_to_tile(tile_id):
    """
    Convert a tile string to int. (no leading zeros)
    Args: A string of the 6 digit tile id.
    Returns: A dictionary with the tile id h and v as integers.
    """
    h_num = int(tile_id[0:3])
    v_num = int(tile_id[3:])

    return {"h": h_num, "v": v_num}


def tile_to_string(h_v):
    """
    Convert a tile hv to a tile id string.
    Args:
      h_v: A dictionary of a tile id horizontal, vertical numbers.
    Returns: A string of the tile id.
    """
    return f"{h_v['h']:03}{h_v['v']:03}"


def interval(grid, dataset):
    """
    Get the tile intervals for x and y.
    Args:
      grid: String of the grid name. ("cu", "ak", "hi")
      dataset: String of the dataset name. ("ard")
    Returns: A dictionary of the x,y intervals for a tile.
    """
    tgrid = tile_grid(grid=grid, dataset=dataset)
    x_interval = tgrid["rx"] * tgrid["sx"]
    y_interval = tgrid["ry"] * tgrid["sy"]

    return {"x_int": x_interval, "y_int": y_interval}
