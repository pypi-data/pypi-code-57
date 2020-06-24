"""
Copyright 2019 Cognitive Scale, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import warnings
from typing import Optional, Union, cast, Callable, Dict

import attr
import pydash

from cortex_common.constants import CONTEXTS, ATTRIBUTE_VALUES
from cortex_common.types import Dimension
from cortex_common.types import NumberAttributeValue, StringAttributeValue, \
    BooleanAttributeValue, ProfileAttributeValue, EntityEvent, EntityRelationshipAttributeValue, \
    EntityRelationshipEvent, ProfileLink, ProfileRelationshipEvent, ListAttributeValue, DimensionalAttributeValue, \
    ProfileRelationshipAttributeValue, EntityAttributeValue, BaseProfileAttribute
from cortex_common.types import ProfileAttributeSchema
from cortex_common.types.attribute_values import load_profile_attribute_value_from_dict
from cortex_common.utils import get_logger
from cortex_common.utils import is_primitive, key_has_value_in_dict, construct_attr_class_from_dict

TPrimitive = Union[int, float, str, bool]
TProfileLinkAlternatives = Union[str, StringAttributeValue, ProfileLink, dict]

log = get_logger(__name__)
PrimitiveAttributeValues = Union[NumberAttributeValue, StringAttributeValue, BooleanAttributeValue]


def cast_primitive_values(value: Union[int, float, str, bool],
                          context: Optional[str] = None) -> PrimitiveAttributeValues:
    """
    Converts Primitive Values into Attribute Values.
    :param value:
    :param context:
    :return:
    """
    default_contexts = {
        float: ATTRIBUTE_VALUES.NUMBER_PROFILE_ATTRIBUTE_VALUE,
        int: ATTRIBUTE_VALUES.NUMBER_PROFILE_ATTRIBUTE_VALUE,
        str: ATTRIBUTE_VALUES.STRING_PROFILE_ATTRIBUTE_VALUE,
        bool: ATTRIBUTE_VALUES.BOOLEAN_PROFILE_ATTRIBUTE_VALUE,
    }
    type_of_primitive = type(value)
    context = context if context is not None else default_contexts.get(type_of_primitive)
    if context is None:
        emsg = f"Cannot cast value {value} into a PrimitiveAttributeValue."
        log.erorr(f"{emsg} Type: {type_of_primitive}, Optional[Context]: {context}")
        raise ValueError(emsg)
    return cast(PrimitiveAttributeValues, load_profile_attribute_value_from_dict({"value": value, "context": context}))


def extract_specified_linked_schema_id_from_schema_def(attr_schema: dict) -> Optional[str]:
    """
    Determines the inner profile link type ...
    :param attr_schema:
    :return:
    """
    # List[ProfileLink[Investor]] or Dimensional[ProfileLink[Investor], Number] ...
    # In both cases ... profile link is first inner type ...
    profile_type_in_schema = pydash.get(attr_schema, 'valueType.innerTypes[0]', None)
    if profile_type_in_schema is None:
        return None
    return pydash.get(profile_type_in_schema, 'innerTypes[0].outerType', None)


def cast_profile_id(value: Union[str, StringAttributeValue, ProfileLink, dict],
                    attr_schema: Union[dict, ProfileAttributeSchema],
                    default_schema_id: Optional[str] = None) -> Optional[ProfileLink]:
    """
    :param value:
    :param attr_schema:
    :param default_schema_id: This is generally used for dimensional ... when the profile type is not in the schema ...
    :return:
    """
    if not isinstance(value, (str, StringAttributeValue, ProfileLink, dict)):
        log.warning(f"Validation Warning: Unexpected value {value} of type {type(value)} being used as profileId.")
        return None
    if isinstance(value, dict):
        if key_has_value_in_dict(value, "context", CONTEXTS.PROFILE_LINK):
            value = cast(ProfileLink, construct_attr_class_from_dict(ProfileLink, value))
        # Treat {'value': 'profileId'} as a primitive string ...
        elif len(value.keys()) == 1 and "value" in value and isinstance(value["value"], str):
            value = value["value"]
        else:
            log.warning(f"Validation Warning: Unexpected value {value} of type {type(value)} being used as profileId.")
            return None
    # No casting needed
    if isinstance(value, ProfileLink):
        return value
    string_value = value if isinstance(value, str) else cast(StringAttributeValue, value.value)
    # Cannot cast non string Po1 ids ...
    if not isinstance(string_value, str):
        log.warning(f"Validation Warning: Could not cast value <{value}> into po1 id.")
        return None
    dict_attr_schema = dict(attr_schema)
    modeled_schema_id = extract_specified_linked_schema_id_from_schema_def(dict_attr_schema)
    schema_id_to_use_for_po1_links = modeled_schema_id or default_schema_id
    # Could not extract schema ...
    if not schema_id_to_use_for_po1_links:
        log.warning(f"Casting Warning: Could not determine schema to use when casting <{value}> into po1 id.")
        return None
    warnings.warn(
        f"Casting was used to convert '{value}' into a ProfileLink. Casting will be deprecated soon.",
        DeprecationWarning
    )
    return ProfileLink(profileId=value, schemaId=schema_id_to_use_for_po1_links)  # type: ignore


def get_context_of_inner_type(attr_schema: Union[dict, ProfileAttributeSchema], index=0) -> Optional[str]:
    """
    Get outer type of of inner type at specific index.
    :param attr_schema:
    :param index:
    :return:
    """
    dict_attr_schema = dict(attr_schema)
    context = pydash.get(dict_attr_schema, f'valueType.innerTypes[{index}].outerType', None)
    # return context if context != CONTEXTS.PROFILE_LINK
    #                else pydash.get(attr_schema, f'valueType.innerTypes[{index}].innerTypes[0].outerType', None)
    # the contextOfDimension should be a profile link!
    return context


def cast_value_in_list(value: Union[ProfileAttributeValue, TPrimitive],
                       attr_schema: Union[dict, ProfileAttributeSchema]) -> Union[ProfileLink, ProfileAttributeValue, None]:
    """
        if schema says its a profile link ...
            cast all non profile links ... and warn ...
        if value in list is primitive ...
              cast and warn ...
    """
    modeled_inner_list_type = get_context_of_inner_type(attr_schema, 0)
    profile_link_casting_enabled = (modeled_inner_list_type == CONTEXTS.PROFILE_LINK)
    # Value is supposed to be a profile link ...
    if profile_link_casting_enabled:
        if isinstance(value, ProfileLink):
            return value
        else:
            return cast_profile_id(cast(TProfileLinkAlternatives, value), attr_schema=attr_schema)
    elif is_primitive(value):
        # TODO .. make sure the inner list type is a valid primitive type ...
        return cast_primitive_values(cast(str, value), modeled_inner_list_type)
    else:
        return cast(ProfileAttributeValue, value)


def cast_value_in_dimensional(value: Union[dict, Dimension],
                              attr_schema: Union[dict, ProfileAttributeSchema],
                              context_of_id: Optional[str], context_of_value: Optional[str]) -> Optional[Dimension]:
    """
    if schema says its a profile link ...
        cast all non profile links ... and warn ...
    if value in list is primitive ...
          cast and warn ...
    :param value:
    :param attr_schema:
    :param context_of_id:
    :param context_of_value:
    :return:
    """
    modeled_context_of_id = get_context_of_inner_type(attr_schema, 0)
    modeled_context_of_value = get_context_of_inner_type(attr_schema, 1)

    value = dict(value)
    dimension_id, dimension_value = value.get("dimensionId"), value.get("dimensionValue")

    joined_context_of_id = modeled_context_of_id or context_of_id
    joined_context_of_value = modeled_context_of_value or context_of_value

    # Default context ... if dict ...
    if (
        isinstance(dimension_value, dict) and
        ("context" not in dimension_value) and
        (joined_context_of_value is not None)
    ):
        context_source = "schema" if modeled_context_of_value is not None else "contextOfDimensionValue"
        warnings.warn(
            f"Defaulting context to value provided by {context_source}: {joined_context_of_value}."
            + " Contexts need to be explicitly provided in the future.",
            DeprecationWarning
        )
        dimension_value = pydash.merge({}, dimension_value, {"context": joined_context_of_value})

    # If dimensionValue does not have context ... and [schema|contextOfDimensionValue] don't dictate it ...
    if isinstance(dimension_value, dict) and ('context' not in dimension_value):
        # Treat context free dict as primitive ...?
        if is_primitive(dimension_value.get("value")):
            dimension_value = dimension_value.get("value")
        else:
            log.error(
                f"Casting Error: Can not cast dimension value {value}. No context regarding attribute value type."
            )
            return None

    # Cast Primitives ...
    dimension_value = (
        cast_primitive_values(cast(TPrimitive, dimension_value), joined_context_of_value)
        if is_primitive(dimension_value) else dimension_value
    )
    # Turn Dicts into Profile Attributes Value Types ...
    dimension_value = (
        load_profile_attribute_value_from_dict(dimension_value)
        if isinstance(dimension_value, dict) else dimension_value
    )

    # Validate that the inner types match ...
    if isinstance(dimension_value, BaseProfileAttribute):
        if (joined_context_of_value is not None) and joined_context_of_value != dimension_value.context:
            log.error(
                "Validation Error: There is a type mismatch between."
                + f" Expected {joined_context_of_value} dimensionValue got {dimension_value.context} instead."
            )
            return None
        else:
            # Leave BaseProfileAttribute as is ...
            pass

    cast_dimension_ids = joined_context_of_id == CONTEXTS.PROFILE_LINK
    return Dimension(  # type: ignore
        dimensionId=cast_profile_id(
            cast(TProfileLinkAlternatives, dimension_id), attr_schema=attr_schema
        ) if cast_dimension_ids else dimension_id,
        dimensionValue=dimension_value
    )


def cast_ee_into_simple_attr_value(ee: EntityEvent,
                                   attr_schema: Union[dict, ProfileAttributeSchema]) -> Optional[ProfileAttributeValue]:
    """

    :param ee:
    :param attr_schema:
    :return:
    """
    value = ee.properties
    dict_attr_schema = dict(attr_schema)
    return load_profile_attribute_value_from_dict(
        pydash.merge(
            {},
            value,
            dict(context=pydash.get(dict_attr_schema, 'valueType.outerType', None))
        )
    )


def cast_ee_into_list_attr_value(ee: EntityEvent,
                                 attr_schema: Union[dict, ProfileAttributeSchema]) -> Optional[ListAttributeValue]:
    """

    :param ee:
    :param attr_schema:
    :return:
    """
    value = dict(ee.properties)
    values = [
        cast_value_in_list(item, attr_schema)
        for item in value.get("value", [])
    ]
    first_bad_value = pydash.find_index(values, lambda x: x is None)
    if first_bad_value >= 0:
        bad_value = value.get("value", [])[first_bad_value]
        log.error(f"Validation Error: Invalid item within ListAttrVal @ index {first_bad_value}: {bad_value}")
        return None
    return load_profile_attribute_value_from_dict(pydash.merge(  # type: ignore
        {},
        value,
        dict(
            value=values,
            context=ATTRIBUTE_VALUES.LIST_PROFILE_ATTRIBUTE_VALUE
        )
    ))


def cast_ee_into_dimensional_attr_value(
        ee: EntityEvent, attr_schema: Union[dict, ProfileAttributeSchema]) -> Optional[DimensionalAttributeValue]:
    """
    :param ee:
    :param attr_schema:
    :return:
    """
    value = dict(ee.properties)
    modeled_context_of_id = get_context_of_inner_type(attr_schema, 0)
    modeled_context_of_value = get_context_of_inner_type(attr_schema, 1)
    # Go by what the schema says ... default to what the value says ... enable validation eventually
    context_of_id = modeled_context_of_id or value.get("contextOfDimension")
    context_of_value = modeled_context_of_value or value.get("contextOfDimensionValue")
    values = [
        cast_value_in_dimensional(item, attr_schema, context_of_id, context_of_value)
        for item in value.get("value", [])
    ]
    first_bad_dimension = pydash.find_index(values, lambda x: x is None)
    if first_bad_dimension >= 0:
        bad_value = value.get("value", [])[first_bad_dimension]
        log.error(f"Validation Error: Invalid item in DimensionalAttrVal @ index {first_bad_dimension}: {bad_value}")
        return None
    final_value = pydash.merge(
        {},
        value,
        dict(
            value=values,
            contextOfDimension=context_of_id,
            contextOfDimensionValue=context_of_value,
            context=ATTRIBUTE_VALUES.DIMENSIONAL_PROFILE_ATTRIBUTE_VALUE
        )
    )
    return cast(Optional[DimensionalAttributeValue], load_profile_attribute_value_from_dict(final_value))


def cast_ee_into_profile_rel_attr_value(
        ee: Union[EntityEvent, EntityRelationshipEvent], **kwargs) -> Optional[ProfileRelationshipAttributeValue]:
    """
    :param ee:
    :param kwargs:
    :return:
    """
    value = dict(ee.properties)
    # Do nothing ... ideal route ...
    if (isinstance(ee, EntityEvent) and (
            key_has_value_in_dict(value, "context", ATTRIBUTE_VALUES.PROFILE_REL_PROFILE_ATTRIBUTE_VALUE)
    )):
        return cast(Optional[ProfileRelationshipAttributeValue], load_profile_attribute_value_from_dict(dict(value)))
    else:
        warning_message = (
            "Casting EntityEvent w/ ProfileLink into ProfileRelationshipAttributeValue. Casting will be disabled soon."
        )
        log.warning(warning_message)
        warnings.warn(warning_message, DeprecationWarning)
    if (
        isinstance(ee, EntityEvent) and (
            (isinstance(value, ProfileLink) or key_has_value_in_dict(value, "context", CONTEXTS.PROFILE_LINK))
        )
    ):
        profileLink = construct_attr_class_from_dict(ProfileLink, value)
        if profileLink is None:
            log.error(f"Could not instantiate ProfileLink with supplied data: {value}")
            return None
        return ProfileRelationshipAttributeValue(  # type:ignore
            value=ProfileRelationshipEvent(  # type:ignore
                targetLink=profileLink,
                targetEntityId=profileLink.profileId,
                targetEntityType=profileLink.schemaId,
                **pydash.omit(dict(ee), "properties")
            )
        )
    elif isinstance(ee, EntityRelationshipEvent):
        profileLink = ProfileLink( # type:ignore
            profileId=ee.targetEntityId,
            schemaId=ee.targetEntityType,
        )
        return ProfileRelationshipAttributeValue( # type:ignore
            value=construct_attr_class_from_dict(
                ProfileRelationshipEvent,
                pydash.merge(dict(targetLink=profileLink), dict(ee))
            )
        )
    log.warning(f"Unable to cast ee {ee} into ProfileRelationshipAttributeValue")
    return None


def cast_ee_into_entity_rel_attr_value(
        ee: Union[EntityEvent, EntityRelationshipEvent], **kwargs) -> Optional[EntityRelationshipAttributeValue]:
    """
    :param ee:
    :param kwargs:
    :return:
    """
    value = dict(ee.properties)
    if isinstance(ee, EntityEvent):
        # Return as is ... no casting needed ...
        if key_has_value_in_dict(value, "context", ATTRIBUTE_VALUES.ENTITY_REL_PROFILE_ATTRIBUTE_VALUE):
            return cast(Optional[EntityRelationshipAttributeValue], load_profile_attribute_value_from_dict(value))
        else:
            log.error(f"Casting Error: Could not cast {dict(ee)} into EntityRelationshipAttributeValue")
            return None
    if isinstance(ee, EntityRelationshipEvent):
        warnings.warn(
            f"Could not cast {dict(ee)} into EntityRelationshipAttributeValue",
            DeprecationWarning
        )
        return EntityRelationshipAttributeValue(value=ee)  # type:ignore
    log.error(f"Casting Error: Could not cast {dict(ee)} into EntityRelationshipAttributeValue")
    return None


def cast_ee_into_entity_attr_value(ee: EntityEvent, **kwargs) -> Optional[ProfileAttributeValue]:
    """
    :param ee:
    :param kwargs:
    :return:
    """
    # Try to use the entity event properties as the attribute value (since this is the preferred way)
    try:
        returnVal = load_profile_attribute_value_from_dict(dict(ee.properties))
        if returnVal is not None:
            return returnVal
    except Exception as e:
        pass
    warnings.warn(
        "Casting Entity Event into EntityAttributeValue as is since properties was not valid EE."
        + " In the future Entity Event Attribute Values are likely to be depricated.",
        DeprecationWarning
    )
    return EntityAttributeValue(value=ee)  # type:ignore


def cast_ee_into_attr_value_according_to_schema(
        ee: Union[EntityEvent, EntityRelationshipEvent],
        attr_schema: Union[dict, ProfileAttributeSchema]) -> Optional[ProfileAttributeValue]:
    """
    Casting should only happen prior to saving ee's ... not after retrieving them ...
    :param ee:
    :param attr_schema:
    :return:
    """
    dict_attr_schema = dict(attr_schema)
    attribute_value_type = pydash.get(dict_attr_schema, "valueType.outerType")
    try:
        # TODO ... check if we support the {attribute_value_type}
        # No casting required ...
        # if ee.properties.get("context") in list(ATTRIBUTE_VALUES.values()):
        #     return load_profile_attribute_value_from_dict(ee.properties)
        to_cast = ee
        if ee.properties.get("context") is None and attribute_value_type != ATTRIBUTE_VALUES.ENTITY_ATTRIBUTE_VALUE:
            warning_message = (
                f"Event is missing context / being casted. Defaulting to schema value {attribute_value_type}."
                + " Context must explicitly be provided in the future"
            )
            log.warning(warning_message)
            warnings.warn(warning_message, DeprecationWarning)
            new_properties = pydash.merge({}, dict(ee.properties), {"context": attribute_value_type})
            to_cast = attr.evolve(ee, properties=new_properties)
        casters: Dict[str, Callable] = {
            ATTRIBUTE_VALUES.DIMENSIONAL_PROFILE_ATTRIBUTE_VALUE: cast_ee_into_dimensional_attr_value,
            ATTRIBUTE_VALUES.LIST_PROFILE_ATTRIBUTE_VALUE: cast_ee_into_list_attr_value,
            ATTRIBUTE_VALUES.PROFILE_REL_PROFILE_ATTRIBUTE_VALUE: cast_ee_into_profile_rel_attr_value,
            ATTRIBUTE_VALUES.ENTITY_REL_PROFILE_ATTRIBUTE_VALUE: cast_ee_into_entity_rel_attr_value,
            ATTRIBUTE_VALUES.ENTITY_ATTRIBUTE_VALUE: cast_ee_into_entity_attr_value,
        }
        caster = casters.get(attribute_value_type, cast_ee_into_simple_attr_value)
        log.debug(f"Using casting function {caster} for valueType {attribute_value_type}")
        return caster(to_cast, attr_schema=attr_schema)
    except Exception as e:
        log.error(f"Failed to cast EE into {attribute_value_type}")
        log.error(e)
        return None


# def cast_ee_properties_into_attribute_value(
#   ee: Union[EntityEvent, EntityRelationshipEvent]) -> Optional[ProfileAttributeValue]:
#     if is_primitive(ee.properties):
#         return cast_primitive_values(ee.properties)
#     elif isinstance(ee.properties, dict):
#         # if value is the only key ... and value is primitive ... then cast ...
#         if len(ee.properties) == 1 and "value" in ee.properties and is_primitive(ee.properties.get("value")):
#             return cast_primitive_values(ee.properties)
#         return None
#
#     # EntityRelationshipAttributeValue, EntityRelationshipEvent
#
#     # if it is a ProfileLink ... cast it ...
#     # if it is a Relationship event ... cast it ...

# based on schema ... cast the ee's into the appropriate attribute values!
