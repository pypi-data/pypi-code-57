# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2015-2020 Comet ML INC
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************

from __future__ import print_function

import calendar
import functools
import getpass
import io
import json
import logging
import math
import numbers
import operator
import os
import os.path
import random
import re
import tempfile
import time
from collections import defaultdict
from datetime import datetime

import six
from pkg_resources import DistributionNotFound, get_distribution
from requests.models import PreparedRequest

from ._typing import (
    IO,
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    Union,
)

LOGGER = logging.getLogger(__name__)
LOG_ONCE_CACHE = set()  # type: Set[str]

if six.PY2:
    from StringIO import StringIO
else:
    StringIO = io.StringIO


if hasattr(time, "monotonic"):
    get_time_monotonic = time.monotonic
else:
    # Python2 just won't have accurate time durations
    # during clock adjustments, like leap year, etc.
    get_time_monotonic = time.time

try:
    import numpy

    HAS_NUMPY = True
except ImportError:
    LOGGER.warning("numpy not installed; some functionality will be unavailable")
    HAS_NUMPY = False


INFINITY = float("inf")


def fix_special_floats(value, _inf=INFINITY, _neginf=-INFINITY):
    """ Fix out of bounds floats (like infinity and -infinity) and Not A
    Number.
    Returns either a fixed value that could be JSON encoded or the original
    value.
    """

    try:
        if hasattr(value, "numpy"):
            value = value.numpy()

        # Check if the value is Nan, equivalent of math.isnan
        if math.isnan(value):
            return "NaN"

        elif value == _inf:
            return "Infinity"

        elif value == _neginf:
            return "-Infinity"

    except Exception:
        # Value cannot be compared
        return value

    return value


def log_once_at_level(logging_level, message, *args, **kwargs):
    """
    Log the given message once at the given level then at the DEBUG
    level on further calls.

    This is a global log-once-per-session, as ooposed to the
    log-once-per-experiment.
    """
    global LOG_ONCE_CACHE

    if message not in LOG_ONCE_CACHE:
        LOG_ONCE_CACHE.add(message)
        LOGGER.log(logging_level, message, *args, **kwargs)
    else:
        LOGGER.debug(message, *args, **kwargs)


def merge_url(url, params):
    """
    Given an URL that might have query strings,
    combine with additional query strings.

    Args:
        url - a url string (perhaps with a query string)
        params - a dict of additional query key/values

    Returns: a string
    """
    req = PreparedRequest()
    req.prepare_url(url, params)
    return req.url


def is_iterable(value):
    try:
        iter(value)
        return True

    except TypeError:
        return False


def is_list_like(value):
    """ Check if the value is a list-like
    """
    if is_iterable(value) and not isinstance(value, six.string_types):
        return True

    else:
        return False


def to_utf8(str_or_bytes):
    if hasattr(str_or_bytes, "decode"):
        return str_or_bytes.decode("utf-8", errors="replace")

    return str_or_bytes


def local_timestamp():
    # type: () -> int
    """ Return a timestamp in a format expected by the backend (milliseconds)
    """
    now = datetime.utcnow()
    timestamp_in_seconds = calendar.timegm(now.timetuple()) + (now.microsecond / 1e6)
    timestamp_in_milliseconds = int(timestamp_in_seconds * 1000)
    return timestamp_in_milliseconds


def wait_for_empty(check_function, timeout, verbose=False, sleep_time=1):
    """ Wait up to TIMEOUT seconds for the messages queue to be empty
    """
    end_time = time.time() + timeout
    while check_function() is False and time.time() < end_time:
        if verbose is True:
            LOGGER.info("Still uploading")
        # Wait a max of sleep_time, but keep checking to see if
        # check_function is done. Allows wait_for_empty to end
        # before sleep_time has elapsed:
        end_sleep_time = time.time() + sleep_time
        while check_function() is False and time.time() < end_sleep_time:
            time.sleep(sleep_time / 20)


def read_unix_packages(package_status_file="/var/lib/dpkg/status"):
    # type: (str) -> Optional[List[str]]
    if os.path.isfile(package_status_file):
        package = None
        os_packages = []
        with open(package_status_file, "rb") as fp:
            for binary_line in fp:
                line = binary_line.decode("utf-8", errors="ignore").strip()
                if line.startswith("Package: "):
                    package = line[9:]
                if line.startswith("Version: "):
                    version = line[9:]
                    if package is not None:
                        os_packages.append((package, version))
                    package = None
        os_packages_list = sorted(
            [("%s=%s" % (package, version)) for (package, version) in os_packages]
        )
        return os_packages_list
    else:
        return None


def image_data_to_file_like_object(
    image_data,
    file_name,
    image_format,
    image_scale,
    image_shape,
    image_colormap,
    image_minmax,
    image_channels,
):
    # type: (Union[IO[bytes], Any], Optional[str], str, float, Optional[Sequence[int]], Optional[str], Optional[Sequence[float]], str) -> Union[IO[bytes], None, Any]
    """
    Ensure that the given image_data is converted to a file_like_object ready
    to be uploaded
    """
    try:
        import PIL.Image
    except ImportError:
        PIL = None

    ## Conversion from standard objects to image
    ## Allow file-like objects, numpy arrays, etc.
    if hasattr(image_data, "numpy"):  # pytorch tensor
        array = image_data.numpy()
        fp = array_to_image_fp(
            array,
            image_format,
            image_scale,
            image_shape,
            image_colormap,
            image_minmax,
            image_channels,
        )

        return fp
    elif hasattr(image_data, "eval"):  # tensorflow tensor
        array = image_data.eval()
        fp = array_to_image_fp(
            array,
            image_format,
            image_scale,
            image_shape,
            image_colormap,
            image_minmax,
            image_channels,
        )

        return fp
    elif PIL is not None and isinstance(image_data, PIL.Image.Image):  # PIL.Image
        ## filename tells us what format to use:
        if file_name is not None and "." in file_name:
            _, image_format = file_name.rsplit(".", 1)
        fp = image_to_fp(image_data, image_format)

        return fp
    elif image_data.__class__.__name__ == "ndarray":  # numpy array
        fp = array_to_image_fp(
            image_data,
            image_format,
            image_scale,
            image_shape,
            image_colormap,
            image_minmax,
            image_channels,
        )

        return fp
    elif hasattr(image_data, "read"):  # file-like object
        return image_data
    elif isinstance(image_data, (tuple, list)):  # list or tuples
        if not HAS_NUMPY:
            LOGGER.error("The Python library numpy is required for this operation")
            return None
        array = numpy.array(image_data)
        fp = array_to_image_fp(
            array,
            image_format,
            image_scale,
            image_shape,
            image_colormap,
            image_minmax,
            image_channels,
        )
        return fp
    else:
        LOGGER.error("invalid image file_type: %s", type(image_data))
        if PIL is None:
            LOGGER.error("Consider installing the Python Image Library, PIL")
        return None


