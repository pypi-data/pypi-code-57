#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 08:58:19 2018

@author: rensmasselink
"""
import logging

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.vrt import WarpedVRT
from sklearn.cluster import KMeans

from classifier.dataprep import check_training_data_nodata
from classifier.utils.general import get_available_model_args, progress
UNSUPERVISED_LOGGER = logging.getLogger(__name__)

def make_input_array(rasters, windows, config_dict):
    """ Create an input array for unsupervised classification

    Function for creating the input array for the training of the
    unsupervised models. A train_size relative to the entire dataset can be
    set to reduce the amount of memory needed

       Args:
           rasters (list)      input rasters
           windows (list)      A list of rasterio Windows to use
           config_dict (dict)   The parameters for making an input array

        Returns:
            A data array to use in model training"""
    # Create a 2d array which can be passed into the classifier
    bandcount = []
    for raster in rasters:
        with rasterio.open(raster, 'r') as src_r:
            bandcount.append(src_r.count)
    b_count = np.sum(bandcount)
    # Random index for choosing the windows to use
    subset_windows = np.random.choice(
        np.array(windows)[:, 1],
        size=int(len(windows) * config_dict['us_trainfraction']),
        replace=False
    )

    assert len(subset_windows) > 0, ("Not enough subset data. Please increase"
                                     " -us_train_size parameter"
                                    )

    UNSUPERVISED_LOGGER.info(
        "\nUsing %i windows for training",
        len(subset_windows)
    )

    windows_length = np.sum([win.height*win.width for win in subset_windows])
    data_array = np.zeros(shape=[int(windows_length), int(b_count)])

    # iterate through rasters and fill array
    data_array = raster_iterator(subset_windows, rasters, data_array)

    #Check for missing values and impute if necessary
    data_array = check_training_data_nodata(data_array, config_dict)

    return data_array[~np.isnan(data_array).any(axis=1)]


def load_raster_data(vrt, win, data_array, col_counter, row_counter):
    """
    Load all the raster data into an array
    Args:
        vrt: The VRT
        win: A rasterio window
        data_array: The array in which to put the data
        col_counter: A counter for columns (for slicing array)
        row_counter: A counter for rows (for slicing array)

    Returns:
        data_array: filled data array for windows
        col_counter: Updated col_counter
        raster_counter: counter of number of bands in vrt

    """
    nan_value = vrt.nodatavals[0]
    raster_data = vrt.read(window=win)
    # Set the nan values to nan
    raster_data[raster_data == nan_value] = np.ma.masked
    # Fill the array with this data
    raster_counter = raster_data.shape[1] * \
                     raster_data.shape[2]
    nr_bands = vrt.count
    data_array[row_counter:row_counter + raster_counter,
               col_counter:col_counter + nr_bands] = \
               raster_data.reshape(raster_data.shape[0],
                                   raster_counter).T
    col_counter += nr_bands
    return data_array, col_counter, raster_counter


def raster_iterator(subset_windows, rasters, data_array):
    """
    Iterate though the rasters and call the load_raster_data function
    Args:
        subset_windows: the windows list to use
        rasters: list of rasters
        data_array: the array to fill

    Returns:
        THe filled data_array

    """
    with rasterio.open(rasters[0], 'r') as template:
        row_counter = 0
        nr_windows = len(subset_windows)
        for i, win in enumerate(subset_windows):
            progress(i, nr_windows)
            col_counter = 0
            # Create a vrt with the window and add the data to the array
            for raster in rasters:
                with rasterio.open(raster, 'r') as src:
                    with WarpedVRT(src,
                                   resampling=Resampling.bilinear,
                                   meta=template.meta,
                                   width=template.meta['width'],
                                   height=template.meta['height'],
                                   crs=template.crs,
                                   transform=template.transform
                                  ) as vrt:
                        data_array, col_counter, raster_counter = \
                            load_raster_data(vrt, win, data_array,
                                             col_counter, row_counter)
            row_counter += raster_counter
    return data_array


def train_kmeans(train_array, n_classes, algorithm_args):
    """Train the kmeans model

        Args:
            train_array (array)   A data array with columns (bands) and rows (
            pixels)
            n_classes (int)       The number of classes to distinguish
            algorithm_args (dict) Arguments for algorithm

        Returns:
            A dictionary conaining the algorithm name, the trained model and an
            empty label key to match the dicts from the supervised
            classifications
    """
    UNSUPERVISED_LOGGER.info("Now Training Model. This might take some time...")
    model_algorithms_args = get_available_model_args(algorithm_args, KMeans)
    kmeans = KMeans(n_clusters=n_classes, **model_algorithms_args)
    kmeans.fit(train_array)
    return {'app_algorithm': 'us_kmeans', 'model': kmeans, 'labels': None}
