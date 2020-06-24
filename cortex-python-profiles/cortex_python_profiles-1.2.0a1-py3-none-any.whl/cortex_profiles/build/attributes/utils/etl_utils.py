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

from typing import cast, List, Optional, Type, Union

import arrow
import attr
import pandas as pd

from cortex_common.types import EntityEvent, EntityAttributeValue, DeclaredProfileAttribute, ProfileAttributeType, \
    ProfileAttributeValue, EntityRelationshipAttributeValue, EntityRelationshipEvent
from cortex_common.utils import utc_timestamp
from cortex_profiles.datamodel.dataframes import INSIGHT_COLS, INTERACTIONS_COLS, SESSIONS_COLS, \
    INTERACTION_DURATIONS_COLS
from cortex_profiles.ext.casting import cast_ee_into_attr_value_according_to_schema

__all__ = [
    "turn_attribute_into_entity_event",
    "turn_entity_event_into_attribute",
    "filter_insights_for_profile",
    "filter_interactions_for_profile",
    "filter_sessions_for_profile",
    "filter_events_for_profile",
    "filter_timed_events_for_profile",
    "expand_tag_column",
]


def filter_insights_for_profile(insights_df:pd.DataFrame, profileId:str) -> pd.DataFrame:
    """
    Filter insights for a specific profile
    :param insights_df:
    :param profileId:
    :return:
    """
    return insights_df[insights_df[INSIGHT_COLS.PROFILEID] == profileId]


def filter_interactions_for_profile(interactions_df:pd.DataFrame, profileId:str) -> pd.DataFrame:
    """
    Filter interactions for a specific profile
    :param interactions_df:
    :param profileId:
    :return:
    """
    return interactions_df[interactions_df[INTERACTIONS_COLS.PROFILEID] == profileId]


def filter_sessions_for_profile(sessions_df:pd.DataFrame, profileId:str) -> pd.DataFrame:
    """
    Filter sessions for a specific profile
    :param sessions_df:
    :param profileId:
    :return:
    """
    return sessions_df[sessions_df[SESSIONS_COLS.PROFILEID] == profileId]


def filter_events_for_profile(events:List[EntityEvent], profileId:str) -> List[EntityEvent]:
    """
    Filter events for a specific profile
    :param events:
    :param profileId:
    :return:
    """
    return list(filter(lambda e: e.entityId == profileId, events))


def filter_timed_events_for_profile(events:List[EntityEvent], profileId:str) -> List[EntityEvent]:
    """
    Filter timed events for a specific profile
    :param events:
    :param profileId:
    :return:
    """
    return list(filter(
        lambda e: INTERACTION_DURATIONS_COLS.STARTED_INTERACTION in e.properties and INTERACTION_DURATIONS_COLS.STOPPED_INTERACTION in e.properties,
        filter_events_for_profile(events, profileId)
    ))


def expand_tag_column(df:pd.DataFrame, tag_column_name:str) -> pd.DataFrame:
    """
    Expand a column that contains InsightTags ...

    :param df:
    :param tag_column_name:
    :return:
    """
    return df.assign(
        taggedConceptType=df[tag_column_name].map(lambda x: x.get("concept").get("context")),
        taggedConceptId=df[tag_column_name].map(lambda x: x.get("concept").get("id")),
        taggedConceptTitle=df[tag_column_name].map(lambda x: x.get("concept").get("title")),
        taggedConceptRelationship=df[tag_column_name].map(lambda x: x.get("relationship").get("id")),
        taggedOn=df[tag_column_name].map(lambda x: x.get("tagged"))
    )


def turn_attribute_into_entity_event(attribute: ProfileAttributeType, defaultEntityType:Optional[str]=None) -> EntityEvent:
    """
    Transforms an attribute into an entity event.
        If type(attribute) == ProfileAttribute[EntityAttributeValue] then the Entity Event captured
            within the attribute is used as is ...
        Otherwise ... the attribute is converted into an entity event where ...
            - The attributeKey is used as the event
            - The time of the attributeCreation is used as the eventTime ...
            - The attributeValue is used as the properties as is ...
    :param attribute:
    :return:
    """
    # if isinstance(attribute.attributeValue, (EntityAttributeValue, EntityRelationshipAttributeValue, ProfileRelationshipAttributeValue)):
    #     return attribute.attributeValue.value
    # else:
    return EntityEvent(  # type: ignore
        event=attribute.attributeKey,
        entityId=attribute.profileId,
        entityType=attribute.profileType if attribute.profileType is not None else defaultEntityType,
        eventTime=attribute.createdAt,
        properties=dict(attribute.attributeValue)
    )


def turn_entity_event_into_attribute(
        entityEvent: Union[EntityEvent, EntityRelationshipEvent],
        attributeType: Type[ProfileAttributeType] = DeclaredProfileAttribute,
        attributeValueType: Type[ProfileAttributeValue] = EntityAttributeValue) -> ProfileAttributeType:
    """
    Transforms an attribute into an entity event.
        If type(attribute) == ProfileAttribute[EntityAttributeValue] then the Entity Event captured
            within the attribute is used as is ...
        Otherwise ... the attribute is converted into an entity event where ...
            - The attributeKey is used as the event
            - The time of the attributeCreation is used as the eventTime ...
            - The attributeValue is used as the properties as is ...
    :param attribute:
    :return:
    """
    if not isinstance(entityEvent, (EntityEvent, EntityRelationshipAttributeValue)):
        raise ValueError(f"Can not cast object of type {type(entityEvent)} into attribute")
    context_to_cast_to = attr.fields(attributeValueType).context.default
    value_type_to_cast_to = {
        "valueType": {
            "outerType": context_to_cast_to
        }
    }
    return attributeType(  #type:ignore
        profileId=entityEvent.entityId,
        profileType=entityEvent.entityType,
        attributeKey=entityEvent.event,
        attributeValue=cast_ee_into_attr_value_according_to_schema(entityEvent, value_type_to_cast_to),
        createdAt=(
            str(arrow.get(cast(int, entityEvent.eventTime) / 1000))
            if entityEvent.eventTime is not None else utc_timestamp()
        ),
    )