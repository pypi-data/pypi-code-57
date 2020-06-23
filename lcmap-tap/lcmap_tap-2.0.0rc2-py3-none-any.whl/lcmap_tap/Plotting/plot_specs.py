"""Prepare data for plotting"""

import sys
import datetime as dt
from collections import OrderedDict
from typing import Union
import numpy as np
from lcmap_tap.logger import exc_handler, log
from lcmap_tap.Plotting import plot_functions


sys.excepthook = exc_handler

bands = ("blue", "green", "red", "nir", "swir1", "swir2", "thermal")

index_functions = {
    "ndvi": {"func": plot_functions.ndvi, "bands": ("reds", "nirs"), "inds": (2, 3)},
    "msavi": {"func": plot_functions.msavi, "bands": ("reds", "nirs"), "inds": (2, 3)},
    "evi": {
        "func": plot_functions.evi,
        "bands": ("blues", "reds", "nirs"),
        "inds": (0, 2, 3),
    },
    "savi": {"func": plot_functions.savi, "bands": ("reds", "nirs"), "inds": (2, 3)},
    "ndmi": {"func": plot_functions.ndmi, "bands": ("nirs", "swir1s"), "inds": (3, 4)},
    "nbr": {"func": plot_functions.nbr, "bands": ("nirs", "swir2s"), "inds": (3, 5)},
    "nbr2": {
        "func": plot_functions.nbr2,
        "bands": ("swir1s", "swir2s"),
        "inds": (4, 5),
    },
}


def make_arrays(in_dict: dict) -> dict:
    """
    Convert a dict of lists into arrays
    Args:
        in_dict: a dictionary of lists

    Returns: a dictionary of numpy arrays
    """
    for key in in_dict.keys():
        if isinstance(in_dict[key], list):
            in_dict[key] = np.array(in_dict[key])

    return in_dict


def mask_daterange(dates: np.array, start: dt.date, stop: dt.date) -> np.array:
    """
    Create a mask for values outside of the global BEGIN_DATE and END_DATE

    Args:
        dates: List or array of dates to check against
        start: Begin date stored as a datetime.date object
        stop: End date stored as a datetime.date object

    Returns:
        Array containing the locations of the truth condition
    """
    return np.logical_and(dates >= start.toordinal(), dates < stop.toordinal())


def get_modeled_index(ard, results, predicted_values):
    """
    Calculate the model-predicted index curves
    Returns:
    """
    indices = ("ndvi", "msavi", "evi", "savi", "ndmi", "nbr", "nbr2")
    modeled = dict()

    for key in ard.keys():
        if key in indices:
            new_key = f"{key}-modeled"

            modeled[new_key] = list()

            call = index_functions[key]["func"]

            inds = index_functions[key]["inds"]

            try:
                for m in range(len(results)):
                    args = tuple(
                        [predicted_values[m * len(bands) + ind] for ind in inds]
                    )

                    modeled[new_key].append(call(*args))

            except (AttributeError, TypeError) as e:
                log.error("Exception: %s", e, exc_info=True)

                modeled[new_key].append([])

    return modeled


def get_predicts(num: Union[int, list], predicted_values: list, results: dict) -> list:
    """
    Return the model prediction values in the time series for a particular band or bands

    Args:
        num:

    Returns:
        A list of segment models

    """
    # Check for type int, create list if true
    if isinstance(num, int):
        num = [num]

    try:
        _predicts = [
            predicted_values[m * len(bands) + n]
            for n in num
            for m in range(len(results))
        ]

    except (IndexError, TypeError) as e:
        log.error("Exception: %s", e, exc_info=True)

        _predicts = []

    return _predicts


def get_lookups(ard, results, predicted_values):
    """
    Calculate indices from observed values

    Calculate indices from the results' change models
    The change models are stored by order of model, then band number.
    For example, the band values for the first change model
    are represented by indices 0-5,
    the second model by indices 6-11, and so on.
    """
    index_modeled = get_modeled_index(
        ard=ard, results=results, predicted_values=predicted_values
    )

    index_lookup = OrderedDict(
        [
            ("NDVI", ("ndvi", "ndvi-modeled")),
            ("MSAVI", ("msavi", "msavi-modeled")),
            ("EVI", ("evi", "evi-modeled")),
            ("SAVI", ("savi", "savi-modeled")),
            ("NDMI", ("ndmi", "ndmi-modeled")),
            ("NBR", ("nbr", "nbr-modeled")),
            ("NBR-2", ("nbr2", "nbr2-modeled")),
        ]
    )

    index_lookup = [
        (key, (ard[index_lookup[key][0]], index_modeled[index_lookup[key][1]]))
        for key in index_lookup.keys()
        if index_lookup[key][0] in ard.keys()
    ]

    index_lookup = OrderedDict(index_lookup)

    lookup = OrderedDict(
        [
            ("Blue", ("blues", 0)),
            ("Green", ("greens", 1)),
            ("Red", ("reds", 2)),
            ("NIR", ("nirs", 3)),
            ("SWIR-1", ("swir1s", 4)),
            ("SWIR-2", ("swir2s", 5)),
            ("Thermal", ("thermals", 6)),
        ]
    )

    band_lookup = [
        (
            key,
            (
                ard[lookup[key][0]],
                get_predicts(
                    num=lookup[key][1],
                    predicted_values=predicted_values,
                    results=results,
                ),
            ),
        )
        for key in lookup.keys()
        if lookup[key][0] in ard.keys()
    ]

    # Example of how the band_lookup is structured:
    # band_lookup = [("Blue", (ard['blues'], get_predicts(0))),
    #                     ("Green", (ard['greens'], get_predicts(1))),
    #                     ("Red", (ard['reds'], get_predicts(2))),
    #                     ("NIR", (ard['nirs'], get_predicts(3))),
    #                     ("SWIR-1", (ard['swir1s'], get_predicts(4))),
    #                     ("SWIR-2", (ard['swir2s'], get_predicts(5))),
    #                     ("Thermal", (ard['thermals'], get_predicts(6)))]

    band_lookup = OrderedDict(band_lookup)

    # Combine these two dictionaries
    all_lookup = plot_functions.merge_dicts(band_lookup, index_lookup)

    return index_lookup, band_lookup, all_lookup


