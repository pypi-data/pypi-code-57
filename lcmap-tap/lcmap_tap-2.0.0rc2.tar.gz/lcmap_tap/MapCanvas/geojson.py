"""
geojson - Generate Geographic JSON features for inclusion in
           the map overlay.
"""
import os
from jinja2 import Template
import lcmap_tap
from lcmap_tap.logger import log
from lcmap_tap.RetrieveData import tiles


def write_tile_overlay(grid, dataset):
    """
    Write the GeoJSON tile overlay file if it does not exist.
    This file is expected by the (UseWeb[Engine]View) index.html files and used by
    the javascript map feature overlay.
    Args:
      grid: A string of the grid to get tiles from.
            ("cu", "ak", "hi")
      dataset: String of the dataset name. ("ard")
    Returns: None. Side effect of a file write.
    """
    out_file = os.path.join(js_overlay_path(), js_overlay_file(grid))

    if not os.path.isfile(out_file):
        log.info("Map tile overlay not found. Generating now...please wait.")
        js_hv_tiles = hv_tiles(grid, dataset)

        with open(out_file, "w") as f:
            f.write(js_hv_tiles)

        log.info("Map tile overlay generated.")


def js_overlay_path():
    """
    Return the path to the javascript hv tile overlay file.
    Args: None.
    Returns: A string of the path.
    """
    return os.path.join(lcmap_tap.top_dir(), "MapCanvas")


def js_overlay_file(grid):
    """
    Returns the filename of the javascript hv tile overlay file.
    Args:
      grid: A string of the grid to get tiles from.
            ("cu", "ak", "hi")
    Returns: A string of the file name.
    """
    return "hv-tiles-" + grid + ".js"


def hv_tiles(grid, dataset):
    """
    Generate GeoJSON features for inclusion in a Javascript map overlay.
    Args:
      grid: A string of the grid to get tiles from.
            ("cu", "ak", "hi")
      dataset: String of the dataset name. ("ard")
    Returns: A json object for direct Javascript GeoJSON variable use.
    """
    # Get all of the tile h,v and coordinates
    hv_longlat = tiles.hv_longlat(grid, dataset)

    # Build the jinja2 template variables
    jinja_template_vars = list(map(template_vars, range(len(hv_longlat)), hv_longlat))

    # Render each template var with a jinja2 template object
    jinja_template = Template(feature_template())
    feature_list = list(map(jinja_template.render, jinja_template_vars))

    # Build the javascript variable to be used for geojson features
    js_hv_tiles = header() + "\n" + ",\n".join(feature_list) + "\n" + footer()

    return js_hv_tiles


## Static Header/Footer strings
def header():
    """
    Return the geo json header for the javascript file.
    Args: None.
    Returns: A string of the javascript header for geojson feature entries.
    """
    return """var hv_tiles = [{
  "type": "FeatureCollection",
  "name": "ncompare_test",
  "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
  "features": ["""


def footer():
    """
    Return the geo json footer for the javascript file.
    Args: None.
    Returns: A string of the javascript footer for geojson feature entries.
    """
    return "]}];"


## GeoJSON Templating
def feature_template():
    """
    Return a geo json feature template string.
    Args: None.
    Returns: A string of the jinja2 template to plug variables into.
    """
    return """\
    { "type": "Feature", "properties": { "Name": "h{{tile_h}}v{{tile_v}}", "Description": "<html xmlns:fo=\\"http:\\/\\/www.w3.org\\/1999\\/XSL\\/Format\\" xmlns:msxsl=\\"urn:schemas-microsoft-com:xslt\\"> <head> <META http-equiv=\\"Content-Type\\" content=\\"text\\/html\\"> <meta http-equiv=\\"content-type\\" content=\\"text\\/html; charset=UTF-8\\"> <\\/head> <body style=\\"margin:0px 0px 0px 0px;overflow:auto;background:#FFFFFF;\\"> <table style=\\"font-family:Arial,Verdana,Times;font-size:12px;text-align:left;width:100%;border-collapse:collapse;padding:3px 3px 3px 3px\\"> <tr style=\\"text-align:center;font-weight:bold;background:#9CBCE2\\"> <td>h{{tile_h}}v{{tile_v}}<\\/td> <\\/tr> <tr> <td> <table style=\\"font-family:Arial,Verdana,Times;font-size:12px;text-align:left;width:100%;border-spacing:0px; padding:3px 3px 3px 3px\\"> <tr> <td>FID<\\/td> <td>{{fid}}<\\/td> <\\/tr> <tr bgcolor=\\"#D4E4F3\\"> <td>h<\\/td> <td>{{tile_h}}<\\/td> <\\/tr> <tr> <td>v<\\/td> <td>{{tile_v}}<\\/td> <\\/tr> <tr bgcolor=\\"#D4E4F3\\"> <td>h_v<\\/td> <td>h{{tile_h}}v{{tile_v}}<\\/td> <\\/tr> <\\/table> <\\/td> <\\/tr> <\\/table> <\\/body> <\\/html>" }, "geometry": { "type": "MultiPolygon", "coordinates": [ [ [ [ {{ll_long}}, {{ll_lat}}, 0.0 ], [ {{lr_long}}, {{lr_lat}}, 0.0 ], [ {{ur_long}}, {{ur_lat}}, 0.0 ], [ {{ul_long}}, {{ul_lat}}, 0.0 ], [ {{ll_long}}, {{ll_lat}}, 0.0 ] ] ] ] } }"""


def template_vars(fid, tile_info):
    """
    Map tile variables to values used to populate the geojson feature template.
    Args:
      fid: An integer to be used for the feature id.
      tile_info: A list/tuple of a tile hv values dict and corner coordinate pairs dict.
    Returns: A dictionary of variables to apply to a jinja2 string template.
    """
    tile_hv = 0
    tile_coords = 1
    return {
        "fid": fid,
        "tile_h": tile_info[tile_hv]["h"],
        "tile_v": tile_info[tile_hv]["v"],
        "ll_long": tile_info[tile_coords]["tile_ll"]["x"],
        "ll_lat": tile_info[tile_coords]["tile_ll"]["y"],
        "lr_long": tile_info[tile_coords]["tile_lr"]["x"],
        "lr_lat": tile_info[tile_coords]["tile_lr"]["y"],
        "ur_long": tile_info[tile_coords]["tile_ur"]["x"],
        "ur_lat": tile_info[tile_coords]["tile_ur"]["y"],
        "ul_long": tile_info[tile_coords]["tile_ul"]["x"],
        "ul_lat": tile_info[tile_coords]["tile_ul"]["y"],
    }
