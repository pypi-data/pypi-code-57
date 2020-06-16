from bytegain.custom.cust.apartmentlist.feature_filter import FeatureFilter

from .common import EXCLUDED_FEATURES

NUMERICAL_FEATURES = ['account_age_hours',
 'commute_mode_tr',
 'demand_ratio',
 'distinct_properties_viewed_1w',
 'dwell_time_bucket',
 'email_verified',
 'event_week',
 'has_phone_number',
 'interest_order',
 'latitude',
 'ldp_views_1w',
 'lease_pms_tr',
 'move_in_delay',
 'notifiable',
 'positive_interest_count',
 'positive_velocity_rate',
 'preferences_beds_0',
 'preferences_beds_1',
 'preferences_beds_2',
 'preferences_beds_3',
 'preferences_move_urgency',
 'preferred_available_units',
 'preferred_budget_deviation',
 'preferred_units',
 'property_in_preferred_city',
 'recent_user_ldp_views',
 'rental_id_tr',
 'total_units']

# NUMERICAL_FEATURES_OLD = ['account_age_hours',
#  'average_preferred_price',
#  'average_preferred_price_tr',
#  'budget_max',
#  'budget_max_tr',
#  'budget_min',
#  'budget_min_tr',
#  'commute_distance_tr',
#  'commute_minutes_tr',
#  'commute_mode_tr',
#  'contact_model_tr',
#  'cosigner_tr',
#  'demand_ratio',
#  'demand_ratio_tr',
#  'distinct_properties_viewed_1w',
#  'dwell_time_bucket_tr',
#  'dwell_time_bucket',
#  'dwell_time_tr',
#  'email_domain_tr',
#  'email_marketing_tr',
#  'email_verified',
#  'event_month',
#  'event_week',
#  'gallery_viewed_1w',
#  'has_been_evicted_tr',
#  'has_phone_number',
#  'has_rent_special',
#  'interest_order',
#  'interest_source_app_tr',
#  'interest_source_partner_tr',
#  'interest_state_current_tr',
#  'latitude',
#  'ldp_views_1w',
#  'lead_pms_tr',
#  'lease_pms_tr',
#  'longitude',
#  'median_pi_cnt_tr',
#  'median_preferred_price_tr',
#  'median_units_available_tr',
#  'metro_id_tr',
#  'most_important_feature_tr',
#  'move_in_delay',
#  'notifiable',
#  'NOTIFICATION_RATE',
#  'p_avgprice_tr',
#  'p_medianprice_tr',
#  'persona_tr',
#  'photo_num_tr',
#  'photo_view_after_tr',
#  'positive_interest_count',
#  'positive_velocity_rate',
#  'preferences_beds_0',
#  'preferences_beds_1',
#  'preferences_beds_2',
#  'preferences_beds_3',
#  'preferences_lease_length_tr',
#  'preferences_move_urgency',
#  'preferred_available_units',
#  'preferred_budget_deviation',
#  'preferred_units',
#  'price_discrepancy_tr',
#  'product_epoch_tr',
#  'property_built_year_tr',
#  'property_city_center_distance_tr',
#  'property_city_id_tr',
#  'PROPERTY_HEALTH',
#  'property_in_preferred_city',
#  'property_in_preferred_neighborhood',
#  'property_remodeled_year_tr',
#  'property_zip_code_tr',
#  'recent_user_ldp_views',
#  'registered_source_app_tr',
#  'registered_source_partner_tr',
#  'rental_id_tr',
#  'sign_in_cnt_tr',
#  't30_saturation_band_tr',
#  't30_saturation_score_tr',
#  't7_saturation_band_tr',
#  't7_saturation_score_tr',
#  'total_units',
#  'view_after_ratio_tr',
#  'view_photo_num_tr',
#  'view_photo_percentage_tr']

# CATEGORY_FEATURES_OLD = ['bump',
#  'commute_mode',
#  'contact_model',
#  'email_domain',
#  'interest_source_app',
#  'interest_source_partner',
#  'interest_state_current',
#  'lead_pms',
#  'lease_pms',
#  'metro_id',
#  'most_important_feature',
#  'persona',
#  'product_epoch',
#  'property_city_id',
#  'registered_source_app',
#  'registered_source_partner',
#  't30_saturation_band',
#  't7_saturation_band','notifiable']

CATEGORY_FEATURES = ['commute_mode',
 'contact_model',
 'interest_source_app',
 'interest_state_current',
 'metro_id',
 'most_important_feature',
 'notifiable',
 'product_epoch']

BUCKET_FEATURES = [
]

MODEL_TITLE = "data_science"
VERSION = "1.0.0"

filter = FeatureFilter(EXCLUDED_FEATURES, NUMERICAL_FEATURES, CATEGORY_FEATURES, [])



config = {'table': 'SCRATCH.ZLI.LS2_TRAIN',
          'model_name': MODEL_TITLE,
          'model_version': VERSION,
          'feature_json': MODEL_TITLE + '_' + VERSION,
          'filter': filter,
          'outcome_field': 'leased_at_property',
          'control_field': 'lsd_control',
          'positive_outcome_rate_field': 100.,
          'control_weight': 1,
          'subsample': 0.7787,
          'gamma':0.827254,
          'id_field': 'event_id',
          'random_seed': 147,
          'max_rounds': 101,
          'max_depth': 3,
          'train_step_size': 0.2,
          'min_child_weight': 844,
          'l2_norm':   37.8157,
          'l1_norm': 27.223769798,
          'eval_metric':'auc',  #'aucpr'
          'scale_pos_weight':18,
          'minority_class_prop':0.0027,
          'downsample': False,
          'grow_policy':'lossguide',#'depthwise'
          'start_date': '2019-01-01',
          'end_date': '2020-02-10'}  




test_config = dict(config)
test_config['table'] = 'scratch.GDURKIN.ML_TEST_ORDERED_JUNE'#'scratch.GDURKIN.LS2_AFTER'
test_config['downsample'] = False
test_config['minority_class_prop'] = 0.0027

prod_config = dict(config)



prod_config['downsample'] = False
