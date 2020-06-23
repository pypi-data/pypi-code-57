"""
Unit tests for lcmap_tap/Plotting/make_plots.py
"""

import datetime as dt
from collections import OrderedDict
import pytest
import numpy as np
import matplotlib
from lcmap_tap.Plotting import make_plots
from lcmap_tap.Plotting import COLORS, LEG_DEFAULTS

ard_pixel_dates_array = {
    "greens": np.array([5610, -9999, -9999, 6056, 2222, -9999], dtype=np.int16),
    "dates": np.array([736691, 736689, 736683]),
    "qas": np.array([992, 1, 1, 224, 224, 1], dtype=np.uint16),
}

predict_data_sample = [
    {
        "primary-landcover": 3,
        "secondary-landcover": 1,
        "primary-confidence": 82,
        "secondary-confidence": 16,
        "annual-change": 3,
        "sday": "1985-07-01",
        "eday": "1986-07-01",
    },
    {
        "primary-landcover": 3,
        "secondary-landcover": 1,
        "primary-confidence": 82,
        "secondary-confidence": 16,
        "annual-change": 3,
        "sday": "1986-07-01",
        "eday": "1987-07-01",
    },
]

index_lookup = OrderedDict(
    [
        (
            "NDVI",
            (
                np.array([0.03113959, 0.0, 0.0, 0.0112811, 0.10661062, 0.0]),
                [
                    np.array(
                        [
                            0.40755407,
                            0.40480608,
                            0.4019406,
                            0.21234589,
                            0.21504904,
                            0.21772809,
                        ]
                    )
                ],
            ),
        )
    ]
)
band_lookup = OrderedDict(
    [
        (
            "Green",
            (
                np.array([5610, -9999, -9999, 6056, 2222, -9999]),
                [
                    np.array(
                        [
                            1304.06489439,
                            1304.45904127,
                            1304.90873875,
                            826.49541708,
                            819.01962881,
                            811.60571047,
                        ]
                    )
                ],
            ),
        ),
        (
            "Red",
            (
                np.array([5896, -9999, -9999, 6398, 2338, -9999]),
                [
                    np.array(
                        [
                            1337.05348557,
                            1340.3547586,
                            1343.80650288,
                            890.24231824,
                            879.87031453,
                            869.67637912,
                        ]
                    )
                ],
            ),
        ),
        (
            "NIR",
            (
                np.array([6275, -9999, -9999, 6544, 2896, -9999]),
                [
                    np.array(
                        [
                            3176.61910763,
                            3163.57145669,
                            3150.08325369,
                            1370.24819962,
                            1361.97754611,
                            1353.78675127,
                        ]
                    )
                ],
            ),
        ),
    ]
)
all_lookup = OrderedDict(
    [
        (
            "Green",
            (
                np.array([5610, -9999, -9999, 6056, 2222, -9999]),
                [
                    np.array(
                        [
                            1304.06489439,
                            1304.45904127,
                            1304.90873875,
                            826.49541708,
                            819.01962881,
                            811.60571047,
                        ]
                    )
                ],
            ),
        ),
        (
            "Red",
            (
                np.array([5896, -9999, -9999, 6398, 2338, -9999]),
                [
                    np.array(
                        [
                            1337.05348557,
                            1340.3547586,
                            1343.80650288,
                            890.24231824,
                            879.87031453,
                            869.67637912,
                        ]
                    )
                ],
            ),
        ),
        (
            "NIR",
            (
                np.array([6275, -9999, -9999, 6544, 2896, -9999]),
                [
                    np.array(
                        [
                            3176.61910763,
                            3163.57145669,
                            3150.08325369,
                            1370.24819962,
                            1361.97754611,
                            1353.78675127,
                        ]
                    )
                ],
            ),
        ),
        (
            "NDVI",
            (
                np.array([0.03113959, 0.0, 0.0, 0.0112811, 0.10661062, 0.0]),
                [
                    np.array(
                        [
                            0.40755407,
                            0.40480608,
                            0.4019406,
                            0.21234589,
                            0.21504904,
                            0.21772809,
                        ]
                    )
                ],
            ),
        ),
    ]
)


@pytest.mark.parametrize(
    "test_data, result", [(ard_pixel_dates_array["dates"], True,),],
)
def test_ard_datetimes(test_data, result):
    """
    Validate a datetime object list from an ARD timeseries.
    """
    ard_datetime = make_plots.ard_datetimes(test_data)
    print(f"ARD Datetimes are: {ard_datetime}")
    assert isinstance(ard_datetime[0], dt.datetime) == result
    assert len(ard_datetime) == 2


@pytest.mark.parametrize(
    "test_data, key, result",
    [(predict_data_sample, "Grass/Shrub", [724823, 725188],),],
)
def test_get_class_results(test_data, key, result):
    """
    Test extracting classification results from a data object.
    """
    class_results = make_plots.get_class_results(test_data)
    print(f"class_results are: {class_results}")
    assert class_results.get(key).get("starts") == result


@pytest.mark.parametrize(
    "test_all_lookup, test_bands, test_index, selected_indices, result",
    [
        (all_lookup, band_lookup, index_lookup, ["Green"], 1,),
        (all_lookup, band_lookup, index_lookup, [], 3,),
    ],
)
def test_get_plot_items(
    test_all_lookup, test_bands, test_index, selected_indices, result
):
    """
    Test extracting bands/indices selected to plot.
    """
    plot_items = make_plots.get_plot_items(
        test_all_lookup, test_bands, test_index, selected_indices
    )
    print(f"plot_items are: {plot_items}")
    assert len(plot_items) == result


@pytest.mark.parametrize(
    "test_color_key, result", [("Grass/Shrub", 0.9019607843137255),],
)
def test_get_legend_handle(test_color_key, result):
    """
    Validate a matplotlib Line2D object is created.
    """
    my_line = make_plots.get_legend_handle(color=COLORS[test_color_key])
    print(f"my_line is: {my_line.get_color()}")
    assert my_line.get_color()[0] == result


@pytest.mark.parametrize(
    "test_config, results", [(LEG_DEFAULTS, True),],
)
def test_create_legend_handle_list(test_config, results):
    """
    Verify custom plotting legend handle list is created.
    """
    handles = make_plots.create_legend_handle_list(test_config)
    print(f"handles are: {handles}")
    assert isinstance(handles[0], matplotlib.lines.Line2D) == results


@pytest.mark.parametrize(
    "index_test, result", [(0, "Selected"),],
)
def test_get_labels(index_test, result):
    """
    Verify label list is created successfully.
    """
    label_list = make_plots.get_labels()
    print(f"label_list is: {label_list}")
    assert label_list[index_test] == result


# TODO
# @pytest.mark.parametrize(
#    "key_test, result", [("", ""),],
# )
# def test_leg_lines_to_plots():
#    """
#    Validate the mapping of legend lines to plot artists is created successfully.
#    """
