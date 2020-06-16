import pickle

from bytegain.data_import.segment_utils import parse_s3_url

# file = open("bytegain/cust/apartmentlist/data/all_features/lead_scoring_lead_scoring_set/lead_scoring.lead_scoring_set..pickle")
filespec = "gs://bg-dataflow/all_features"
# filespec = "gs://bg-dataflow/all_features/web_pages/"

filespec = "gs://bg-dataflow/apartmentlist/user_value/1year_date_fix"


def get_schema(filespec, subdirs={'events':'/web_pages/', 'features':'/lead_scoring_lead_scoring_set_with_model/',
                                  'identifies':'/api_identifies/', 'interest':'/api_interest/'}):
    from google.cloud import storage
    client = storage.Client()
    bucket_name, key, _ = parse_s3_url(filespec)
    bucket = client.get_bucket(bucket_name)
    tables_info = {}
    for k, v in list(subdirs.items()):
        path = key + v
        blobs = bucket.list_blobs(prefix=path)
        for blob in blobs:
            if (blob.name).endswith('.pickle'):
                file = blob
        pickle_string = file.download_as_string()
        table_info = pickle.loads(pickle_string)
        tables_info[k] = table_info
    return tables_info

schemas = get_schema(filespec)
features = schemas['features']
identifies = schemas['identifies']

sample = {"budget_min":"630","dwell_time":"149","commute_minutes":"","user_id":"236156686",
          "interest_state":"strong_interest","viewed_availability":"t","registered_source_partner":"apartment_list",
          "interest_source_app":"MobileApartmentList","property_lat":"39.974504",
          "preferred_budget_deviation":"1.04046242","preferred_available_units":"45","label":"f",
          "positive_velocity_rate":"0.53508771929824561","preferred_units":"75","search_category":"Email",
          "registered_source_app":"MobileApartmentList","budget_max":"900",
          "preferences_move_urgency":"0.80000000000000004","timestamp":"2017-01-11 06:00:14.914","move_in_delay":"-123",
          "metro_id":"747240","preferences_lease_length":"12","commute_distance":"","commute_mode":"",
          "preferences_baths":"","property_lon":"-86.080742","distance":"2.861052221994","rental_id":"p10663",
          "interest_source_partner":"apartment_list","median_preferred_price":"865.0","preferences_beds_2":"f",
          "preferences_beds_3":"f","preferences_beds_0":"f","preferences_beds_1":"t","property_zip_code":"46033",
          "email_clicked":"t","average_preferred_price":"904","has_phone_number":"t","data_updated_at":"2017-10-18 23:58:33"}


# Maps categorical feature to index
def category_to_index(groups):
    cat_ind_map = {}
    for index, (name, fraction) in enumerate(groups):
        if not name:
            name = ''
        cat_ind_map[name] = index
    if '' not in cat_ind_map:
        cat_ind_map[''] = index + 1
    return cat_ind_map

def numerical_to_index(value, vals, num_buckets):
    import numpy as np
    (median, perc25, perc75) = vals
    bins = np.arange(perc25, perc75, abs(perc75 - perc25) / num_buckets)
    bins = np.insert(bins, 0, -np.inf)
    bins = np.append(bins, np.inf)
    if value is None:
        return len(bins), len(bins) + 1
    # TODO: Add minus and plus infinities into bins
    index = np.digitize(value, bins) - 1
    return index, len(bins) + 1

