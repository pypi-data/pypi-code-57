"""
Retrieve PyCCD attributes and results for the pixel coordinates
"""
from itertools import repeat
import sys
from cytoolz import merge
from lcmap_tap.date_utils import gen_dates
from lcmap_tap.date_utils import gen_sday_eday
from lcmap_tap.logger import log, exc_handler
from lcmap_tap.RetrieveData import tiles
from lcmap_tap.storage import ceph, local

sys.excepthook = exc_handler


def get_cache_or_ceph(cache_type, chip_coord):
    """
    Check cache for a chip. If not found, download from ceph.
    Args:
        chip_coord: The upper left coordinate of the chip in projected meters
        cache_type: a string representing the type of cache to check.
                    (ard, pixel, segment)
    Returns: A list of the chip's json data.
    """
    # Attempt to retrieve from cache
    cached_file = local.read_cache(cache_type=cache_type, chip_coord_ul=chip_coord)

    if cached_file:
        log.debug("Using file from local cache.")
        return cached_file

    # Data type to ceph retrieval function mapping
    get_type = {
        "pixel": ceph.get_pixel,
        "segment": ceph.get_segment,
    }

    log.debug("Downloading file from object storage.")
    chip = get_type[cache_type](chip_coord.x, chip_coord.y)

    if chip:
        log.debug("Saving file to cache.")
        local.save_cache(
            cache_type=cache_type, cache_data=chip, chip_coord_ul=chip_coord
        )

    return chip


def get_cover_range(chip_coord, grid, tile_id, proc_dates):
    """
    Download a date range of land cover products.
    Args:
      chip_coord: The upper left coordinate of the chip in projected meters.
      grid: String of the grid name. ("cu", "ak", "hi")
      tile_id: A string of the tile id.
      proc_dates: A list of processing date strings. ([YYYY-MM-DD,...])
    Returns: A list of land cover products from a start year to end year.
    """
    return list(
        map(
            ceph.get_cover,
            repeat(chip_coord.x),
            repeat(chip_coord.y),
            repeat(grid),
            repeat(tile_id),
            proc_dates,
        )
    )


def filter_pixels_cover(chip_cover, px_index):
    """
    Pull out the target pixels from a list of land cover chip products.
    Args:
      chip_cover: A list of chips containing pixel land cover data.
      px_index: An int index of the target pixel to extract from each chip.
    Returns: A list of pixels as dictionaries with land cover product data.
    """
    return list(map(lambda chip: chip[px_index], chip_cover))


def get_ccd_cover(
    chip_coord,
    pixel_coord,
    date_start="1985-07-01",
    date_stop="2017-07-01",
    grid="cu",
    dataset="ard",
):
    """
    Get the land cover product values for a pixel, from a chip.
    Args:
        chip_coord: The upper left coordinate of the chip in projected meters.
        pixel_coord: The upper left coordinate of the pixel in projected meters.
        date_start: String for the starting date to collect cover products. (YYYY-MM-DD)
        date_stop: String for the ending date to collect cover products. (YYYY-MM-DD)
        grid: String of the grid name. ("cu", "ak", "hi")
        dataset: String of the dataset name. ("ard")
    Returns: A list of diciontaries of land cover product data.
    """
    log.debug(
        "Retrieving pixel's land cover product data from chip (%s, %s)",
        chip_coord.x,
        chip_coord.y,
    )

    # convert chip coord to get a tile id
    tile_id = tiles.xy_to_tile(
        grid=grid, dataset=dataset, coords={"x": chip_coord.x, "y": chip_coord.y}
    )

    # Build the list of processing date strings.
    proc_dates = gen_dates(date_start=date_start, date_end=date_stop)

    # Download the range of cover products
    chip_cover = get_cover_range(
        chip_coord=chip_coord,
        grid=grid,
        tile_id=tile_id,
        proc_dates=proc_dates,
    )

    # Index of the pixel to pull from each chip's cover product
    px_index = tiles.pixel_index(
        grid=grid,
        dataset=dataset,
        pixel_coords={"x": pixel_coord.x, "y": pixel_coord.y},
    )

    # Filter the list of chip cover data down to a list of the target pixel
    px_cover = filter_pixels_cover(chip_cover, px_index)

    # Generate the start/end dates
    se_dates = gen_sday_eday(proc_dates)

    # Combine the pixel cover data with the associated start/end dates
    return list(map(merge, px_cover, se_dates))


def get_ccd_pixel_mask(chip_coord, pixel_coord):
    """
    Get the pixel mask result from a chip.
    Args:
        chip_coord: The upper left coordinate of the chip in projected meters
        pixel_coord: The upper left coordinate of the pixel in projected meters
    Returns: A list of the chip's pixel's processing mask
    """
    log.debug("Retrieving chip's pixel data (%s, %s)", chip_coord.x, chip_coord.y)
    chip_with_pixel = get_cache_or_ceph(cache_type="pixel", chip_coord=chip_coord)
    return pixel_ccd_info(chip_with_pixel, pixel_coord)[0]["mask"]


def get_ccd_segment(chip_coord, pixel_coord):
    """
    Get the segment model data for a chip.
    Args:
        chip_coord: The upper left coordinate of the chip in projected meters
        pixel_coord: The upper left coordinate of the pixel in projected meters
    Returns: dictionary of chip segment model data
    """
    log.debug("Retrieving chip's segment data (%s, %s)", chip_coord.x, chip_coord.y)
    chip_segment = get_cache_or_ceph(cache_type="segment", chip_coord=chip_coord)
    return pixel_ccd_info(chip_segment, pixel_coord)


def pixel_ccd_info(results_chip: str, coord) -> dict:
    """
    Find the CCD output for a specific pixel from within the chip by
    matching the pixel coordinates.

    Args:
        results_chip: JSON object
        coord: Upper left coordinate of the target pixel in projected meters

    Returns:
        All of the information stored in the target JSON for the specific pixel coordinate
    """
    return list(
        filter(lambda x: coord.x == x["px"] and coord.y == x["py"], results_chip)
    )