def array_to_image_fp(
    array,
    image_format,
    image_scale,
    image_shape,
    image_colormap,
    image_minmax,
    image_channels,
):
    # type: (Any, str, float, Optional[Sequence[int]], Optional[str], Optional[Sequence[float]], str) -> Optional[IO[bytes]]
    """
    Convert a numpy array to an in-memory image
    file pointer.
    """
    image = array_to_image(
        array, image_scale, image_shape, image_colormap, image_minmax, image_channels
    )
    return image_to_fp(image, image_format)


def array_to_image(
    array,
    image_scale=1.0,
    image_shape=None,
    image_colormap=None,
    image_minmax=None,
    image_channels=None,
    mode=None,
):
    # type: (Any, float, Optional[Sequence[int]], Optional[str], Optional[Sequence[float]], Optional[str], Optional[str]) -> Optional[Any]
    """
    Convert a numpy array to an in-memory image.
    """
    try:
        import PIL.Image
        import numpy
        from matplotlib import cm
    except ImportError:
        LOGGER.error(
            "The Python libraries PIL, numpy, and matplotlib are required for this operation"
        )
        return None

    array = numpy.array(array)

    ## Handle image transformations here
    ## End up with a 0-255 PIL Image
    if image_minmax is not None:
        minmax = image_minmax
    else:  # auto minmax
        flatten_array = flatten(array)
        min_array = min(flatten_array)
        max_array = max(flatten_array)
        if min_array == max_array:
            min_array = min_array - 0.5
            max_array = max_array + 0.5
        min_array = math.floor(min_array)
        max_array = math.ceil(max_array)
        minmax = [min_array, max_array]

    ## if a shape is given, try to reshape it:
    if image_shape is not None:
        try:
            ## array shape is opposite of image size(width, height)
            array = array.reshape(image_shape[1], image_shape[0])
        except Exception:
            LOGGER.info("WARNING: invalid image_shape; ignored", exc_info=True)

    ## If 3D, but last array is flat, make it 2D:
    if len(array.shape) == 3 and array.shape[-1] == 1:
        array = array.reshape((array.shape[0], array.shape[1]))
    elif len(array.shape) == 1:
        ## if 1D, make it 2D:
        array = numpy.array([array])
    if image_channels == "first" and len(array.shape) == 3:
        array = numpy.moveaxis(array, 0, -1)

    ### Ok, now let's colorize and scale
    if image_colormap is not None:
        ## Need to be in range (0,1) for colormapping:
        array = rescale_array(array, minmax, (0, 1), "float")
        try:
            cm_hot = cm.get_cmap(image_colormap)
            array = cm_hot(array)
        except Exception:
            LOGGER.info("WARNING: invalid image_colormap; ignored", exc_info=True)
        ## rescale again:
        array = rescale_array(array, (0, 1), (0, 255), "uint8")
        ## Convert to RGBA:
        image = PIL.Image.fromarray(array, "RGBA")
    else:
        ## Rescale (0, 255)
        array = rescale_array(array, minmax, (0, 255), "uint8")
        image = PIL.Image.fromarray(array)

    if image_scale != 1.0:
        image = image.resize(
            (int(image.size[0] * image_scale), int(image.size[1] * image_scale))
        )

    ## Put in a standard mode:
    if mode:
        image = image.convert(mode)
    elif image.mode not in ["RGB", "RGBA"]:
        image = image.convert("RGB")
    return image


