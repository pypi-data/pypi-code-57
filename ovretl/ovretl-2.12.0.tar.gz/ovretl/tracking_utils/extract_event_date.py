import numpy as np
import pandas as pd
from ovretl.tracking_utils.check_shipment_active import check_shipment_active


def extract_event_date_by_sorting(events_shipment_df: pd.DataFrame, ascending: bool, location_key=None):
    if len(events_shipment_df) == 0:
        return np.nan
    events_shipment = events_shipment_df.sort_values(by="date", ascending=ascending).reset_index(drop=True)
    if len(events_shipment) > 0 and location_key is not None:
        if events_shipment.loc[0, "location_type"] == location_key:
            return (
                pd.to_datetime(events_shipment.loc[0, "date"])
                if not pd.isna(events_shipment.loc[0, "date"])
                else np.nan
            )
        return np.nan
    if len(events_shipment) > 0:
        return pd.to_datetime(events_shipment.loc[0, "date"]) if not pd.isna(events_shipment.loc[0, "date"]) else np.nan
    return np.nan


def extract_pickup_event_date(events_shipment_df: pd.DataFrame):
    mask_event_pickup = events_shipment_df["event_description"].apply(lambda e: "Pickup" in e)
    mask_event_not_delivery = events_shipment_df["event_description"].apply(lambda e: "Delivery" not in e)
    event_found_by_description = extract_event_date_by_sorting(
        events_shipment_df=events_shipment_df[mask_event_pickup], ascending=True,
    )
    event_found_by_order = extract_event_date_by_sorting(
        events_shipment_df=events_shipment_df[mask_event_not_delivery], ascending=True, location_key="warehouse",
    )
    if not pd.isna(event_found_by_description):
        return event_found_by_description
    return event_found_by_order


def extract_departure_event_date(events_shipment_df: pd.DataFrame):
    mask_etd = events_shipment_df["is_used_for_etd"] == True
    mask_event_departure = events_shipment_df["event_description"].apply(lambda e: "Departure" in e)
    mask_event_not_arrival = events_shipment_df["event_description"].apply(lambda e: "Arrival" not in e)
    event_found_by_etd = extract_event_date_by_sorting(events_shipment_df=events_shipment_df[mask_etd], ascending=True,)

    event_found_by_description = extract_event_date_by_sorting(
        events_shipment_df=events_shipment_df[mask_event_departure], ascending=True,
    )

    event_first = extract_event_date_by_sorting(
        events_shipment_df=events_shipment_df[mask_event_not_arrival], ascending=True, location_key="harbor",
    )
    if not pd.isna(event_found_by_etd):
        return event_found_by_etd
    if not pd.isna(event_found_by_description):
        return event_found_by_description
    return event_first


def extract_arrival_event_date(events_shipment_df: pd.DataFrame):
    mask_eta = events_shipment_df["is_used_for_eta"] == True
    mask_event_arrival = events_shipment_df["event_description"].apply(lambda e: "Arrival" in e)
    mask_event_not_departure = events_shipment_df["event_description"].apply(lambda e: "Departure" not in e)
    events_shipment = events_shipment_df[mask_eta].sort_values(by="date", ascending=False).reset_index(drop=True)
    if len(events_shipment) > 0:
        return events_shipment.loc[0, "date"]

    event_found_by_eta = extract_event_date_by_sorting(
        events_shipment_df=events_shipment_df[mask_eta], ascending=False,
    )

    event_found_by_description = extract_event_date_by_sorting(
        events_shipment_df=events_shipment_df[mask_event_arrival], ascending=False,
    )

    event_last = extract_event_date_by_sorting(
        events_shipment_df=events_shipment_df[mask_event_not_departure], ascending=False, location_key="harbor",
    )
    if not pd.isna(event_found_by_eta):
        return event_found_by_eta
    if not pd.isna(event_found_by_description):
        return event_found_by_description
    return event_last


def extract_delivery_event_date(events_shipment_df: pd.DataFrame):
    mask_event_delivery = events_shipment_df["event_description"].apply(lambda e: "Delivery" in e)
    mask_event_not_pickup = events_shipment_df["event_description"].apply(lambda e: "Pickup" not in e)

    event_found_by_description = extract_event_date_by_sorting(
        events_shipment_df=events_shipment_df[mask_event_delivery], ascending=False,
    )

    event_last = extract_event_date_by_sorting(
        events_shipment_df=events_shipment_df[mask_event_not_pickup], ascending=False, location_key="warehouse",
    )
    if not pd.isna(event_found_by_description):
        return event_found_by_description
    return event_last


def add_tracking_event_dates(shipments_df: pd.DataFrame, events_shipment_df: pd.DataFrame) -> pd.DataFrame:
    pickup_dates = events_shipment_df.groupby("shipment_id").apply(extract_pickup_event_date)
    departure_dates = events_shipment_df.groupby("shipment_id").apply(extract_departure_event_date)
    arrival_dates = events_shipment_df.groupby("shipment_id").apply(extract_arrival_event_date)
    delivery_dates = events_shipment_df.groupby("shipment_id").apply(extract_delivery_event_date)

    shipments_with_events_df = pd.merge(
        shipments_df, pickup_dates.to_frame("pickup_date"), left_on="shipment_id", right_index=True, how="left",
    )

    shipments_with_events_df = pd.merge(
        shipments_with_events_df,
        departure_dates.to_frame("departure_date"),
        left_on="shipment_id",
        right_index=True,
        how="left",
    )

    shipments_with_events_df = pd.merge(
        shipments_with_events_df,
        arrival_dates.to_frame("arrival_date"),
        left_on="shipment_id",
        right_index=True,
        how="left",
    )

    shipments_with_events_df = pd.merge(
        shipments_with_events_df,
        delivery_dates.to_frame("delivery_date"),
        left_on="shipment_id",
        right_index=True,
        how="left",
    )
    shipments_with_events_df.loc[:, "is_active"] = shipments_with_events_df.apply(
        lambda s: check_shipment_active(s, events_shipment_df), axis=1
    )
    return shipments_with_events_df