def predicts(days, coef, intercept):
    """
    Calculate change segment curves

    Args:
        days:
        coef:
        intercept:

    Returns:

    """
    return (
        intercept
        + coef[0] * days
        + coef[1] * np.cos(days * 1 * 2 * np.pi / 365.25)
        + coef[2] * np.sin(days * 1 * 2 * np.pi / 365.25)
        + coef[3] * np.cos(days * 2 * 2 * np.pi / 365.25)
        + coef[4] * np.sin(days * 2 * 2 * np.pi / 365.25)
        + coef[5] * np.cos(days * 3 * 2 * np.pi / 365.25)
        + coef[6] * np.sin(days * 3 * 2 * np.pi / 365.25)
    )


def date_str_to_date(date_string):
    """
    Convert a date string to a datetime object.
    Args: a string formatted date in YYYY-MM-DD
    Returns: a datetime object's date
    """
    return dt.datetime.strptime(date_string, "%Y-%m-%d").date()


def get_modelled_specs(results):
    """
    Extract values from a ccd segment data structure and return the list results.
    Args: results - a ccd segment data structure
    Returns: multiple lists of the extracted values.
        predicted_values
        prediction_dates
        break_dates
        start_dates
        end_dates
    """
    band_info = {
        "blpred": [],
        "grpred": [],
        "repred": [],
        "nipred": [],
        "s1pred": [],
        "s2pred": [],
        "thpred": [],
    }

    predicted_values = []
    prediction_dates = []
    break_dates = []
    start_dates = []
    end_dates = []
    for result in results:
        days = np.arange(
            dt.datetime.toordinal(date_str_to_date(result["sday"])),
            dt.datetime.toordinal(date_str_to_date(result["eday"])) + 1,
        )

        break_dates.append(result["bday"])
        start_dates.append(result["sday"])
        end_dates.append(result["eday"])

        for b in band_info:
            # use the first two letters from the keys of band_info to
            # lookup the band + coef and int keys from the segment result data
            band_info[b] = predicts(
                days, result[(b[:2] + "coef")], result[(b[:2] + "int")]
            )

            prediction_dates.append(days)
            predicted_values.append(band_info[b])

    return predicted_values, prediction_dates, break_dates, start_dates, end_dates


def rescale_thermal(ard, fill_mask):
    """
    Fix the scaling of the Brightness Temperature, if it was selected for plotting
    """
    temp_thermal = np.copy(ard["thermals"])
    temp_thermal[fill_mask] = temp_thermal[fill_mask] * 10 - 27315

    return np.copy(temp_thermal)


def index_to_observations(ard, items):
    """
    Add index calculated observations to the timeseries pixel rod

    Returns:
    """
    indices = ["NDVI", "MSAVI", "EVI", "SAVI", "NDMI", "NBR", "NBR-2"]

    selected_indices = [i for i in indices if i in items or "All Indices" in items]

    for i in selected_indices:
        key = i.lower().replace("-", "")

        call = index_functions[key]["func"]

        args = tuple([ard[band] for band in index_functions[key]["bands"]])

        ard[key] = call(*args)

    return ard


class PlotSpecs:
    """
    Generate and retain the data required for plotting
    """

    def __init__(
        self,
        ard: dict,
        pixel_change,
        segs,
        items: list,
        begin: dt.date = dt.date(year=1982, month=1, day=1),
        end: dt.date = dt.date(year=2017, month=12, day=31),
    ):
        """
        Args:
            ard: The ARD observations for a given point (ARDData.pixel_ard)
            pixel_change: PyCCD pixel results for a given point
            segs: Classification segment results
            begin: Beginning day of PyCCD
            end: Ending day of PyCCD
        """
        self.begin = begin
        self.end = end
        self.items = items

        self.ard = make_arrays(ard)
        self.dates = self.ard["dates"]

        self.ccd_mask = np.array(pixel_change, dtype=np.bool)
        self.segment_classes = segs

        self.date_mask = mask_daterange(dates=self.dates, start=begin, stop=end)

        self.dates_in = self.ard["dates"][self.date_mask]
        self.dates_out = self.ard["dates"][~self.date_mask]

        self.qa_mask = np.isin(self.ard["qas"], [66, 68, 322, 324])

        self.fill_mask = np.isin(
            self.ard["qas"], [n for n in np.unique(self.ard["qas"]) if n != 1]
        )

        self.fill_in = self.fill_mask[self.date_mask]
        self.fill_out = self.fill_mask[~self.date_mask]

        # Check for presence of thermals, rescale if present
        if "thermals" in self.ard.keys():
            self.ard["thermals"] = rescale_thermal(
                ard=self.ard, fill_mask=self.fill_mask
            )

        self.ard = index_to_observations(ard=self.ard, items=self.items)

        if self.segment_classes is not None:
            (
                self.predicted_values,
                self.prediction_dates,
                self.break_dates,
                self.start_dates,
                self.end_dates,
            ) = get_modelled_specs(self.segment_classes)

        else:
            self.predicted_values = []
            self.prediction_dates = []
            self.break_dates = []
            self.start_dates = []
            self.end_dates = []

        self.index_lookup, self.band_lookup, self.all_lookup = get_lookups(
            ard=self.ard,
            results=self.segment_classes,
            predicted_values=self.predicted_values,
        )
