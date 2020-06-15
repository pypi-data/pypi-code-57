"""
Common methods shared between blocks, especially useful for directory handling
and block parameter/query input.
"""
import json
import os
from typing import Callable
from contextlib import ContextDecorator
import pathlib
from enum import Enum
import shutil

import copy
import numpy as np
import rasterio as rio

from geojson import FeatureCollection, Feature

from .stac import STACQuery
from .logging import get_logger

logger = get_logger(__name__)


def ensure_data_directories_exist():
    """Creates required directories for any block input and output (`/tmp/input`,
     `tmp/output`, `/tmp/quicklooks`).
    """
    pathlib.Path("/tmp/input/").mkdir(parents=True, exist_ok=True)
    pathlib.Path("/tmp/output/").mkdir(parents=True, exist_ok=True)
    pathlib.Path("/tmp/quicklooks/").mkdir(parents=True, exist_ok=True)


def setup_test_directories(test_dir: pathlib.Path):
    """Creates given test directory and empty input/output/quicklook subfolders.

    Arguments:
        test_dir: A directory to store temporary files (usually `/tmp` or
            `/tmp/e2e_test`)

    """
    test_dir.mkdir(parents=True, exist_ok=True)

    cleanup_test_directories(test_dir)


def cleanup_test_directories(test_dir: pathlib.Path):
    """Deletes given test directory.

    Arguments:
        test_dir: A directory to store temporary files (usually `/tmp` or \
            `/tmp/e2e_test`)
    """
    if test_dir.exists():
        for folder in ["input", "output", "quicklooks"]:
            try:
                shutil.rmtree(test_dir / folder)
                pathlib.Path(test_dir / folder).mkdir(parents=True, exist_ok=True)
            # Deleting subfolder sometimes does not work in temp, then remove all subfiles.
            except (PermissionError, OSError):
                pathlib.Path(test_dir / folder).mkdir(parents=True, exist_ok=True)
                files_to_delete = pathlib.Path(test_dir / folder).rglob("*.*")
                for file_path in files_to_delete:
                    file_path.unlink()


class TestDirectoryContext(ContextDecorator):
    """Yields the test directory making sure folders exist and cleans up when
    context is closed.
    """

    def __init__(self, test_dir: pathlib.Path):
        """
        Example:
            ```python
            with TestDirectoryContext(pathlib.Path("/tmp")) as test_dir:
                block.process(dir=pathlib.Path("/tmp"))
            ```

        Arguments:
            test_dir: A directory to store temporary files (usually `/tmp`
                or `/tmp/e2e_test`)
        """
        self.test_dir = test_dir

    def __enter__(self) -> pathlib.Path:
        """Context entry point.

        Returns:
            Temporary test directory.
        """
        setup_test_directories(self.test_dir)
        return self.test_dir

    def __exit__(self, *exc):
        """Context exit point. Deletes temporary directory.
        """
        cleanup_test_directories(self.test_dir)
        return False


def load_query(validator: Callable = lambda x: True) -> STACQuery:
    """Get the query for the current task directly from the task parameters
    in `UP42_TASK_PARAMETERS` environment variable.

    Example:
        ```python
        def val(data: dict) -> bool:
            # Ensure bbox is defined.
            return "bbox" in data

        query = load_query(val)
        ```

    Arguments:
        validator: Callable that returns if the loaded query is valid.

    Returns:
        A `STACQuery` object initialized with the parameters if valid.
    """
    data: str = os.environ.get("UP42_TASK_PARAMETERS", "{}")
    logger.debug("Raw task parameters from UP42_TASK_PARAMETERS are: %s", data)
    query_data = json.loads(data)
    return STACQuery.from_dict(query_data, validator)


def load_params() -> dict:
    """Get the parameters for the current task directly from the task
    parameters parameters in `UP42_TASK_PARAMETERS` environment variable.

    Returns:
        Dictionary of task parameters.
    """
    data: str = os.environ.get("UP42_TASK_PARAMETERS", "{}")
    logger.debug("Fetching parameters for this block: %s", data)
    if data == "":
        data = "{}"
    return json.loads(data)


def load_metadata() -> FeatureCollection:
    """Get the geojson metadata input.

    Returns:
        Object defining input features for block.
    """
    ensure_data_directories_exist()
    if os.path.exists("/tmp/input/data.json"):
        with open("/tmp/input/data.json") as fp:
            data = json.loads(fp.read())

        features = []
        for feature in data["features"]:
            features.append(Feature(**feature))

        return FeatureCollection(features)
    else:
        return FeatureCollection([])


def save_metadata(result: FeatureCollection):
    """Save the geojson metadata output.

    Arguments:
        result: Output feature collection.
    """
    ensure_data_directories_exist()
    with open("/tmp/output/data.json", "w") as fp:
        fp.write(json.dumps(result))


class BlockModes(Enum):
    """
    Types of block modes: DRY_RUN or DEFAULT.

    Important:
        Find out more about job modes/block modes in our
        [documentation](https://docs.up42.com/reference/block-envvars.html#up42-job-mode).
    """

    DRY_RUN = "DRY_RUN"
    DEFAULT = "DEFAULT"


def get_block_mode() -> str:
    """Gets the task mode from environment variables. If no task mode is set,
    DEFAULT mode will be returned.

    Important:
        Find out more about job modes/block modes in our
        [documentation](https://docs.up42.com/reference/block-envvars.html#up42-job-mode).

    Returns:
        Block mode.
    """
    value = os.environ.get("UP42_JOB_MODE", BlockModes.DEFAULT.value)
    if value not in [mode.value for mode in BlockModes]:
        value = "DEFAULT"
    return value


def get_block_info() -> dict:
    """Gets the Block Info variable as a dictionary.

    Returns:
        Block info as a dict.
    """
    value_str = str(os.environ.get("UP42_BLOCK_INFO"))
    value_dict = json.loads(value_str)

    return value_dict


def isclose(
    transform1: rio.Affine,
    transform2: rio.Affine,
    rtol: float = 1e-05,
    atol: float = 1e-08,
) -> bool:
    """
    Operator to compare two Affine transformations. Returns true if equal under
    tolerances.

    The tolerance values are positive, typically very small numbers.
    The relative difference (rtol * abs(b)) and the absolute difference
    atol are added together to compare against the absolute difference
    between a and b.

    Arguments:
        transform1: A rasterio transform object.
        transform2: Another rasterio transform object.
        rtol: Relative tolerance for comparison.
        atol: Absolute tolerance for comparison.

    Returns:
        If the two transforms are equal within the given tolerances.

    """
    transform1_ar = np.array(transform1)
    transform2_ar = np.array(transform2)
    return np.allclose(transform1_ar, transform2_ar, rtol=rtol, atol=atol)


def meta_is_equal(meta1: dict, meta2: dict, rtol=1e-05, atol=1e-08) -> bool:
    """
    Operator for comparing two metadata tags provided by a rasterio dataset.

    Compares affine transformations with isclose method.

    Arguments:
        meta1: A meta object.
        meta2: Another meta object.
        rtol: Relative tolerance for comparison.
        atol: Absolute tolerance for comparison.

    Returns:
        If the two meta objects are equal within the given tolerances.

    """
    meta1_transform = meta1.get("transform")
    meta2_transform = meta2.get("transform")

    meta1 = copy.deepcopy(meta1)
    meta2 = copy.deepcopy(meta2)

    del meta1["transform"]
    del meta2["transform"]

    return isclose(meta1_transform, meta2_transform, rtol, atol) and meta1 == meta2