excluded_features = [
    'opened_email',
    'email_opens_count',
    'email_clicks_count',
    'matching_units',
    'all_price',
    'availability_views',
    'commute_congestion',
    'preferences_amenities',
    'preferences_beds',
    'score',
    'interest_id',
    'leased_at_notified_property',
    'matched_user',
    'commute_lat',
    'commute_lon',
    'source_app',
    'median_matching_price',
    'photo_gallery_views',
    'prev_interests',
    'consent_call_consent',
    'consent_email_consent',
    'preferences_contracts',
    'renter_phone_area_code',
    'renter_phone_exchange',
    'interest_created_at',
    'total_units',
    'matched_interest',
    'user_id',
    'preferences_wants_dishwasher',
    'preferences_most_important_feature',
    'preferences_wants_on_site_laundry',
    'preferences_wants_gym',
    'preferences_wants_in_unit_laundry',
    'preferences_wants_dog_friendly',
    'preferences_wants_pool',
    'preferences_wants_air_conditioning',
    'preferences_wants_parking',
    'preferences_cotenant',
    'preferences_cosigner',
    'avg_12mo_2bd_location_price',
    'relative_2bd_price',
    'property_lat_round',
    'property_lon_round',
    'property_to_total_velocity_rate',
    'positive_interest_velocity',
    'total_interest_velocity',
    'score',
    'model',
    'version',
    'rental_id',
    'label',
    'extra_label',
    'leased_at_property',
    'value_on',
    'event_id',
    'property_city_id',
    'email_domain',
    'registered_source_partner',
    'registered_source_app',
    'interest_source_app',
    'property_zip_code',
    'metro_id',
    'property_lon',
    'property_lat'
]
# Maps each feature to index
def get_maps(features):
    maps = {}
    cats, bools, other, time, excluded = 0, 0, 0, 0, 0
    excluded_set = set(excluded_features)
    for col in features.columns:
        if col.name in excluded_set:
            excluded += 1
            continue
        if 'character' in col.datatype:
            if col.name == 'rental_id':
                continue
            maps[col.name] = category_to_index(sorted(col._groups, key=lambda x: x[1]))
            cats += 1
        elif col.datatype == 'boolean':
            maps[col.name] = {'t': 1, 'f': 0}
            bools += 1
        elif 'time' in col.datatype:
            time += 1
        else:
            vals = col.median, col.percentile_25, col.percentile_75
            maps[col.name] = lambda x, vals=vals: numerical_to_index(x, vals, 7)
            other += 1
    print(("Total features without excluded and time: %d, categorical: %d, boolean :%d, other %d" % (
    len(features.columns) - excluded - time, cats, bools, other)))
    return maps

# def sample_to_one_hot(sample):
#     sample_one_hot = {}
#     for k, v in sample.iteritems():
#         bucket_map = maps.get(k, [])
#         bucket_len = len(bucket_map)
#         if bucket_len > 0:
#             sample_one_hot[k] = [bucket_len, bucket_map.get(v)]
#     return sample_one_hot

def sample_to_vec(sample, maps):
    sample_vec = []
    bucketed_features = 0
    for k, v in list(sample.items()):
        bucket_map = maps.get(k, [])
        if callable(bucket_map):
            num = None if v == '' else float(v)
            index, bucket_len = bucket_map(num)
        else:
            bucket_len = len(bucket_map)
            index = None
        print('Feature: %s' % k)
        if bucket_len > 0:
            vec = [0] * bucket_len
            if index is not None:
                vec[index] = 1
            else:
                vec[bucket_map.get(v)] = 1
            sample_vec += vec
            bucketed_features += 1
    print('Sample: total features %s, bucketed features %s' % (len(sample), bucketed_features))
    return sample_vec

# import time
# time0 = time.time()
# maps = get_maps(features)
# # for k, v in maps.iteritems():
# #     print '%s: %s'%(k, v)
# maps_time = time.time()
# # sample_one_hot = sample_to_one_hot(sample)
# # print 'Bucketed sample: %s' % sample_one_hot
# vec = sample_to_vec(sample, maps)
# vec_time = time.time()
# print 'Len vec %d, vec: %s' % (len(vec), vec)
# print 'Maps time %.4f' % (maps_time - time0)
# print 'Vec time %.4f' % (vec_time - maps_time)

from bytegain.custom.model_data.bucket_features import FeatureBucketerLinear as feature_bucketer
bucketer = feature_bucketer(excluded_features, features)
bucketer.construct_buckets()
vec_bucketed = bucketer.sample_to_vec(sample)
print('Length %d, vec: %s' % (len(vec_bucketed), vec_bucketed))

print('Nonlinear bucketer')
from bytegain.custom.model_data.bucket_features import FeatureBucketerNonLinear as feature_bucketer
bucketer = feature_bucketer(excluded_features, features)
bucketer.construct_buckets()
vec_bucketed = bucketer.sample_to_vec(sample)
print('Length %d, vec: %s' % (len(vec_bucketed), vec_bucketed))

print('Direct bucketer')
from bytegain.custom.model_data.bucket_features import FeatureBucketerDirect as feature_bucketer
bucketer = feature_bucketer(excluded_features, features)
bucketer.construct_buckets()
vec_bucketed = bucketer.sample_to_vec(sample)
print('Length %d, vec: %s' % (len(vec_bucketed), vec_bucketed))
