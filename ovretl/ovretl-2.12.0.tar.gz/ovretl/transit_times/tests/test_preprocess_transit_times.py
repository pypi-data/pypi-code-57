import pandas as pd
from ovretl.transit_times.preprocess_transit_times import preprocess_transit_times
from pandas.util.testing import assert_frame_equal


def test_preprocess_transit_times():
    raw_df = pd.read_csv("./ovretl/transit_times/tests/transit_times_data.csv")
    result = preprocess_transit_times(raw_df, 20)
    result_should_be = pd.read_csv("./ovretl/transit_times/tests/preprocessed_transit_times_data.csv")
    assert_frame_equal(result.reset_index(drop=True), result_should_be.reset_index(drop=True))
