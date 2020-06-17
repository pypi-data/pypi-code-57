def assert_version(version, version_json):
    assert version.id == version_json["id"]
    assert version.environment_id == version_json["environmentId"]
    assert version.label == version_json["label"]
    assert version.description == version_json["description"]
    assert version.build_status == version_json["buildStatus"]
    assert version.created_at == version_json["created"]


def assert_custom_model_version(version, version_json):
    assert version.id == version_json["id"]
    assert version.custom_model_id == version_json["customModelId"]
    assert version.label == version_json["label"]
    assert version.description == version_json["description"]
    assert version.version_minor == version_json["versionMinor"]
    assert version.version_major == version_json["versionMajor"]
    assert version.is_frozen == version_json["isFrozen"]

    assert len(version.items) == len(version_json["items"])
    for item, item_json in zip(version.items, version_json["items"]):
        assert item.id == item_json["id"]
        assert item.file_name == item_json["fileName"]
        assert item.file_path == item_json["filePath"]
        assert item.file_source == item_json["fileSource"]
        assert item.created_at == item_json["created"]

    assert version.created_at == version_json["created"]
