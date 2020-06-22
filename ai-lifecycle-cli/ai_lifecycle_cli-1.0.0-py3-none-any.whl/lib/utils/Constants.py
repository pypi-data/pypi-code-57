#  © Copyright IBM Corporation 2020.

EXPORT_SUPPORTED_ASSET_TYPES = [
    'wml_model',
    'wml_model_definition',
    'omrs_relationship_message',
    'policy_transform',
    'folder_asset',
    'asset_terms',
    'connection',
    'wml_function',
    'wml_pipeline',
    'wml_experiment',
    'omrs_relationship',
    'omrs_entity',
    'column_info',
    'data_asset',
    'environment',
    'notebook',
    'script',
    'shiny_asset'
]

ASSET_EXCLUDED_METADATA = [
    'asset_state',
    'catalog_id',
    'created',
    'rating',
    'rov',
    'source_asset',
    'total_ratings',
    'version'
]


WML_RESOLVABLE_ASSET_TYPES = [
        'wml_model',
        'wml_model_definition',
        'wml_function',
        'wml_pipeline',
        'wml_experiment',
        'script',
        'shiny_asset'
    ]


WML_DEPENDENCY_MAP = {
        "wml_model": {
            "training_lib.id": "wml_model_definition",
            "training_lib.href": "wml_model_definition",
            "model_definition.id": "wml_model_definition",
            "pipeline.id": "wml_pipeline",
            "pipeline.href": "wml_pipeline",
            "software_spec.base_id": "software_specification",
            "data_asset_dependencies": "data_asset",
            "training_data_references[].location.href": "data_asset"
        },
        "wml_function": {
            "software_spec.id": "software_specification"
        },
        "wml_pipeline": {
            "document.pipelines[].nodes[].parameters.model_definition": "wml_model_definition",
            "document.pipelines[].nodes[].parameters.training_lib_href": "wml_model_definition",
            "model_definition_dependencies": "wml_model_definition",
            "training_lib_dependencies": "wml_model_definition",
            "document.runtimes[].app_data.wml_data.software_spec.id": "software_specification",
            "software_spec_depenencies": "software_specification"
        },
        "wml_experiment": {
            "training_references[].pipeline.id": "wml_pipeline",
            "pipeline_dependencies": "wml_pipeline",
            "training_references[].training_lib.id": "wml_model_definition",
            "training_lib_dependencies": "wml_model_definition",
            "training_references[].model_definition.id": "wml_model_definition",
            "model_definition_dependencies": "wml_model_definition",
            "training_references[].pipeline.hardware_spec.id": "hardware_specification",
            "training_references[].pipeline.hybrid_pipeline_hardware_specs[].hardware_spec.id": "hardware_specification",
            "hardware_spec_dependencies": "hardware_specification",
            "training_references[].model_definition.software_spec.id": "software_specification",
            "software_spec_dependencies": "software_specification"
        },
        "script": {
            "software_spec.base_id": "software_specification"
        },
        "software_specifications": {
            "package_extensions.metadata.asset_id": "package_extension"
        }
    }