import hashlib
import inspect
import json
import os
import re
from pathlib import Path
from typing import Dict

from ruamel.yaml import YAML

from cognite.client.data_classes import Event
from cognite.client.experimental import CogniteClient


def _path_to_function_dir() -> Path:
    stack = inspect.stack()
    function_dir = [f[1] for f in stack if "handler.py" in f[1]][0]
    function_path = Path(function_dir)
    while function_path.parts[-1] != "function":
        function_path = function_path.parent
        if function_path == Path("/"):
            raise BaseException("Could not find function folder.")
    return function_path


def _read_init() -> str:
    init_path = _path_to_function_dir() / "__init__.py"
    with init_path.open(mode="r") as init:
        init_content = init.read()
    return init_content


def retrieve_version() -> str:
    init = _read_init()
    version = init.split("\n")[0].split(" = ")[1]
    version = re.sub('"', "", version)
    version = ".".join(version.split(".")[:-1])
    return version


def retrieve_model_name() -> str:
    init = _read_init()
    model_name = init.split("\n")[1].split(" = ")[1]
    model_name = re.sub('"', "", model_name)
    return model_name


def read_yaml(file: Path) -> Dict:
    yaml_file = YAML(typ="safe").load(file)
    return yaml_file


def retrieve_data_set_id(client: CogniteClient) -> int:
    air_data_set = client.data_sets.list(limit=-1).to_pandas().query('name == "AIR"')
    if not air_data_set.shape[0]:
        raise BaseException("AIR data set does not exist.")
    data_set_id = air_data_set.id.iloc[0]
    return data_set_id


def retrieve_project_name() -> str:
    return os.environ["COGNITE_PROJECT"]


def create_event(
    ts_id: int, ts_external_id: str, start: int, end: int, client: CogniteClient, metadata: Dict = None
) -> Event:

    if metadata is None:
        metadata = {}

    metadata.update(
        {
            "model": retrieve_model_name(),
            "model_asset_id": str(retrieve_model_asset_id(client)),
            "model_version": retrieve_version(),
            "time_series_id": str(ts_id),
            "time_series_external_id": ts_external_id,
            "description": retrieve_model_description(client),
            "type_of_event": retrieve_clean_model_name(client),
        }
    )

    event_external_id = create_event_external_id(ts_external_id, retrieve_model_name(), retrieve_version(), start, end)

    if client.events.retrieve(external_id=event_external_id):
        return Event()

    model_output_event = Event(
        external_id=event_external_id,
        start_time=start,
        end_time=end,
        data_set_id=retrieve_data_set_id(client),
        type="AIR",
        subtype="model_output",
        metadata=metadata,
    )
    client.events.create(model_output_event)
    return model_output_event


def retrieve_schedule_config(client: CogniteClient) -> Dict:
    model_name = retrieve_model_name()
    model_asset = client.assets.list(data_set_ids=retrieve_data_set_id(client), name=model_name)[0].dump()
    return model_asset


def retrieve_model_description(client: CogniteClient) -> str:
    schedule_config = retrieve_schedule_config(client)
    description = schedule_config.get("description")
    return description if description else ""


def retrieve_clean_model_name(client: CogniteClient) -> str:
    schedule_config = retrieve_schedule_config(client)
    metadata = schedule_config.get("metadata")
    return metadata.get("frontEndName") if metadata else ""


def retrieve_model_asset_id(client: CogniteClient) -> int:
    model_name = retrieve_model_name()
    assets = client.assets.list(name=model_name, data_set_ids=[retrieve_data_set_id(client)])
    if len(assets) == 0:
        raise BaseException("No asset for this model.")
    asset_id = assets[0].id
    return asset_id


def create_event_external_id(
    ts_external_id: str, model_name: str, model_version: str, start_time: int, end_time: int
) -> str:

    to_be_hashed = model_name + model_version + ts_external_id + str(start_time) + str(end_time)
    hash_object = hashlib.md5(to_be_hashed.encode())  # nosec
    return hash_object.hexdigest()


def retrieve_dependency(model_name: str) -> str:
    path = _path_to_function_dir() / "resources/dependencies.yaml"
    dependency = read_yaml(path).get(model_name)
    return dependency if dependency else ""


def retrieve_window_size(client: CogniteClient) -> int:
    asset_id = retrieve_model_asset_id(client)
    schedule = json.loads(client.assets.retrieve(asset_id).metadata.get("schedule"))
    if schedule.get("windowSize"):
        return int(schedule.get("windowSize"))
    return 0


def extract_data(client: CogniteClient, data: Dict) -> Dict:
    schedule_asset_external_id = data["schedule_asset_ext_id"]
    schedule_asset = client.assets.retrieve(external_id=schedule_asset_external_id)
    data = json.loads(schedule_asset.metadata["data"])
    return data