def dataset_to_sprite_image(
    matrix,
    size,
    preprocess_function=None,
    transparent_color=None,
    background_color_function=None,
):
    # type: (Any, Sequence[int], Optional[Callable], Optional[Sequence[int]], Optional[Callable]) -> Any
    """
    Convert a dataset (array of arrays) into a giant image of
    images (a sprite sheet).

    Args:
        matrix: array of vectors or Images
        size: (width, height) of each thumbnail image
        preprocess_function: function to preprocess image values
        transparent_color: color to mark as transparent
        background_color_function: function that takes index, returns a color

    Returns: image
    """
    try:
        from PIL import Image
    except ImportError:
        LOGGER.error("The Python library PIL is required for this operation")
        return None

    length = len(matrix)
    sprite_size = math.ceil(math.sqrt(length))

    sprite_image = Image.new(
        mode="RGBA",
        size=(int(sprite_size * size[0]), int(sprite_size * size[1])),
        color=(0, 0, 0, 0),
    )
    if preprocess_function is not None:
        matrix = preprocess_function(matrix)
    for i, array in enumerate(matrix):
        if isinstance(array, Image.Image):
            image = array
        else:
            image = array_to_image(
                array,
                image_scale=1.0,
                image_shape=size,
                image_colormap=None,
                image_minmax=(0, 255),
                image_channels="last",
                mode="RGBA",
            )

            if not image:
                return None

        if transparent_color is not None:
            image = image_transparent_color(image, transparent_color, threshold=1)
        if background_color_function is not None:
            color = background_color_function(i)
            image = image_background_color(image, color)
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        location = (int((i % sprite_size) * size[0]), int((i // sprite_size) * size[1]))
        sprite_image.paste(image, location)
    return sprite_image


def image_background_color(image, color):
    # type: (Any, Sequence[int]) -> Optional[Any]
    """
    Given an image with some transparency, add a background color to it.

    Args:
        image: a PIL image
        color: a red, green, blue color tuple
    """
    try:
        from PIL import Image
    except ImportError:
        LOGGER.error("The Python library PIL is required for this operation")
        return None

    if image.mode != "RGBA":
        raise ValueError(
            "image must have an alpha channel in order to set a background color"
        )

    new_image = Image.new("RGB", image.size, color)
    new_image.paste(image, (0, 0), image)
    return new_image


def image_transparent_color(image, color, threshold=1):
    # type: (Any, Tuple[int, int, int], int) -> Any
    """
    Given a color, make that be the transparent color.

    Args:
        image: a PIL image
        color: a red, green, blue color tuple
        threshold: the max difference in each color component
    """
    try:
        from PIL import Image
        import numpy
    except ImportError:
        LOGGER.error(
            "The Python libraries PIL and numpy are required for this operation"
        )
        return

    image = image.convert("RGBA")
    array = numpy.array(numpy.asarray(image))
    r, g, b, a = numpy.rollaxis(array, axis=-1)
    mask = (
        (numpy.abs(r - color[0]) < threshold)
        & (numpy.abs(g - color[1]) < threshold)
        & (numpy.abs(b - color[2]) < threshold)
    )
    array[mask, 3] = 0
    return Image.fromarray(array, mode="RGBA")


def image_to_fp(image, image_format):
    # type: (Any, str) -> IO[bytes]
    """
    Convert a PIL.Image into an in-memory file
    pointer.
    """
    fp = io.BytesIO()
    image.save(fp, format=image_format)  # save the content to fp
    fp.seek(0)
    return fp


def rescale_array(array, old_range, new_range, dtype):
    """
    Given a numpy array in an old_range, rescale it
    into new_range, and make it an array of dtype.
    """
    if not HAS_NUMPY:
        LOGGER.error("The Python library numpy is required for this operation")
        return

    old_min, old_max = old_range
    if array.min() < old_min or array.max() > old_max:
        ## truncate:
        array = numpy.clip(array, old_min, old_max)
    new_min, new_max = new_range
    old_delta = float(old_max - old_min)
    new_delta = float(new_max - new_min)
    if old_delta == 0:
        return ((array - old_min) + (new_min + new_max) / 2).astype(dtype)
    else:
        return (new_min + (array - old_min) * new_delta / old_delta).astype(dtype)


def write_file_like_to_tmp_file(file_like_object, tmpdir):
    # type: (IO, str) -> str
    # Copy of `shutil.copyfileobj` with binary / text detection

    buf = file_like_object.read(1)

    # Detect binary/text
    if isinstance(buf, six.binary_type):
        tmp_file_mode = "w+b"
    else:
        tmp_file_mode = "w+"

    tmp_file = tempfile.NamedTemporaryFile(mode=tmp_file_mode, dir=tmpdir, delete=False)
    tmp_file.write(buf)

    # Main copy loop
    while True:
        buf = file_like_object.read(16 * 1024)

        if not buf:
            break

        tmp_file.write(buf)

    return tmp_file.name


def table_to_fp(tabular_data, delim, headers):
    # type: (Any, str, Union[Sequence[str], bool]) -> IO
    if isinstance(headers, bool):
        add_headers = headers
    else:
        add_headers = True
    fp = StringIO()
    for row in tabular_data:
        if isinstance(row, (numbers.Number, six.string_types)):
            if add_headers:
                if isinstance(headers, bool):
                    fp.write('"column1"\n')
                else:
                    fp.write('"%s"\n' % (headers[0],))
                add_headers = False
            fp.write(str(row) + "\n")
        else:
            columns = flatten(row)
            if add_headers:
                for i, column in enumerate(columns):
                    if isinstance(headers, bool):
                        column = '"column%s"' % (i + 1)
                    else:
                        column = '"%s"' % (headers[i],)
                    if i == len(columns) - 1:
                        fp.write(column)
                    else:
                        fp.write(column + delim)
                fp.write("\n")
                add_headers = False
            for i, column in enumerate(columns):
                if i == len(columns) - 1:
                    fp.write(str(column))
                else:
                    fp.write(str(column) + delim)
            fp.write("\n")
    fp.seek(0)
    return fp


def data_to_fp(data):
    # type: (Union[bytes, str, Any]) -> Optional[IO]
    if isinstance(data, str):
        fp = StringIO()
        fp.write(data)
    elif isinstance(data, bytes):
        fp = io.BytesIO()
        fp.write(data)
    else:
        fp = StringIO()
        try:
            json.dump(data, fp)
        except Exception:
            LOGGER.error("Failed to log asset data as JSON", exc_info=True)
            return None
    fp.seek(0)
    return fp


def format_bytes(size):
    # type: (int) -> str
    """
    Given a size in bytes, return a sort string representation.
    """
    kbytes = size // 1024
    mbytes = kbytes // 1024
    gbytes = mbytes // 1024
    if gbytes:
        return "%s %s" % (gbytes, "GB")
    elif mbytes:
        return "%s %s" % (mbytes, "MB")
    elif kbytes:
        return "%s %s" % (kbytes, "KB")
    else:
        return "%s %s" % (size, "bytes")


class Embedding(object):
    """
    Data structure for holding embedding template info.
    """

    def __init__(
        self,
        vector_url,
        vector_shape,
        metadata_url,
        sprite_url=None,
        image_size=None,
        title="Comet Embedding",
    ):
        """
        The URL's and sizes for all of the Embedding'
        resources.
        """
        self.vector_url = vector_url
        self.vector_shape = vector_shape
        self.metadata_url = metadata_url
        self.sprite_url = sprite_url
        self.image_size = image_size
        self.title = title

    def to_json(self):
        """
        Return a JSON representation of the embedding
        """
        template = {
            "tensorName": self.title,
            "tensorShape": list(self.vector_shape),
            "tensorPath": self.vector_url,
            "metadataPath": self.metadata_url,
        }
        if self.sprite_url is not None:
            template["sprite"] = {
                "imagePath": self.sprite_url,
                "singleImageDim": list(self.image_size),
            }
        return template


class ConfusionMatrix(object):
    """
    Data structure for holding a confusion matrix of values and their
    labels.
    """

    def __init__(
        self,
        y_true=None,
        y_predicted=None,
        labels=None,
        matrix=None,
        title="Confusion Matrix",
        row_label="Actual Category",
        column_label="Predicted Category",
        max_examples_per_cell=25,
        max_categories=25,
        winner_function=None,
        index_to_example_function=None,
        cache=True,
        selected=None,
        **kwargs  # keyword args for index_to_example_function
    ):
        """
        Create the ConfusionMatrix data structure.

        Args:
            y_true: (optional) a list of target vectors containing
                the correct values for the y_predicted vectors. If
                not provided, then matrix may be provided.
            y_predicted: (optional) a list of output vectors containing
                the predicted values for the y_true vectors. If
                not provided, then matrix may be provided.
            labels: (optional) a list of strings that name of the
                columns and rows, in order. By default, it will be
                "0" through the number of categories (e.g., rows/columns).
            matrix: (optional) the confusion matrix (list of lists).
                Must be square, if given. If not given, then it is
                possible to provide y_true and y_predicted.
            title: (optional) a custom name to be displayed. By
                default, it is "Confusion Matrix".
            row_label: (optional) label for rows. By default, it is
                "Actual Category".
            column_label: (optional) label for columns. By default,
                it is "Predicted Category".
            max_examples_per_cell: (optional) maximum number of
                examples per cell. By default, it is 25.
            max_categories: (optional) max number of columns and rows to
                use. By default, it is 25.
            winner_function: (optional) a function that takes in an
                entire list of rows of patterns, and returns
                the winning category for each row. By default, it is argmax.
            index_to_example_function: (optional) a function
                that takes an index and returns either
                a number, a string, a URL, or a {"sample": str,
                "assetId": str} dictionary. See below for more info.
                By default, the function returns a number representing
                the index of the example.
            cache: (optional) should the results of index_to_example_function
                be cached and reused? By default, cache is True.
            selected: (optional) None, or list of selected category
                indices. These are the rows/columns that will be shown. By
                default, select is None. If the number of categories is
                greater than max_categories, and selected is not provided,
                then selected will be computed automatically by selecting
                the most confused categories.
            kwargs: (optional) any extra keywords and their values will
                be passed onto the index_to_example_function.

        Note:
            The matrix is [row][col] and [real][predicted] order. That way, the
            data appears as it is display in the confusion matrix in the user
            interface on comet.ml.

        Example:

        ```python
        # Typically, you can log the y_true/y_predicted or matrix:

        >>> experiment = Experiment()

        # If you have a y_true and y_predicted:
        >>> y_predicted = model.predict(x_test)
        >>> experiment.log_confusion_matrix(y_true, y_predicted)

        # Or, if you have already computed the matrix:
        >>> experiment.log_confusion_matrix(labels=["one", two", three"],
                                            matrix=[[10, 0, 0]
                                                    [ 0, 9, 1]
                                                    [ 1, 1, 8]])

        # However, if you want to reuse examples from previous runs,
        # you can reuse a ConfusionMatrix instance. You might want to
        # do this if you are creating a series of confusion matrices
        # during the training of a model.
        # See https://staging.comet.ml/docs/quick-start/ for a tutorial.

        >>> cm = ConfusionMatrix()
        >>> y_predicted = model.predict(x_test)
        >>> cm.compute_matrix(y_true, y_predicted)
        >>> experiment.log_confusion_matrix(matrix=cm)

        # Log again, using previously cached values:
        >>> y_predicted = model.predict(x_test)
        >>> cm.compute_matrix(y_true, y_predicted)
        >>> experiment.log_confusion_matrix(matrix=cm)
        ```
        """
        if y_true is not None and y_predicted is not None:
            if matrix is not None:
                raise ValueError(
                    "you need to give either (y_true and y_predicted) or matrix, NOT both"
                )
            # else fine
        elif y_true is None and y_predicted is None:
            pass  # fine
        elif y_true is None or y_predicted is None:
            raise ValueError("if you give y_true OR y_predicted you must give both")

        if winner_function is not None:
            self.winner_function = winner_function  # type: ignore

        if index_to_example_function is not None:
            self.index_to_example_function = index_to_example_function  # type: ignore

        self.y_true = y_true
        self.y_predicted = y_predicted
        self.labels = labels
        self.title = title
        self.row_label = row_label
        self.column_label = column_label
        self.max_examples_per_cell = max_examples_per_cell
        self.max_categories = max_categories
        self.selected = selected
        self.use_cache = cache
        self.clear_cache()
        self.clear()
        self._matrix = None

        if self.y_true is not None and self.y_predicted is not None:
            self.compute_matrix(self.y_true, self.y_predicted, **kwargs)
        elif matrix is not None:
            try:
                self._matrix = convert_to_matrix(matrix, dtype=numbers.Number)
            except Exception:
                LOGGER.error(
                    "convert_to_matrix failed; confusion matrix not generated",
                    exc_info=True,
                )

    def clear(self):
        """
        Clear the matrices and type.
        """
        self.type = None
        self._example_matrix = None
        self._matrix = None

    def clear_cache(self):
        """
        Clear the caches.
        """
        # Set of indices (ints):
        self._cache = set()
        # Map index (int) -> example
        self._cache_example = {}

    def initialize(self):
        """
        Initialize the confusion matrix based on y_true.
        """
        n = len(self.y_true[0])
        self._matrix = self._create_matrix((n, n), 0)
        self._example_matrix = self._create_matrix((n, n), None)

    def winner_function(self, ndarray):
        """
        A default winner function. Takes a list
        of patterns to apply winner function to.

        Args:
            ndarry: a 2-D matrix where rows are the patterns

        Returns a list of winning categories.
        """
        try:
            from numpy import argmax

            def winner(ndarray):
                return argmax(ndarray, axis=1)

        except ImportError:
            # numpy is faster, but not required
            log_once_at_level(
                logging.INFO,
                "numpy not installed; using a slower "
                + "winner_function for confusion matrix",
            )

            def winner(ndarray):
                # Even if the following code is doing two iterations on the
                # list, most of the computation is done by C code
                return [array.index(max(array)) for array in ndarray]

        return winner(ndarray)

    def index_to_example_function(self, index, **kwargs):
        """
        User-provided function.

        Args:
            index: the index of the pattern being tested
            kwargs: additional keyword arguments for an overridden method

        Returns:
            * an integer representing the winning cateory
            * a string representing a example
            * a string representing a URL (starts with "http")
            * a dictionary containing keys "sample" and "assetId"

        The return dictionary is used to link a confusion matrix cell
        with a Comet asset. In this function, you can create an asset
        and return a dictionary, like so:

        ```python
        # Example index_to_example_function
        def index_to_example_function(index):
            # x_test is user's inputs (just an example):
            image_array = x_test[index]
            # Make an asset name:
            image_name = "confusion-matrix-%05d.png" % index
            # Make an asset:
            results = experiment.log_image(
                image_array, name=image_name, image_shape=(28, 28, 1)
            )
            # Return the example name and assetId
            return {"sample": image_name, "assetId": results["imageId"]}

        # Then, pass it to ConfusionMatrix(), or log_confusion_matrix()
        ```
        """
        return index

    def _set_type_from_example(self, example):
        """
        Take the cached example and set the global
        confusion matrix type.

        Args:
            example: an int or dict
        """
        if isinstance(example, int):
            self.type = "integer"
        elif isinstance(example, dict):
            if example["assetId"] is not None:
                self.type = "image"
            elif example["sample"].startswith("http"):
                self.type = "link"
            else:
                self.type = "string"
        else:
            raise TypeError("unknown example type: %r" % example)

    def _process_new_example(self, example, index):
        """
        Turn the user's return value into a proper example.  Sets the type
        based on user's value.

        Args:
            example: a new example from user function
            index: the index of the example

        Side-effect: saves in cache if possible.
        """
        if isinstance(example, int):
            self.type = "integer"
        elif isinstance(example, str):
            if example.startswith("http"):
                self.type = "link"
            else:
                self.type = "string"
            example = {
                "index": index,  # index
                "sample": example,  # example
                "assetId": None,  # assetId
            }
        elif isinstance(example, dict):
            # a dict of index (int), assetId (string), example (string)
            if "sample" not in example or "assetId" not in example:
                raise ValueError(
                    "index_to_example_function must return {'sample': ..., 'assetId': ...}"
                )
            # Add the index, in case not already in:
            if "index" not in example:
                example["index"] = index
            # Set the confusion matrix type:
            if "type" in example:
                self.type = example["type"]
                # Remove from dict:
                del example["type"]
            else:  # default type
                self.type = "image"
        else:
            raise ValueError(
                "index_to_example_function must return an int, string, URL, or {'sample': string, 'assetId': string}"
            )
        if self.type != "integer" and self.use_cache:
            self._put_example_in_cache(index, example)
        return example

    def _index_to_example(self, index, **kwargs):
        """
        Wrapper around user function/cache.

        Args:
            index: the index of the example
            kwargs: passed to user function
        """
        if self.use_cache and self._example_in_cache(index):
            example = self._get_example_from_cache(index)
            self._set_type_from_example(example)
            return example

        try:
            example = self.index_to_example_function(index, **kwargs)
        except Exception:
            LOGGER.error(
                "The index_to_example_function failed for index %s; example not generated",
                index,
                exc_info=True,
                extra={"show_traceback": True},
            )
            example = index
        example = self._process_new_example(example, index)

        return example

    def _create_matrix(self, shape, initial_value):
        """
        Create a matrix with initial value of initial_value.

        Args:
            shape: shape of matrix (row, col)
            initial_value: initial value for cell
        """
        return [[initial_value for x in range(shape[1])] for y in range(shape[0])]

    def _get_example_from_cache(self, index):
        """
        Get a example from the example cache.

        Args:
            index: the index of example
        """
        key = index
        return self._cache_example[key]

    def _example_in_cache(self, index):
        """
        Is the example in the example cache?

        Args:
            index: the index of example
        """
        key = index
        return key in self._cache_example

    def _put_example_in_cache(self, index, example):
        """
        Put a example in the example cache.

        Args:
            index: the index of example
            example: the processed example
        """
        key = index
        self._cache_example[key] = example

    def _example_from_list(self, indices, x, y, **kwargs):
        """
        Example from indices so that it is no more than max length.
        Use previous indices from cache.

        Args:
            indices: the indices of the patterns to example from
            x: the column of example cell
            y: the row of example cell
            kwargs: keyword args to pass to user function
        """
        if len(indices) <= self.max_examples_per_cell:
            retval = set(indices)
        else:
            indices = list(indices)
            retval = list(self._cache.intersection(indices))
            # If you need more:
            retval += [
                indices.pop(random.randint(0, len(indices) - 1))
                for i in range(self.max_examples_per_cell - len(retval))
            ]
            # Return minimum needed:
            retval = set(retval[: self.max_examples_per_cell])

        new_ones = retval - self._cache
        if self.index_to_example_function is not None:
            examples = []
            for index in retval:
                example = self._index_to_example(index, **kwargs)
                examples.append(example)
            self._example_matrix[x][y] = examples
        # Update the ones sent:
        if self.use_cache:
            self._cache.update(new_ones)
        return retval

    def compute_matrix(
        self, y_true, y_predicted, index_to_example_function=None, **kwargs
    ):
        """
        Compute the confusion matrix.

        Args:
            y_true: list of vectors representing the targets
            y_predicted: list of vectors representing predicted
                values
            index_to_example_function: (optional) a function
                that takes an index and returns either
                a number, a string, a URL, or a {"sample": str,
                "assetId": str} dictionary. See below for more info.
                By default, the function returns a number representing
                the index of the example.

        Note: uses winner_function to compute winning category.
        """
        if len(y_true) != len(y_predicted):
            raise ValueError(
                "y_true and y_predicted should have the same lengths; %s != %s"
                % (len(y_true), len(y_predicted))
            )
        if len(y_true[0]) != len(y_predicted[0]):
            raise ValueError(
                "y_true[0] and y_predicted[0] should have the same lengths; %s != %s"
                % (len(y_true[0]), len(y_predicted[0]))
            )
        self.y_true = y_true
        self.y_predicted = y_predicted
        if index_to_example_function is not None:
            self.index_to_example_function = index_to_example_function
        self.initialize()

        # Keep track of all indices for each cell:
        # Create confusion matrix:
        xs = self.winner_function(y_true)
        ys = self.winner_function(y_predicted)

        examples = defaultdict(set)
        for (i, (x, y)) in enumerate(zip(xs, ys)):
            # Add count to cell:
            self._matrix[x][y] += 1
            # Add index to cell:
            examples[(x, y)].add(i)

        # Example all cells that have items (reuse from cache/other cells if possible):
        for key in examples:
            x, y = key
            self._example_from_list(examples[key], x, y, **kwargs)

    def to_json(self):
        """
        Return the associated confusion matrix as the JSON to
        upload.
        """
        if (
            self.y_true is not None
            and len(self.y_true[0]) > self.max_categories
            and self.selected is None
        ):
            # Sort row by worst performing:
            correct_counts = [(i, self._matrix[i][i]) for i in range(len(self._matrix))]
            ordered_rows = sorted(correct_counts, key=lambda pair: pair[1])
            self.selected = [row[0] for row in ordered_rows[: self.max_categories]]

        if self.selected is not None:
            # Make sure sorted, smallest to largest:
            self.selected = sorted(self.selected)

        if self.labels is None:
            if self.selected is not None:
                labels = [str(v) for v in self.selected]
            elif self._matrix is not None:
                labels = [str(v) for v in range(len(self._matrix[0]))]
            else:
                labels = []
        else:
            if self.selected is not None:
                labels = [
                    label for (i, label) in enumerate(self.labels) if i in self.selected
                ]
            else:
                labels = self.labels
        if self._example_matrix is not None:
            smatrix = self._example_matrix if any(self._example_matrix) else None
            if smatrix is not None and self.selected is not None:
                smatrix = [
                    [smatrix[row][col] for col in self.selected]
                    for row in self.selected
                ]
        else:
            smatrix = None
        if smatrix is None:
            self.type = None
        if self.selected is not None:
            matrix = [
                [self._matrix[row][col] for col in self.selected]
                for row in self.selected
            ]
        else:
            matrix = self._matrix
        if matrix is not None:
            if len(matrix) != len(labels):
                raise ValueError(
                    "The length of labels does not match number of categories"
                )
        return {
            "version": 1,
            "title": self.title,
            "labels": labels,
            "matrix": matrix,
            "rowLabel": self.row_label,
            "columnLabel": self.column_label,
            "maxSamplesPerCell": self.max_examples_per_cell,
            "sampleMatrix": smatrix,
            "type": self.type,
        }

    def display(self, space=4):
        """
        Display an ASCII version of the confusion matrix.

        Args:
            space: (optional) column width
        """

        def format(string):
            print(("%" + str(space) + "s") % str(string)[: space - 1], end="")

        json_format = self.to_json()
        total_width = len(json_format["matrix"]) * space
        row_label = json_format["rowLabel"] + (" " * total_width)
        format(row_label[0])
        format("")
        print(json_format["title"].center(total_width))
        format(row_label[1])
        format("")
        print(json_format["columnLabel"].center(total_width))
        format(row_label[2])
        format("")
        for row in range(len(json_format["matrix"])):
            format(json_format["labels"][row])
        print()
        format(row_label[3])
        for row in range(len(json_format["matrix"])):
            format(json_format["labels"][row])
            for col in range(len(json_format["matrix"][row])):
                format(json_format["matrix"][row][col])
            print()
            format(row_label[row + 4])
        print()


class Histogram(object):
    """
    Data structure for holding a counts of values. Creates an
    exponentially-distributed set of bins.

    See also [`Experiment.log_histogram`](#experimentlog_histogram)
    """

    def __init__(self, start=1e-12, stop=1e20, step=1.1, offset=0):
        """
        Initialize the values of bins and data structures.

        Args:
            start: float (optional), value of start range. Default 1e-12
            stop: float (optional), value of stop range. Default 1e20
            step: float (optional), value of step. Greater than one creates an
                exponentially-distributed set of bins. Default 1.1
            offset: float (optional), center of distribution. Default is zero.
        """
        self.start = start
        self.stop = stop
        self.step = step
        self.offset = offset
        self.values = tuple(self.create_bin_values())
        self.clear()

    def __sub__(self, other):
        if (
            isinstance(other, Histogram)
            and (self.start == other.start)
            and (self.stop == other.stop)
            and (self.step == other.step)
            and (self.offset == other.offset)
        ):

            histogram = Histogram(self.start, self.stop, self.step, self.offset)
            histogram.counts = [
                abs(c2 - c1) for c1, c2 in zip(self.counts, other.counts)
            ]
            return histogram
        else:
            raise TypeError("Can't subtract Histograms of different regions")

    def clear(self):
        """
        Clear the counts, initializes back to zeros.
        """
        self.counts = [0] * len(self.values)

    def add(self, values, counts=None, max_skip_count=10):
        """
        Add the value(s) to the count bins.

        Args:
            values: a list, tuple, or array of values (any shape)
                to count
            counts: a list of counts for each value in values. Triggers
                special mode for conversion from Tensorboard
                saved format.
            max_skip_count: int, (optional) maximum number of empty
                cells that triggers a binary search.

        Counting values in bins can be expensive, so this method uses
        binary_search to find the initial bin, and iterates through
        sorted values, incrementing the bin as it goes. If too many
        bins are empty (skip_count reaches max_skip_count) then it
        jumps out and does another binary_search.
        """
        try:
            values = [float(values)]
        except Exception:
            pass

        if len(values) == 0:
            return

        values = flatten(values)

        # Sort for speed of inserts
        if counts is None:
            values = sorted(values)
        # Find initial bin:
        bucket = self.get_bin_index(values[0])

        for i, value in enumerate(values):
            skip_count = 0
            while not (self.values[bucket] <= value < self.values[bucket + 1]):
                skip_count += 1
                # if too many skips
                if skip_count > max_skip_count:
                    # then let's just do a binary search
                    bucket = self.get_bin_index(value)
                    break
                else:
                    bucket += 1
            if counts is not None:
                self.counts[bucket] += int(counts[i])
            else:
                self.counts[bucket] += 1

    def counts_compressed(self):
        """
        Convert list of counts to list of [(index, count), ...].
        """
        return [
            [i, self.counts[i]] for i in range(len(self.counts)) if self.counts[i] > 0
        ]

    @classmethod
    def from_json(cls, data, verbose=True):
        """
        Given histogram JSON data, returns either a Histogram object (in
        the case of a 2D histogram) or a list of Histogram objects (in
        the case of a 3D histogram).

        Args:
            data: histogram filename or JSON data
            verbose: optional, bool, if True, display the Histogram
                after conversion

        Returns: a Histogram, or list of Histograms.

        Example:

        ```python
        In[1]: histogram = Histogram.from_json("histogram.json")

        Histogram 3D:
        Step: 0
        Histogram
        =========
        Range Start      Range End          Count           Bins
        -----------------------------------------------------------
            -0.1239        -0.1003        63.7810      [506-508]
            -0.1003        -0.0766      1006.1836      [508-511]
            -0.0766        -0.0530      1824.0884      [511-514]
            -0.0530        -0.0293     11803.4008      [514-521]
            -0.0293        -0.0056     13118.4797      [521-538]
            -0.0056         0.0180     13059.5624     [538-1023]
             0.0180         0.0417     13133.6479    [1023-1032]
             0.0417         0.0654      5865.2828    [1032-1037]
             0.0654         0.0890      1616.2949    [1037-1040]
             0.0890         0.1127       275.2784    [1040-1042]
             0.1127         0.1363         0.0000    [1042-1044]
        -----------------------------------------------------------
        Total:     61766.0000
        Out[1]:
        <comet_ml.utils.Histogram at 0x7fac8f3819b0>
        ```
        """
        if isinstance(data, str):
            filename = os.path.expanduser(data)
            if os.path.isfile(filename):
                with open(filename) as fp:
                    histogram_json = json.load(fp)
                    return Histogram.from_json(histogram_json, verbose=verbose)
            else:
                LOGGER.error("Histogram.from_json: no such file %r", filename)
                return
        elif "histograms" in data:
            retval = []
            if verbose:
                print("Histogram 3D:")
            for datum in data["histograms"]:
                histogram_json = datum["histogram"]
                if verbose:
                    print("Step:", datum["step"])
                histogram = Histogram.from_json(histogram_json, verbose=verbose)
                retval.append(histogram)
            return retval
        else:
            histogram = Histogram(
                data["start"], data["stop"], data["step"], data["offset"]
            )
            for (i, count) in data["index_values"]:
                histogram.counts[i] = count
            if verbose:
                histogram.display()
            return histogram

    def to_json(self):
        """
        Return histogram as JSON-like dict.
        """
        return {
            "version": 2,
            "index_values": self.counts_compressed(),
            "values": None,
            "offset": self.offset,
            "start": self.start,
            "stop": self.stop,
            "step": self.step,
        }

    def is_empty(self):
        # type: () -> bool
        """ Check if the Histogram is empty. Return True if empty, False otherwise
        """
        # If the Histogram contains at least one value, at least one element of
        # self.counts will be not null
        return not any(self.counts)

    def create_bin_values(self):
        """
        Create exponentially distributed bin values
        [-inf, ..., offset - start, offset, offset + start, ..., inf)
        """
        values = [-float("inf"), self.offset, float("inf")]
        value = self.start
        while value <= self.stop:
            values.insert(1, self.offset - value)
            values.insert(-1, self.offset + value)
            value *= self.step
        return values

    def get_bin_index(self, value):
        """
        Given a value, return the bin index where:

            values[index] <= value < values[index + 1]

        Implemented using binary search.
        """
        if value == float("inf"):
            return len(self.values) - 1
        return self.binary_search(value, 0, len(self.values) - 1)

    def binary_search(self, value, low, high):
        """
        Find value between low and high, via binary search.
        """
        while True:
            middle = (high + low) // 2
            if (high - low) <= 1:
                return low
            elif value < self.values[middle]:
                high = middle
            else:
                low = middle

    def get_count(self, min_value, max_value):
        """
        Get the count (can be partial of bin count) of a range.
        """
        index = self.get_bin_index(min_value)
        current_start_value = self.values[index]
        current_stop_value = self.values[index + 1]
        count = 0
        # Add total in this area:
        count += self.counts[index]
        if current_start_value != -float("inf"):
            # Remove proportion before min_value:
            current_total_range = current_stop_value - current_start_value
            percent = (min_value - current_start_value) / current_total_range
            count -= self.counts[index] * percent
        if max_value < current_stop_value:
            # stop is inside this area too, so remove after max
            if current_start_value != -float("inf"):
                percent = (current_stop_value - max_value) / current_total_range
                count -= self.counts[index] * percent
            return count
        # max_value is beyond this area, so loop until last area:
        index += 1
        while max_value > self.values[index + 1]:
            # add the whole count
            count += self.counts[index]
            index += 1
        # finally, add the proportion in last area before max_value:
        current_start_value = self.values[index]
        current_stop_value = self.values[index + 1]
        if current_stop_value != float("inf"):
            current_total_range = current_stop_value - current_start_value
            percent = (max_value - current_start_value) / current_total_range
            count += self.counts[index] * percent
        else:
            count += self.counts[index]
        return count

    def get_counts(self, min_value, max_value, span_value):
        """
        Get the counts between min_value and max_value in
        uniform span_value-sized bins.
        """
        counts = []

        if max_value == min_value:
            max_value = min_value * 1.1 + 1
            min_value = min_value / 1.1 - 1

        bucketPos = 0
        binLeft = min_value

        while binLeft < max_value:
            binRight = binLeft + span_value
            count = 0.0
            # Don't include last as bucketLeft, which is infinity:
            while bucketPos < len(self.values) - 1:
                bucketLeft = self.values[bucketPos]
                bucketRight = min(max_value, self.values[bucketPos + 1])
                intersect = min(bucketRight, binRight) - max(bucketLeft, binLeft)

                if intersect > 0:
                    if bucketLeft == -float("inf"):
                        count += self.counts[bucketPos]
                    else:
                        count += (intersect / (bucketRight - bucketLeft)) * self.counts[
                            bucketPos
                        ]

                if bucketRight > binRight:
                    break

                bucketPos += 1

            counts.append(count)
            binLeft += span_value

        return counts

    def display(
        self, start=None, stop=None, step=None, format="%14.4f", show_empty=False
    ):
        """
        Show counts between start and stop by step increments.

        Args:
            start: optional, float, start of range to display
            stop: optional, float, end of range to display
            step: optional, float, amount to increment each range
            format: str (optional), format of numbers
            show_empty: bool (optional), if True, show all
                entries in range

        Example:

        ```
        >>> from comet_ml.utils import Histogram
        >>> import random
        >>> history = Histogram()
        >>> values = [random.random() for x in range(10000)]
        >>> history.add(values)
        >>> history.display()

        Histogram
        =========
           Range Start      Range End          Count           Bins
        -----------------------------------------------------------
               -0.0000         0.1000       983.4069     [774-1041]
                0.1000         0.2000       975.5574    [1041-1049]
                0.2000         0.3000      1028.8666    [1049-1053]
                0.3000         0.4000       996.2112    [1053-1056]
                0.4000         0.5000       979.5836    [1056-1058]
                0.5000         0.6000      1010.4522    [1058-1060]
                0.6000         0.7000       986.1284    [1060-1062]
                0.7000         0.8000      1006.5811    [1062-1063]
                0.8000         0.9000      1007.7881    [1063-1064]
                0.9000         1.0000      1025.4245    [1064-1065]
        -----------------------------------------------------------
        Total:     10000.0000
        """
        collection = self.collect(start, stop, step)
        print("Histogram")
        print("=========")
        size = len(format % 0)
        sformat = "%" + str(size) + "s"
        columns = ["Range Start", "Range End", "Count", "Bins"]
        formats = [sformat % s for s in columns]
        print(*formats)
        print("-" * (size * 4 + 3))
        total = 0.0
        for row in collection:
            count = row["count"]
            total += count
            if show_empty or count > 0:
                print(
                    format % row["value_start"],
                    format % row["value_stop"],
                    format % count,
                    (
                        sformat
                        % ("[%s-%s]" % (row["bin_index_start"], row["bin_index_stop"]))
                    ),
                )
        print("-" * (size * 4 + 3))
        print(("Total: " + format) % total)

    def collect(self, start=None, stop=None, step=None):
        """
        Collect the counts for the given range and step.

        Args:
            start: optional, float, start of range to display
            stop: optional, float, end of range to display
            step: optional, float, amount to increment each range

        Returns a list of dicts containing details on each
        virtual bin.
        """
        counts_compressed = self.counts_compressed()
        if start is None:
            if len(counts_compressed) > 0:
                start = self.values[counts_compressed[0][0]]
            else:
                start = -1.0
        if stop is None:
            if len(counts_compressed) > 1:
                stop = self.values[counts_compressed[-1][0]]
            else:
                stop = 1.0
        if step is None:
            step = (stop - start) / 10.0

        counts = self.get_counts(start, stop + step, step)
        current = start
        bins = []
        next_one = current + step
        i = 0
        while next_one <= stop + (step) and i < len(counts):
            start_bin = self.get_bin_index(current)
            stop_bin = self.get_bin_index(next_one)
            bin = {
                "value_start": current,
                "value_stop": next_one,
                "bin_index_start": start_bin,
                "bin_index_stop": stop_bin,
                "count": counts[i],
            }
            bins.append(bin)
            current = next_one
            next_one = current + step
            i += 1
        return bins


def write_numpy_array_as_wav(numpy_array, sample_rate, file_object):
    # type: (Any, int, IO) -> None
    """ Convert a numpy array to a WAV file using the given sample_rate and
    write it to the file object
    """
    try:
        import numpy
        from scipy.io.wavfile import write
    except ImportError:
        LOGGER.error(
            "The Python libraries numpy, and scipy are required for this operation"
        )
        return

    array_max = numpy.max(numpy.abs(numpy_array))

    scaled = numpy.int16(numpy_array / array_max * 32767)

    write(file_object, sample_rate, scaled)


def get_file_extension(file_path):
    if file_path is None:
        return None

    ext = os.path.splitext(file_path)[1]
    if not ext:
        return None

    # Get rid of the leading "."
    return ext[1::]


def encode_metadata(metadata):
    # type: (Optional[Dict[Any, Any]]) -> Optional[Union[str, bytes]]
    if metadata is None:
        return None

    if type(metadata) is not dict:
        LOGGER.info("invalid metadata, expecting dict type", exc_info=True)
        return None

    if metadata == {}:
        return None

    try:
        json_encoded = json.dumps(metadata, separators=(",", ":"), sort_keys=True)
        encoded = json_encoded.encode("utf-8")
        return encoded
    except Exception:
        LOGGER.info("invalid metadata, expecting JSON-encodable object", exc_info=True)
        return None


def get_comet_version():
    # type: () -> str
    try:
        return get_distribution("comet_ml").version
    except DistributionNotFound:
        return "Please install comet with `pip install comet_ml`"


def get_user():
    # type: () -> str
    try:
        return getpass.getuser()
    except KeyError:
        return "unknown"


def log_asset_folder(folder, recursive=False):
    # type: (str, bool) -> Generator[Tuple[str, str], None, None]
    if recursive:
        for dirpath, _, filenames in os.walk(folder):
            for file_name in filenames:
                file_path = os.path.join(dirpath, file_name)
                yield (file_name, file_path)
    else:
        file_names = sorted(os.listdir(folder))
        for file_name in file_names:
            file_path = os.path.join(folder, file_name)
            if os.path.isfile(file_path):
                yield (file_name, file_path)


def parse_version_number(raw_version_number):
    # type: (str) -> Tuple[int, int, int]
    """
    Parse a valid "INT.INT.INT" string, or raise an
    Exception. Exceptions are handled by caller and
    mean invalid version number.
    """
    converted_version_number = [int(part) for part in raw_version_number.split(".")]

    if len(converted_version_number) != 3:
        raise ValueError(
            "Invalid version number %r, parsed as %r",
            raw_version_number,
            converted_version_number,
        )

    # Make mypy happy
    version_number = (
        converted_version_number[0],
        converted_version_number[1],
        converted_version_number[2],
    )
    return version_number


def format_version_number(version_number):
    # type: (Tuple[int, int, int]) -> str
    return ".".join(map(str, version_number))


def valid_ui_tabs(tab=None, preferred=False):
    """
    List of valid UI tabs in browser.
    """
    preferred_names = [
        "assets",
        "audio",
        "charts",
        "code",
        "confusion-matrices",
        "histograms",
        "images",
        "installed-packages",
        "metrics",
        "notes",
        "parameters",
        "system-metrics",
        "text",
    ]
    mappings = {
        "asset": "assetStorage",
        "assetStorage": "assetStorage",
        "assets": "assetStorage",
        "audio": "audio",
        "chart": "chart",
        "charts": "chart",
        "code": "code",
        "confusion-matrices": "confusionMatrix",
        "confusion-matrix": "confusionMatrix",
        "confusionMatrix": "confusionMatrix",
        "graphics": "images",
        "histograms": "histograms",
        "images": "images",
        "installed-packages": "installedPackages",
        "installedPackages": "installedPackages",
        "metrics": "metrics",
        "notes": "notes",
        "parameters": "params",
        "params": "params",
        "system-metrics": "systemMetrics",
        "systemMetrics": "systemMetrics",
        "text": "text",
    }
    if preferred:
        return preferred_names
    elif tab is None:
        return mappings.keys()
    elif tab in mappings:
        return mappings[tab]
    else:
        raise ValueError("invalid tab name; tab should be in %r" % preferred_names)


def convert_to_matrix(matrix, dtype=None):
    """
    Convert an unknown item into a list of lists of scalars
    and ensure type is dtype (if given).
    """
    # First, convert it to numpy if possible:
    if hasattr(matrix, "numpy"):  # pytorch tensor
        matrix = matrix.numpy()
    elif hasattr(matrix, "eval"):  # tensorflow tensor
        matrix = matrix.eval()

    # Next, convert to lists of scalars:
    if hasattr(matrix, "tolist"):  # numpy array
        if len(matrix.shape) != 2:
            raise ValueError("matrix should be two dimensional")
        return matrix.tolist()
    else:
        # assume it is something we can iterate over:
        return [convert_to_list(row, dtype=dtype) for row in matrix]


def shape(data):
    """
    Given a nested list or a numpy array,
    return the shape.
    """
    if hasattr(data, "shape"):
        return list(data.shape)
    else:
        try:
            length = len(data)
            return [length] + shape(data[0])
        except TypeError:
            return []


def flatten(values):
    """
    Given a nested list or a numpy array,
    return the data flattened.
    """
    # Numpy arrays have an optimized method of flattening:
    if hasattr(values, "flatten"):
        values = values.flatten()
    else:
        # Otherwise, we try to recursively flatten via functools.reduce:
        try:
            values = functools.reduce(
                operator.iconcat, [flatten(value) for value in values], []
            )
        except TypeError:
            # Otherwise, assume that it is already flat:
            pass
    return values


def convert_to_list(items, dtype=None):
    """
    Take an unknown item and convert to a list of scalars
    and ensure type is dtype, if given.
    """
    # First, convert it to numpy if possible:
    if hasattr(items, "numpy"):  # pytorch tensor
        items = items.numpy()
    elif hasattr(items, "eval"):  # tensorflow tensor
        items = items.eval()

    # Next, handle numpy array:
    if hasattr(items, "tolist"):
        if len(items.shape) != 1:
            raise ValueError("list should be one dimensional")
        return items.tolist()
    else:
        # assume it is something with numbers in it:
        return [convert_to_scalar(item, dtype=dtype) for item in items]


def convert_to_string(user_data):
    # type: (Any) -> str
    """
    Given an object, return it as a string.
    """
    if hasattr(user_data, "numpy"):
        user_data = user_data.numpy()

    if isinstance(user_data, bytes) and not isinstance(user_data, str):
        user_data = user_data.decode("utf-8")

    return str(user_data)


def convert_to_scalar(user_data, dtype=None):
    # type: (Any, Optional[Type]) -> Any
    """
    Try to ensure that the given user_data is converted back to a
    Python scalar, and of proper type (if given).
    """

    # First try to convert tensorflow tensor to numpy objects
    try:
        if hasattr(user_data, "numpy"):
            user_data = user_data.numpy()
    except Exception:
        LOGGER.warning(
            "Failed to convert tensorflow tensor %r to numpy object",
            user_data,
            exc_info=True,
        )

    # Then try to convert numpy object to a Python scalar
    try:
        if HAS_NUMPY and isinstance(user_data, numpy.number):
            user_data = user_data.item()
    except Exception:
        LOGGER.warning(
            "Failed to convert numpy object %r to Python scalar",
            user_data,
            exc_info=True,
        )

    if dtype is not None and not isinstance(user_data, dtype):
        raise TypeError("%r is not of type %r" % (user_data, dtype))

    return user_data


def makedirs(name, exist_ok=False):
    """
    Replacement for Python2's version lacking exist_ok
    """
    if not os.path.exists(name) or not exist_ok:
        os.makedirs(name)


def clean_and_check_root_relative_path(root, relative_path):
    # type: (str, str) -> str
    """
    Given a root and a relative path, resolve the relative path to get an
    absolute path and make sure the resolved path is a child to root. Cases
    where it could not be the case would be if the `relative_path` contains `..`
    or if one part of the relative path is a symlink going above the root.

    Return the absolute resolved path and raises a ValueError if the root path
    is not absolute or if the resolved relative path goes above the root.
    """
    if not os.path.isabs(root):
        raise ValueError("Root parameter %r should an absolute path" % root)

    if not root.endswith(os.sep):
        root = root + os.sep

    joined_path = os.path.join(root, relative_path)
    resolved_path = os.path.realpath(joined_path)

    if not resolved_path.startswith(root):
        raise ValueError("Final path %r is outside of %r" % (resolved_path, root))

    return resolved_path


def check_if_path_relative_to_root(root, absolute_path):
    # type: (str, str) -> bool
    if not os.path.isabs(root):
        raise ValueError("Root parameter %r should an absolute path" % root)

    root_full_path = os.path.realpath(root) + os.sep
    full_path = os.path.realpath(absolute_path)

    return full_path.startswith(root_full_path)


def verify_data_structure(datatype, data):
    # Raise an error if anything wrong
    if datatype == "curve":
        if (
            ("x" not in data)
            or ("y" not in data)
            or ("name" not in data)
            or (not isinstance(data["name"], str))
            or (len(data["x"]) != len(data["y"]))
        ):
            raise ValueError(
                "'curve' requires lists 'x' and 'y' of equal lengths, and string 'name'"
            )
    else:
        raise ValueError("invalid datatype %r: datatype must be 'curve'" % datatype)


def proper_registry_model_name(name):
    """
    A proper registry model name is:
        * lowercase
        * replaces all non-alphanumeric with dashes
        * removes leading and trailing dashes
        * limited to 1 dash in a row
    """
    name = "".join([(char if char.isalnum() else "-") for char in name])
    while name.startswith("-"):
        name = name[1:]
    while name.endswith("-"):
        name = name[:-1]
    name = name.lower()
    while "--" in name:
        name = name.replace("--", "-")
    return name


def safe_filename(filename):
    """
    Given a value, turn it into a valid filename.

    1. Remove the spaces
    2. Replace anything not alpha, '-', '_', or '.' with '_'
    3. Remove duplicate '_'
    """
    string = str(filename).strip().replace(" ", "_")
    string = re.sub(r"(?u)[^-\w.]", "_", string)
    return re.sub(r"_+", "_", string)
