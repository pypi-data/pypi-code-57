"""
ceph - provide capability to retrieve data stored in Ceph,
an S3 compatible object storage.

URL scheme is:

http://host:port/bucket/datatype/cX-cY.json

host:port -> s3 endpoint
bucket -> bucket name
datatype -> 'pixel' or 'segment'
cX -> chip x coordinate (projected meters)
xY -> chip y coordinate (projected meters)
"""
import os
import lcmap_tap
from lcmap_tap.RetrieveData import http_client
from lcmap_tap.storage import local

config_file = os.path.join(lcmap_tap.top_dir(), "config.yaml")
main_cfg = local.load_config(config_file)

if main_cfg:
    config = {
        # environment variables over ride external config file
        "s3_url": os.environ.get("S3_URL", main_cfg["S3_URL"]),
        "s3_bucket": os.environ.get("S3_BUCKET", main_cfg["S3_BUCKET"]),
        "s3_get_timeout": os.environ.get("S3_GET_TIMEOUT", main_cfg["S3_GET_TIMEOUT"]),
    }
else:
    config = {
        "s3_url": os.environ.get("S3_URL", "http://localhost:7484"),
        "s3_bucket": os.environ.get("S3_BUCKET", "test-bucket"),
        "s3_get_timeout": os.environ.get("S3_GET_TIMEOUT", 9),
    }


def get_cover(cx, cy, grid, tile_id, proc_date):
    """
    Download a land cover product.
    Args: cx - chip x coordinate.
          cy - chip y coordinate.
          grid - A string of the grid to get tiles from. (cu, ak, hi)
          tile_id - A string of the tile_id.
          proc_date - String of the YYYY-MM-DD processing date.
    """
    session = http_client.setup_session()
    obj_key = object_key(
        cover_key(
            cx=cx,
            cy=cy,
            grid=grid,
            tile_id=tile_id,
            proc_date=proc_date,
        ),
        config,
    )
    return http_client.try_download(session, obj_key, load_timeout(config))


def get_pixel(cx, cy):
    """
    Download a pixel.
    Args: cx - chip x coordinate
          cy - chip y coordinate
    Returns the json pixel content.
    """
    session = http_client.setup_session()
    obj_key = object_key(pixel_key(cx=cx, cy=cy), config)
    return http_client.try_download(session, obj_key, load_timeout(config))


def get_segment(cx, cy):
    """
    Download a segment.
    Args: cx - chip x coordinate
          cy - chip y coordinate
    Returns the json segment content.
    """
    session = http_client.setup_session()
    obj_key = object_key(segment_key(cx=cx, cy=cy), config)
    return http_client.try_download(session, obj_key, load_timeout(config))


def cover_key(cx, cy, grid, tile_id, proc_date):
    """
    Return the land cover filename convention.
    Args: cx - chip x coordinate.
          cy - chip y coordinate.
          grid - A string of the grid to get tiles from. (cu, ak, hi)
          tile_id - A string of the tile_id.
          proc_date - String of the YYYY-MM-DD processing date.
    """
    tile_h = tile_id[:3]
    tile_v = tile_id[3:6]
    prod_year = proc_date[:4]
    return f"json/{prod_year}/{grid.upper()}/{tile_h}/{tile_v}/cover/{cx}.0/{cy}.0/cover-{cx}.0-{cy}.0-{proc_date}.json"


def pixel_key(cx, cy):
    """
    Return the pixel filename convention.
    Args: cx - chip x coordinate
          cy - chip y coordinate
    """
    return f"pixel/{cx}-{cy}.json"


def segment_key(cx, cy):
    """
    Return the segment filename convention.
    Args: cx - chip x coordinate
          cy - chip y coordinate
    """
    return f"segment/{cx}-{cy}.json"


def bucket(cfg):
    """
    Return the bucket name
    Args: cfg - dictionary config of endpoint url/bucket
    """
    return f"{cfg['s3_url']}/{cfg['s3_bucket']}"


def object_key(key, cfg):
    """
    Return the full path to the object in storage
    Args: key - the s3/ceph object key
          cfg - dictionary config of endpoint url/bucket
    """
    return f"{bucket(cfg)}/{key}"


def load_timeout(cfg):
    """
    Load the timeout (seconds) value from the config.
    Args: Dictionary config containing the timeout value.
    Returns: An integer representing the timeout in seconds.
    """
    timeout_val = int(cfg["s3_get_timeout"])
    if timeout_val < 0:
        return 0
    return timeout_val
