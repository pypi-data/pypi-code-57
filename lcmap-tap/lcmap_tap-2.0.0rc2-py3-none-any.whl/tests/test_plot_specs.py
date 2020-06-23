"""
Unit tests for lcmap_tap/Plotting/plot_specs.py
"""
import datetime as dt
from contextlib import ExitStack as does_not_raise
import pytest
import numpy as np
from lcmap_tap.Plotting import plot_specs

ard_pixel_dates_list = {
    "greens": np.array([5610, -9999, -9999, 6056, 2222, -9999], dtype=np.int16),
    "dates": [736691, 736689, 736683],
    "qas": np.array([992, 1, 1, 224, 224, 1], dtype=np.uint16),
}
ard_pixel_dates_array = {
    "greens": np.array([5610, -9999, -9999, 6056, 2222, -9999], dtype=np.int16),
    "dates": np.array([736691, 736689, 736683]),
    "qas": np.array([992, 1, 1, 224, 224, 1], dtype=np.uint16),
}
ard_pixel_ndvi = {
    "nirs": np.array([6275, -9999, -9999, 6544, 2896, -9999]),
    "dates": np.array([736691, 736689, 736683, 723874, 723867, 723865]),
    "reds": np.array([5896, -9999, -9999, 6398, 2338, -9999]),
    "qas": np.array([992, 1, 1, 224, 224, 1]),
    "greens": np.array([5610, -9999, -9999, 6056, 2222, -9999]),
    "ndvi": np.array([0.03113959, 0.0, 0.0, 0.0112811, 0.10661062, 0.0]),
}
ard_pixel_thermal = {
    "qas": np.array([992, 1, 1, 224, 224, 1], dtype=np.uint16),
    "dates": np.array([736691, 736689, 736683, 723874, 723867, 723865]),
    "thermals": np.array([2525, -9999, -9999, 2594, 2581, -9999], dtype=np.int16),
}
ard_pixel_thermal_fill_mask = np.array([True, False, False, True, True, False])

segment_test_data = [
    {
        "thint": 396304.2,
        "bday": "1995-04-27",
        "grmag": 608.2668,
        "blint": 300536.9,
        "grrmse": 147.79137,
        "s2mag": 713.6907,
        "sday": "1990-08-12",
        "grint": 385939.5,
        "grcoef": [
            -0.52900785,
            226.18793,
            122.43392,
            88.794075,
            24.081324,
            62.27461,
            13.996332,
        ],
        "px": -405615,
        "rermse": 181.07776,
        "s1mag": 674.16016,
        "eday": "1995-03-10",
        "nimag": 600.56604,
        "thcoef": [
            -0.54281944,
            -1199.6116,
            -305.9252,
            121.29901,
            -173.82944,
            342.10953,
            -29.672987,
        ],
        "blcoef": [
            -0.41199747,
            212.46509,
            109.20524,
            24.96621,
            27.207317,
            26.273006,
            28.805037,
        ],
        "s1rmse": 234.10927,
        "nicoef": [
            -0.52706635,
            -392.88232,
            -26.583075,
            379.28754,
            57.393475,
            -16.017681,
            -1.573436,
        ],
        "s2int": 630396.6,
        "s2rmse": 229.22151,
        "thmag": 281.01892,
        "reint": 467632.62,
        "cx": -408585,
        "cy": 2327805,
        "s1int": 578879.3,
        "blrmse": 141.1045,
        "remag": 642.11395,
        "thrmse": 413.42587,
        "s2coef": [
            -0.86417097,
            362.3252,
            52.97076,
            -18.48807,
            -255.3553,
            206.33894,
            -96.69536,
        ],
        "chprob": 1.0,
        "curqa": 8,
        "blmag": 402.47223,
        "niint": 385539.47,
        "s1coef": [
            -0.7922002,
            349.65274,
            -7.1736274,
            71.86158,
            -313.68414,
            249.3641,
            -133.59406,
        ],
        "py": 2327805,
        "nirmse": 228.45187,
        "recoef": [
            -0.64112884,
            386.83954,
            126.86758,
            84.29895,
            -5.845223,
            109.03605,
            13.639065,
        ],
    }
]
pred_value_test_data = [
    np.array(
        [
            906.17682284,
            906.6236723,
            907.18522799,
            685.21700633,
            680.15644824,
            675.03856289,
        ]
    ),
    np.array(
        [
            1304.06489439,
            1304.45904127,
            1304.90873875,
            826.49541708,
            819.01962881,
            811.60571047,
        ]
    ),
    np.array(
        [
            1337.05348557,
            1340.3547586,
            1343.80650288,
            890.24231824,
            879.87031453,
            869.67637912,
        ]
    ),
    np.array(
        [
            3176.61910763,
            3163.57145669,
            3150.08325369,
            1370.24819962,
            1361.97754611,
            1353.78675127,
        ]
    ),
    np.array(
        [
            2757.23420306,
            2764.64630402,
            2772.15997936,
            1483.38464925,
            1478.24079525,
            1474.16734533,
        ]
    ),
    np.array(
        [
            1899.39106509,
            1907.0375723,
            1914.8825172,
            765.10044906,
            762.23613172,
            760.18865792,
        ]
    ),
    np.array(
        [
            2948.49952691,
            2954.2125579,
            2959.72480193,
            -570.74731926,
            -567.70126116,
            -563.27049784,
        ]
    ),
]


