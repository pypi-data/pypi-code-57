import json
import os
import time
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

import cognite.air_ds_util.utils as utils
from cognite.client.data_classes import Event, EventList
from cognite.client.exceptions import CogniteDuplicatedError

path_to_model = os.path.abspath(__file__)
model_dir = os.path.dirname(path_to_model)


def merge_time_intervals(date_list: List[List]) -> List[List]:
    """ takes a list of time intervals and returns a list with non overlapping intervals

    :param date_list: list of time intervals [start_time end_time]
    :return:
    """
    s = sorted(map(sorted, date_list))
    merged: List[List] = []
    for higher in s:
        if not merged:
            merged.append(higher)
        else:
            lower = merged[-1]
            if higher[0] <= lower[1]:
                upper_bound = max(lower[1], higher[1])
                merged[-1] = [lower[0], upper_bound]
            else:
                merged.append(higher)
    return merged


def merge_events_dict(events_dict_list: List[Dict]) -> List:
    """ takes a list of dicts {'time_interval': [time0 time1], 'attr0': val0, 'attri': vali}"""

    for d in events_dict_list:
        d.update({"time_interval": sorted(d["time_interval"])})
    events_dict_list_sorted = sorted(events_dict_list, key=lambda d: d["time_interval"][0])
    merged: List[Dict] = []
    for higher in events_dict_list_sorted:
        if not merged:
            merged.append(higher)
        else:
            lower = merged[-1]
            if higher["time_interval"][0] <= lower["time_interval"][1]:
                upper_bound = max(lower["time_interval"][1], higher["time_interval"][1])
                merged[-1]["time_interval"] = [lower["time_interval"][0], upper_bound]
            else:
                merged.append(higher)
    return merged


def unified_event_creator(events_to_create, ts_id, external_id, client, metadata=None):
    if not metadata:
        metadata = {}

    model_name = utils.retrieve_model_name()
    model_version = utils.retrieve_version()
    events_merged = merge_time_intervals(events_to_create)
    events_in_cdf = client.events.list(
        type="AIR",
        subtype="model_output",
        metadata={"time_series_external_id": external_id, "model": model_name, "model_version": model_version},
        limit=-1,
    )
    metadata.update(
        {
            "event_type": model_name,
            "time_series_id": ts_id,
            "time_series_external_id": external_id,
            "model_sequence": model_name,
        }
    )
    events_filtered = filter_and_update(client, date_list=events_merged, events_in_cdf=events_in_cdf, metadata=metadata)
    return events_filtered


def filter_and_update(client, date_list, events_in_cdf, metadata) -> Tuple[List, pd.DataFrame]:
    """checks if events already exists in CDF, if so remove them from date_list
    5 cases:
    1. no event in cdf: create events from date_list
    2. perfect match: remove events from date_list
    3. new events fit in events_in_cdf: remove those events from date_list
    4. events_in_cdf fit into date_list: remove those events from cdf
    5. overlap between events_in_cdf and date_list: merge both, remove original event in cdf

    :param client: CogniteClient
    :param date_list: list of list of start and end time of shutdown
    :param events_in_cdf: events in CDF to compare date_list with
    :return: list of list of start and end time of shutdown
    """
    if not date_list:
        return [], pd.DataFrame()
    date_df = pd.DataFrame(date_list)

    # 1. case
    if not events_in_cdf:  # if no event in CDF, create all date_list events
        create_events(client, date_list, metadata=metadata)
        return date_list, pd.DataFrame()

    dates_in_cdf = []
    for event_in_cdf in events_in_cdf:
        dates_in_cdf.append([event_in_cdf.start_time, event_in_cdf.end_time])
    events_in_cdf = events_in_cdf.to_pandas()

    # 2. case: remove to be written events if they already exist in CDF (perfect match)
    dl_rem = date_df.apply(
        lambda y: not any((y[0] == events_in_cdf.loc[:, "startTime"]) & (y[1] == events_in_cdf.loc[:, "endTime"])),
        axis=1,
    )

    date_df = date_df[dl_rem]
    if not date_df.shape[0]:  # when date_list empty, return it
        return date_df.to_numpy().tolist(), pd.DataFrame()

    # case 3. - 5.
    date_list = date_df.to_numpy().tolist() + dates_in_cdf
    date_list = merge_time_intervals(date_list)
    # remove from date_list those intervals that are in CDF
    final_list = [x for x in date_list if x not in dates_in_cdf]
    date_df = pd.DataFrame(final_list)

    # at this stage date_df can be empty (if results after filtering are already in CDF)
    if len(date_df) == 0:
        return final_list, pd.DataFrame()

    # remove events in CDF that have an overlap with any of the merged events in date_list
    # get events that are in between the event that is going to be written and remove them
    events_in_cdf_to_remove = events_in_cdf[
        events_in_cdf.apply(
            lambda y: any(
                (y.startTime >= date_df[:][0]) & (y.endTime <= date_df[:][1])
                | (y.startTime >= date_df[:][0]) & (y.startTime <= date_df[:][1])
                | (y.endTime >= date_df[:][0]) & (y.endTime <= date_df[:][1])
                | (y.startTime <= date_df[:][0]) & (y.endTime >= date_df[:][1])
            ),
            axis=1,
        )
    ]
    if len(events_in_cdf_to_remove) > 0:
        delete_events_from_cdf(client, events_in_cdf_to_remove)

    create_events(client=client, date_list=final_list, metadata=metadata)

    return final_list, events_in_cdf_to_remove


