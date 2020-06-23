"""
local - functions that utilize local storage
"""
import os
import sys
import json
import pickle
import yaml
import lcmap_tap
from lcmap_tap.logger import log, exc_handler

sys.excepthook = exc_handler


##-- Config File Functions --##
def load_config(cfg="config.yaml"):
    """
    Load external configuration if it exists.
    Args: cfg - string path to the name of the config file to load.
    Returns: config file data structure or None if file doesn't exist.
    """
    if os.path.exists(cfg):
        with open(cfg, "r") as f:
            return yaml.load(f, Loader=yaml.FullLoader)
    return None


##-- Cache File Saving/Writing to Disk --##
def save_cache(cache_type, cache_data, chip_coord_ul):
    """
    Save the passed in file object to local cache space.
    Args:
      cache_type: a string representing the type of cache to check.
                 (ard, pixel, segment)
      cache_data: the data object ()
      chip_coord_ul: The chip upper left x/y coordinates
    Returns: None. Side effect of file write.
    """
    lcmap_tap.mkdirs(cache_dir_name(file_type=cache_type))
    cache_file = cache_file_path(file_type=cache_type, chip_coord_ul=chip_coord_ul)
    save_cache_file(cache_data=cache_data, file_name=cache_file)


def save_cache_file(cache_data, file_name):
    """
    Attempt to save the cache data to a file.
    Args:
      cache_data: the cache data to save.
      file_name: the file name to save to.
    Returns: None. Side effect of file write.
    """
    if file_name.endswith(".p"):
        save_pickle(cache_data=cache_data, file_name=file_name)
    else:
        save_json(cache_data=cache_data, file_name=file_name)


def save_json(cache_data, file_name):
    """
    Save a json file object to local disk.
    Args:
      file_name: The json file to save to local disk.
    Returns: None. Side effect of file write.
    """
    with open(file_name, "w") as f:
        json.dump(cache_data, f)


def save_pickle(cache_data, file_name):
    """
    Save a pickle file object to local disk.
    Args:
      file_name: The pickle file to save to local disk.
    Returns: None. Side effect of file write.
    """
    with open(file_name, "wb") as f:
        pickle.dump(cache_data, f)


##-- Cache File Loading/Reading from Disk --##
def read_cache(cache_type, chip_coord_ul):
    """
    Check the local disk cache for a file.
    Args:
      cache_type: a string representing the type of cache to check.
                 (ard, pixel, segment)
      chip_coord_ul: The chip upper left x/y coordinates
    Returns:
      A list containing either the cached file contents or empty if file is not cached.
    """
    cache_file = cache_file_path(file_type=cache_type, chip_coord_ul=chip_coord_ul)
    loaded_file = load_cache_file(file_name=cache_file)
    return loaded_file


def load_cache_file(file_name):
    """
    Attempt to load a cached file.
    Args:
      file_name: full path to the file that should be loaded.
    Returns:
      the loaded file object if it exists, otherwise, an empty list.
    """
    if file_name.endswith(".p"):
        load_function = load_pickle
    else:
        load_function = load_json

    try:
        with open(file_name) as f:
            loaded_file = load_function(f)
    except FileNotFoundError:
        log.info("Cache MISS - (%s) not found.", file_name)
        return []
    else:
        log.info("Cache HIT - (%s) found.", file_name)

    return loaded_file


def load_json(file_name):
    """
    Load a json file object into memory.
    Args:
      file_name: The json file to load.
    Returns:
      The loaded json file object.
    """
    return json.load(file_name)


def load_pickle(file_name):
    """
    Load a pickle file object into memory.
    Args:
      file_name: The pickle file to load.
    Returns:
      A loaded pickle file object.
    """
    return pickle.load(file_name)


##-- Cache File Name Generation --##
def cache_file_path(file_type, chip_coord_ul):
    """
    Generates the full path to the cache file.
    Args:
      file_type: a string representing the type of cache to check.
                 (ard, pixel, segment)
      chip_coord_ul: The chip upper left x/y coordinates
    """
    return os.path.join(
        cache_dir_name(file_type=file_type),
        cache_file_name(file_type=file_type, chip_coord_ul=chip_coord_ul),
    )


def cache_dir_name(file_type):
    """
    Generate the name for the directory path to search for cache.
    Args:
      file_type: a string representing the type of cache to check.
                 (ard, pixel, segment)
    Returns: a string of the directory path.
    """
    return os.path.join(lcmap_tap.home(), file_type + "_cache")


def cache_file_name(file_type, chip_coord_ul):
    """
    Generate the name for the file to search for in cache.
    Args:
      file_type: a string representing the type of cache to check.
                 (ard, pixel, segment)
      chip_coord_ul: The chip upper left x/y coordinates
    Returns:
      A string of the filename to search cache for.
    """
    if file_type == "ard":
        return f"{chip_coord_ul.x}-{chip_coord_ul.y}.p"
    return f"{chip_coord_ul.x}-{chip_coord_ul.y}.json"