@pytest.mark.parametrize(
    "test_data, result", [(ard_pixel_dates_list, True,), (ard_pixel_dates_array, True)],
)
def test_make_arrays(test_data, result):
    """
    Validate a list inside a dictionary is converted to a numpy array.
    """
    assert isinstance(plot_specs.make_arrays(test_data)["dates"], np.ndarray) == result


@pytest.mark.parametrize(
    "test_data, date_start, date_end, result",
    [
        (
            ard_pixel_dates_array["dates"],
            dt.date(year=1982, month=1, day=1),
            dt.date(year=2017, month=12, day=31),
            np.array([True, True, True]),
        ),
        (
            ard_pixel_dates_array["dates"],
            dt.date(year=2017, month=12, day=21),
            dt.date(year=2017, month=12, day=31),
            np.array([True, True, False]),
        ),
    ],
)
def test_mask_daterange(test_data, date_start, date_end, result):
    """
    Validate mask values for dates outside of start/end range.
    """
    assert np.array_equal(
        plot_specs.mask_daterange(test_data, date_start, date_end), result
    )


@pytest.mark.parametrize(
    "date_string, result",
    [("2017-09-07", does_not_raise()), (20170907, pytest.raises(TypeError)),],
)
def test_date_str_to_date(date_string, result):
    """
    Test converting a date string to a date object.
    """
    with result:
        assert isinstance(plot_specs.date_str_to_date(date_string), dt.date)


@pytest.mark.parametrize(
    "test_data, result_pred_values, result_pred_dates, result_bday, result_sday, result_eday",
    [
        (
            segment_test_data,
            906.17682284,
            726691,
            ["1995-04-27"],
            ["1990-08-12"],
            ["1995-03-10"],
        ),
    ],
)
def test_get_modelled_specs(
    test_data,
    result_pred_values,
    result_pred_dates,
    result_bday,
    result_sday,
    result_eday,
):
    """
    Verify segment data is extracted into different lists correctly.
    """
    (
        predicted_values,
        prediction_dates,
        break_dates,
        start_dates,
        end_dates,
    ) = plot_specs.get_modelled_specs(results=test_data)

    print(f"-> Predicted values: {predicted_values}")
    assert abs(predicted_values[0][0] - result_pred_values) < 0.001
    print(f"-> Prediction dates: {prediction_dates}")
    assert prediction_dates[0][0] == result_pred_dates
    print(f"-> break dates: {break_dates}")
    assert break_dates == result_bday
    print(f"-> start dates: {start_dates}")
    assert start_dates == result_sday
    print(f"-> end dates: {end_dates}")
    assert end_dates == result_eday


