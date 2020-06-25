from collections.abc import Mapping
from pathlib import Path
from typing import Any, Dict, List


def assert_same_keys(configs: Dict[Path, Dict[str, Any]]) -> None:
    if len(configs) == 0:
        return
    config_keys = {key: configs[key].keys() for key in configs}

    base_name = list(config_keys.keys())[0]
    base_keys = config_keys.pop(base_name)

    for name, keys in config_keys.items():
        is_valid = base_keys == keys
        diff = {}
        if len(base_keys - keys) != 0:
            diff[f"{name} is missing"] = base_keys - keys
        if len(keys - base_keys) != 0:
            diff[f"{base_name} is missing"] = keys - base_keys

        assert is_valid, f"YAML files don't contain the same services defined. Differences:\n{diff}"


def merge_dictionaries(configs: List[Dict]) -> Dict:
    base = configs[0].copy()
    if len(configs) == 1:
        return base

    for d in configs[1:]:
        merge_two_dictionaries(base, d)

    return base


def merge_two_dictionaries(dict_a: Dict, dict_b: Dict) -> None:
    for k, v in dict_b.items():
        if k in dict_a and isinstance(dict_a[k], dict) and isinstance(dict_b[k], Mapping):
            merge_two_dictionaries(dict_a[k], dict_b[k])
        else:
            dict_a[k] = dict_b[k]


def assert_scope_matches(configs: Dict[Path, Dict[str, Any]]) -> None:
    if len(configs) != 2:
        return
    keys = list(configs.keys())

    key1 = keys[0]
    config1 = configs[key1]
    key2 = keys[1]
    config2 = configs[key2]

    if "databricks" in config1 and "databricks" in config2:
        for stage in ["production", "development"]:
            name_in_config1 = config1["databricks"][stage]["scope"]["name"]
            name_in_config2 = config2["databricks"][stage]["scope"]["name"]
            assert name_in_config1 == name_in_config2, (
                f"Mismatch between scope name in '{key1}' ({name_in_config1}) and " f"'{key2}' ({name_in_config2})."
            )
