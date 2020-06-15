from typing import Optional
from splitiorequests.schemas.splits.split_schema import SplitSchema
from splitiorequests.schemas.splits.split_schema_exclude import SplitSchemaExclude
from splitiorequests.models.splits.split import Split
from splitiorequests.schemas.splits.split_definition_schema import SplitDefinitionSchema
from splitiorequests.schemas.splits.split_definition_schema_exclude import SplitDefinitionSchemaExclude
from splitiorequests.models.splits.split_definition import SplitDefinition
from splitiorequests.models.splits.split_definitions import SplitDefinitions
from splitiorequests.schemas.splits.split_definitions_schema import SplitDefinitionsSchema
from splitiorequests.schemas.splits.split_definitions_schema_exclude import SplitDefinitionsSchemaExclude
from splitiorequests.schemas.splits.splits_schema import SplitsSchema
from splitiorequests.schemas.splits.splits_schema_exclude import SplitsSchemaExclude
from splitiorequests.models.splits.splits import Splits
from splitiorequests.common.utils import Utils


def load_split(data: dict, unknown_handler: str = 'RAISE') -> Optional[Split]:
    loaded_split = None
    handler = Utils.get_unknown_field_handler(unknown_handler)
    if handler == "raise":
        loaded_split = SplitSchema().load(data)
    elif handler == "exclude":
        loaded_split = SplitSchemaExclude().load(data)
    return loaded_split


def dump_split(split_obj: Split) -> dict:
    dumped_split = SplitSchema().dump(split_obj)
    return dumped_split


def load_splits(data: dict, unknown_handler: str = 'RAISE') -> Optional[Splits]:
    loaded_splits = None
    handler = Utils.get_unknown_field_handler(unknown_handler)
    if handler == "raise":
        loaded_splits = SplitsSchema().load(data)
    elif handler == "exclude":
        loaded_splits = SplitsSchemaExclude().load(data)
    return loaded_splits


def dump_splits(split_obj: Splits) -> dict:
    dumped_splits = SplitsSchema().dump(split_obj)
    return dumped_splits


def load_split_definition(data: dict, unknown_handler: str = 'RAISE') -> Optional[SplitDefinition]:
    loaded_split_definition = None
    handler = Utils.get_unknown_field_handler(unknown_handler)
    if handler == "raise":
        loaded_split_definition = SplitDefinitionSchema().load(data)
    elif handler == "exclude":
        loaded_split_definition = SplitDefinitionSchemaExclude().load(data)
    return loaded_split_definition


def dump_split_definition(split_definition_obj: SplitDefinition) -> dict:
    dumped_split_definition = SplitDefinitionSchema().dump(split_definition_obj)
    return dumped_split_definition


def load_split_definitions(data: dict, unknown_handler: str = 'RAISE') -> Optional[SplitDefinitions]:
    loaded_split_definitions = None
    handler = Utils.get_unknown_field_handler(unknown_handler)
    if handler == "raise":
        loaded_split_definitions = SplitDefinitionsSchema().load(data)
    elif handler == "exclude":
        loaded_split_definitions = SplitDefinitionsSchemaExclude().load(data)
    return loaded_split_definitions


def dump_split_definitions(split_definitions_obj: SplitDefinitions) -> dict:
    dumped_split_definitions = SplitDefinitionsSchema().dump(split_definitions_obj)
    return dumped_split_definitions