@pytest.mark.parametrize(
    "test_data, test_result",
    [
        (ard_pixel_dates_array, pytest.raises(KeyError)),
        (ard_pixel_ndvi, does_not_raise()),
    ],
)
def test_get_modeled_index(test_data, test_result):
    """
    Verify model predicted index curve results.
    """
    model_index_result = plot_specs.get_modeled_index(
        ard=test_data, results=segment_test_data, predicted_values=pred_value_test_data,
    )
    with test_result:
        assert model_index_result["ndvi-modeled"]


@pytest.mark.parametrize(
    "test_data, test_result_index, test_result_band, test_result_all",
    [
        (
            ard_pixel_dates_array,
            pytest.raises(KeyError),
            does_not_raise(),
            pytest.raises(KeyError),
        ),
        (ard_pixel_ndvi, does_not_raise(), does_not_raise(), does_not_raise()),
    ],
)
def test_get_lookups(test_data, test_result_index, test_result_band, test_result_all):
    """
    Verify calculated indices from observed values.
    """
    index_lookup, band_lookup, all_lookup = plot_specs.get_lookups(
        ard=test_data, results=segment_test_data, predicted_values=pred_value_test_data
    )
    print(f"-> index_lookup: {index_lookup}")
    print(f"-> band_lookup: {band_lookup}")
    print(f"-> all_lookup: {all_lookup}")
    with test_result_index:
        assert index_lookup["NDVI"]
    with test_result_band:
        assert band_lookup["Green"]
    with test_result_all:
        assert all_lookup["NIR"]


@pytest.mark.parametrize(
    "test_ard, test_band_indice, test_result",
    [
        (ard_pixel_dates_array, ["Green"], pytest.raises(KeyError),),
        (ard_pixel_ndvi, ["NDVI"], does_not_raise()),
    ],
)
def test_index_to_observations(test_ard, test_band_indice, test_result):
    """
    Validate index observations are added to the timeseries pixel rod.
    """
    with test_result:
        assert plot_specs.index_to_observations(ard=test_ard, items=test_band_indice)[
            "ndvi"
        ].any()


@pytest.mark.parametrize(
    "test_num, test_pred_values, test_segment, test_result",
    [(1, pred_value_test_data, segment_test_data, 1304.06),],
)
def test_get_predicts(test_num, test_pred_values, test_segment, test_result):
    """
    Validate model prediction values.
    """
    get_predicts_results = plot_specs.get_predicts(
        num=test_num, predicted_values=test_pred_values, results=test_segment
    )
    print(f"-> get_predicts_results: {get_predicts_results}")
    assert abs(get_predicts_results[0][0] - test_result) < 0.01


@pytest.mark.parametrize(
    "test_days, test_coef, test_intercept, test_result",
    [
        (
            np.array([726691, 726692, 726693, 728360, 728361, 728362]),
            segment_test_data[0]["grcoef"],
            segment_test_data[0]["grint"],
            1304.06,
        ),
        (
            np.array([726691, 726692, 726693, 728360, 728361, 728362]),
            segment_test_data[0]["blcoef"],
            segment_test_data[0]["blint"],
            906.17,
        ),
    ],
)
def test_predicts(test_days, test_coef, test_intercept, test_result):
    """
    Validate segment curve calculations.
    """
    predict_results = plot_specs.predicts(
        days=test_days, coef=test_coef, intercept=test_intercept
    )
    print(f"-> predict_results are: {predict_results}")
    assert abs(predict_results[0] - test_result) < 0.01


@pytest.mark.parametrize(
    "test_ard, fill_mask, scaled_thermal, test_result",
    [
        (
            ard_pixel_dates_array,
            ard_pixel_thermal_fill_mask,
            0,
            pytest.raises(KeyError),
        ),
        (ard_pixel_thermal, ard_pixel_thermal_fill_mask, -2065, does_not_raise()),
    ],
)
def test_rescale_thermal(test_ard, fill_mask, scaled_thermal, test_result):
    """
    Verify ard thermal scaling of brightness temperature.
    """
    with test_result:
        test_ard["thermals"] = plot_specs.rescale_thermal(
            ard=test_ard, fill_mask=fill_mask
        )
        assert test_ard["thermals"][0] == scaled_thermal
