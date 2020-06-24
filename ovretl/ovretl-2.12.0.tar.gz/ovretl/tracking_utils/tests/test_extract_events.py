import numpy as np
import pandas as pd
from ovretl.tracking_utils.extract_event_date import (
    extract_pickup_event_date,
    extract_arrival_event_date,
    add_tracking_event_dates,
)
from pandas.util.testing import assert_frame_equal


def test_extract_pickup_event():
    pickup_events_shipment_df = pd.DataFrame.from_records(
        [
            {
                "shipment_id": 0,
                "event_description": "Pickup",
                "date_type": "actual",
                "date": pd.Timestamp("2020-01-02 23:00:00"),
                "location_type": "warehouse",
            },
            {
                "shipment_id": 0,
                "event_description": "Pickup",
                "date_type": "estimated",
                "date": pd.Timestamp("2015-01-05 23:00:00"),
                "location_type": "warehouse",
            },
        ]
    )
    pickup_date = extract_pickup_event_date(events_shipment_df=pickup_events_shipment_df,)
    assert pickup_date == pd.Timestamp("2015-01-05 23:00:00")


def test_extract_arrival_event():
    arrival_events_shipment_df = pd.DataFrame.from_records(
        [
            {
                "shipment_id": 0,
                "event_description": "Arrival",
                "date_type": "actual",
                "date": pd.Timestamp("2020-01-02 23:00:00"),
                "is_used_for_eta": False,
                "location_type": "harbor",
            },
            {
                "shipment_id": 0,
                "event_description": "Arrival",
                "date_type": "estimated",
                "date": pd.Timestamp("2015-01-05 23:00:00"),
                "is_used_for_eta": True,
                "location_type": "harbor",
            },
        ]
    )
    arrival_date = extract_arrival_event_date(events_shipment_df=arrival_events_shipment_df,)
    assert arrival_date == pd.Timestamp("2015-01-05 23:00:00")


def test_add_tracking_events():
    events_shipment_df = pd.DataFrame.from_records(
        [
            {
                "shipment_id": 0,
                "event_description": "Pickup",
                "date_type": "actual",
                "date": pd.Timestamp("2020-01-02 23:00:00"),
                "location_type": "warehouse",
                "is_used_for_etd": False,
                "is_used_for_eta": False,
            },
            {
                "shipment_id": 0,
                "event_description": "Pickup",
                "date_type": "estimated",
                "date": pd.Timestamp("2015-01-05 23:00:00"),
                "location_type": "warehouse",
                "is_used_for_etd": False,
                "is_used_for_eta": False,
            },
        ]
    )
    shipments_df = pd.DataFrame(
        data={"shipment_id": [0], "cancelled": [False], "shipment_status": ["in_progress"], "finished_date": [np.nan],}
    )
    result = add_tracking_event_dates(shipments_df, events_shipment_df)
    result_should_be = pd.DataFrame(
        data={
            "shipment_id": [0],
            "cancelled": [False],
            "shipment_status": ["in_progress"],
            "finished_date": [np.nan],
            "pickup_date": [pd.Timestamp("2015-01-05 23:00:00")],
            "departure_date": [np.nan],
            "arrival_date": [np.nan],
            "delivery_date": [np.nan],
            "is_active": [True],
        }
    )
    assert_frame_equal(result, result_should_be)