def delete_events_from_cdf(client, events_df):
    """delete events stored in a pandas DF
    :param client : CDF client
    :param events_df : dataframe holding the events to be deleted"""
    list_events_id_to_remove = events_df.id
    for i in list_events_id_to_remove.to_list():
        if not np.isnan(i):
            client.events.delete(id=i)
            time.sleep(1)


def filter_and_update_dict(client, dict_list, **kwargs) -> Tuple[list, int]:
    """checks if events already exists in CDF, if so remove them from date_list

    :param client: CogniteClient
    :param dict_list: list of dicts with events properties
    :return: list of list of start and end time of shutdown
    """
    if not dict_list:
        return [], 0
    # dict_list = pd.DataFrame(dict_list)

    # extract system number from time series and asset name
    # give CDF time to register events created
    time.sleep(5)

    events_in_cdf = client.events.list(
        type="AIR",
        metadata={
            "time_series_id": kwargs["time_series_id"],
            "bird": kwargs["bird"],
            "bird_version": kwargs["bird_version"],
        },
        limit=-1,
    )

    if not events_in_cdf:  # if no event in CDF, create all date_list events
        create_events_from_dict(client, pd.DataFrame(dict_list), kwargs)
        # return dict_list.to_numpy().tolist(), kwargs
        return [], 1

    events_in_cdf = events_in_cdf.to_pandas()

    # remove to be written events if they already exist in CDF (perfect match)
    dl_rem = pd.DataFrame(dict_list).apply(
        lambda y: not any(
            (y["time_interval"][0] == events_in_cdf.loc[:, "startTime"])
            & (y["time_interval"][1] == events_in_cdf.loc[:, "endTime"])
        ),
        axis=1,
    )

    dict_list = pd.DataFrame(dict_list)[dl_rem]
    if not dict_list.shape[0]:  # when date_list empty, return it
        # return dict_list.to_numpy().tolist(), 2
        return [], 2

    # get events that are in between the event that is going to be written and remove them
    events_in_cdf_to_remove = events_in_cdf[
        events_in_cdf.apply(
            lambda y: (y.startTime >= dict_list["time_interval"].map(lambda x: x[0]))
            & (y.endTime <= dict_list["time_interval"].map(lambda x: x[1])),
            axis=1,
        )
    ]

    if len(events_in_cdf_to_remove) > 0:
        list_events_id_to_remove = events_in_cdf_to_remove.id
        for i in list_events_id_to_remove.to_list():
            if not np.isnan(i):
                client.events.delete(id=i)

    create_events_from_dict(client=client, dict_list=dict_list, metadata=kwargs)

    return dict_list.to_numpy().tolist(), 3


def create_events(client, date_list, metadata):
    """Creates events in CDF

    :param client: client
    :param date_list: list of list with start and end date
    :param metadata: event metadata
    :return: list of events
    """
    # write events
    # date_list = date_list.to_numpy().tolist()
    # listed_events = []
    # check if metadata was passed as is (cf Birdwatcher)
    if metadata.get("metadata") is not None:
        metadata = metadata.get("metadata")
    for dates in date_list:
        # add min granularity to end date if equals start date
        if dates[0] == dates[1]:
            dates[1] = dates[1] + 1
        utils.create_event(
            ts_id=metadata.get("time_series_id"),
            ts_external_id=metadata.get("time_series_external_id"),
            start=dates[0],
            end=dates[1],
            client=client,
            metadata=metadata,
        )


def create_events_from_dict(client, dict_list, metadata):
    """Creates events in CDF

    :param client: client
    :param dict_list: list of dicts with events attributes
    :param metadata: event metadata
    :return: list of events
    """
    # write events
    # dict_list = dict_list.to_numpy().tolist()
    # listed_events = []
    for x, event in dict_list.iterrows():
        # add min granularity to end date if equals start date
        if event["time_interval"][0] == event["time_interval"][1]:
            event["time_interval"][1] = event["time_interval"][1] + 1
        result = {}
        for key in event.keys():
            if key != "time_interval":
                result[key] = event[key]

        metadata["alert"] = str(abs(result["standard_deviations_to_closest_peak"]) > metadata["threshold"])
        result = json.dumps(result)
        metadata["result"] = result
        eve = Event(
            external_id=utils.create_event_external_id(
                metadata.get("time_series_external_id"),
                metadata.get("model"),
                metadata.get("model_version"),
                event["time_interval"][0],
                event["time_interval"][1],
            ),
            data_set_id=utils.retrieve_data_set_id(client),
            start_time=event["time_interval"][0],
            end_time=event["time_interval"][1],
            type="AIR",
            cognite_client=client,
            metadata=metadata,
        )
        # listed_events.append(eve)
        try:
            client.events.create(eve)
        except CogniteDuplicatedError:
            print("Event not written because it's duplicated.")
    # return date_list


def get_last_events(client, event_type, event_subtype, metadata, nb_events) -> EventList:
    """ Method that returns the list of latest nb_events ordered by start date

    :param client: CDF client
    :param event_type: type of event e.g. "shutdown", "transient"
    :param event_subtype: subtype of event e.g. "27KA28-PRIM"
    :param metadata: metadata containing agent type, version, etc.
    :param nb_events: max number of events to retrieve
    :return: list of events
    """
    # get all events
    event_list = client.events.list(type=event_type, subtype=event_subtype, metadata=metadata, limit=-1)
    # sort them by start date and get last nb_events
    event_list = event_list[-nb_events:]
    return event_list
