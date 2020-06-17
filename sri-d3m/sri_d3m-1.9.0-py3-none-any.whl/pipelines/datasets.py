import json
import os

from sri.pipelines.parsed_datasets import ALL_DATASETS

# Datasets that are slow because of their size (on disk or number of records).
if (os.environ.get('INCLUDE_SLOW_DATASETS') is not None):
    SLOW_DATASETS = set()
else:
    SLOW_DATASETS = {
        'uu3_world_development_indicators_raw',
        'LL1_MITLL_synthetic_vora_E_2538',
        'SEMI_155_pokerhand_MIN_METADATA',
        'LL1_PHEM_weeklyData_malnutrition_MIN_METADATA',
        'SEMI_1040_sylva_prior_MIN_METADATA',
        'LL0_acled_reduced_MIN_METADATA',
        'LL1_PHEM_Monthly_Malnutrition_MIN_METADATA',
        '313_spectrometer_MIN_METADATA',
        'LL1_736_stock_market_MIN_METADATA',
        '4550_MiceProtein_MIN_METADATA',
        '299_libras_move_MIN_METADATA',
        'SEMI_1044_eye_movements_MIN_METADATA',
        'political_instability_MIN_METADATA',
        'uu3_world_development_indicators_MIN_METADATA',
        '1567_poker_hand_MIN_METADATA',
        '60_jester_MIN_METADATA',
        '124_174_cifar10_MIN_METADATA',
    }

# Datasets that are globally broken for one reason or another.
BLACKLIST = {
    # Incorrectly formatted.
    'LL1_736_population_spawn_MIN_METADATA',
    'LL1_736_population_spawn_simpler_MIN_METADATA',
    'LL1_VTXC_1369_synthetic_MIN_METADATA',
    'LL1_bn_fly_drosophila_medulla_net_MIN_METADATA',
    'LL1_terra_canopy_height_long_form_s4_100_MIN_METADATA',
    'LL1_terra_canopy_height_long_form_s4_80_MIN_METADATA',
    'LL1_FB15k_237',
    'LL1_tidy_terra_panicle_detection_MIN_METADATA',
    'LL1_penn_fudan_pedestrian_MIN_METADATA',
    '31_urbansound_MIN_METADATA',

    # Incorrect metadata.
    'LL1_ACLED_TOR_online_behavior_MIN_METADATA',
    'LL1_336_MS_Geolife_transport_mode_prediction_separate_lat_lon_MIN_METADATA',
    'LL1_h1b_visa_apps_7480',
    'LL1_retail_sales_total_MIN_METADATA',
    'LL1_GS_process_classification_tabular_MIN_METADATA',
    'LL1_GS_process_classification_text_MIN_METADATA',
    'SEMI_1053_jm1_MIN_METADATA',
    'SEMI_1217_click_prediction_small_MIN_METADATA',
    'SEMI_1459_artificial_characters_MIN_METADATA',
    'kaggle_music_hackathon_MIN_METADATA',
    'loan_status_MIN_METADATA',
    'LL1_336_MS_Geolife_transport_mode_prediction_MIN_METADATA',
}

# Remove slow and blacklist datasets from consideration.
for i in reversed(range(len(ALL_DATASETS))):
    if (ALL_DATASETS[i]['name'] in BLACKLIST or ALL_DATASETS[i]['name'] in SLOW_DATASETS):
        ALL_DATASETS.pop(i)

def get_dataset(name):
    for dataset in ALL_DATASETS:
        if (dataset['name'] == name):
            return dataset
    raise LookupError("Could not find a dataset with name: %s" % (name))

def get_dataset_names():
    return [dataset['name'] for dataset in ALL_DATASETS]

def get_problem_id(name):
    return get_dataset(name)['problem_id']

def get_full_dataset_id(name):
    return get_dataset(name)['dataset_id']

def get_train_dataset_id(name):
    return get_dataset(name)['train_dataset_id']

def get_test_dataset_id(name):
    return get_dataset(name)['test_dataset_id']

def get_score_dataset_id(name):
    return get_dataset(name)['score_dataset_id']

def get_size(name):
    return get_dataset(name)['size']

def get_dataset_names_by_task(task_type):
    names = []

    for dataset in ALL_DATASETS:
        if (task_type == dataset['task_type']):
            names.append(dataset['name'])

    return names
