from bytegain.custom.model_data.schema_from_TableInfo import get_schema
from bytegain.custom.model_data.bucket_features import FeatureBucketerNonLinear as bucketer

EXCLUDED_FEATURES = [
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

def bucketer_test(path='/home/yuri/devel/custom/'):
    schemas = get_schema(path, {'features': 'ml_notified_training_set/'})
    b = bucketer(EXCLUDED_FEATURES, schemas['features'], n_numerical_buckets=5)
    b.construct_buckets()
    map_sorted = sorted(iter(list(b._feature_map.items())), key=lambda k_v: (k_v[1], k_v[0]))
    for i in range(len(map_sorted)):
        print(map_sorted[i][1])
    return map_sorted


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
bucketer_test()
