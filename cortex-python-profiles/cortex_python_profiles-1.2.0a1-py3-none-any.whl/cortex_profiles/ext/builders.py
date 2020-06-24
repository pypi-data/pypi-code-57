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
import math
import sys
import time
import traceback
from abc import ABC, abstractmethod
from pprint import pformat
from typing import Any, Callable, Union, List, Optional, cast, Tuple, Iterator, Set, Iterable
from urllib.parse import urlparse

import arrow
import attr
import deprecation
import pydash
from cortex.client import Client as CortexClient
from cortex.utils import decode_JWT
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

from cortex_common.types import EntityEvent, ProfileAttributeType, ProfileSchema, ProfileAttributeSchema, \
    ProfileTagSchema, ProfileFacetSchema, ProfileTaxonomySchema, EntityRelationshipEvent, ObservedProfileAttribute
from cortex_common.utils import chunk_iterable, get_logger
from cortex_profiles.build.attributes.utils.etl_utils import turn_attribute_into_entity_event, \
    turn_entity_event_into_attribute
from cortex_profiles.ext import clients
from cortex_profiles.ext.casting import cast_ee_into_attr_value_according_to_schema
from cortex_profiles.ext.rest import ProfilesRestClient

log = get_logger(__name__)

__all__ = [
    "ProfilesBuilder",
    "BulkProfilesBuilder",
    "ProfileSchemaBuilder",
]

TProfileBuildingEventAlternatives = Union[EntityEvent, EntityRelationshipEvent]
TValidatedProfileBuildingEventAlternatives = Tuple[Optional[TProfileBuildingEventAlternatives], Optional[str]]

# def default_db_uri(self) -> str:
#     """
#     # The URI configured ... may be the cluster specific URI ...
#     # The URI users connect to ... may be different ... maybe I shouldn't provide a default for now ... since this
#     # will only work if the db is externalized ...
#     # Also different tenants all use the same db ...
#     :return:
#     """
#     config = self._profiles_client._get("graph/_/config").json()
#     return base64decode_string(config.get(base64encode_string('mongo.graphUri'), ''))


def optional_filter(filter_method: Union[Callable, bool], filter_enabled):
    """
    Helps make filters in list comprehensions, etc toggleable / configurable
    :param filter_method:
    :param filter_enabled:
    :return:
    """
    # if the input is a bool ... return it if the filter is enabled ... other wise ... return true if filter disabled
    if isinstance(filter_method, bool):
        return (not filter_enabled) or filter_method
    return filter_method if filter_enabled else lambda *args, **kwargs: True


def enumerated_chain(*iterables) -> Iterator[Tuple[int, Any]]:
    """
    Chains iterables, but references the index of the iterable an event was yielded from
    :param iterables:
    :return:
    """
    for (i, it) in enumerate(iterables):
        for element in it:
            yield i, element


class AbstractProfilesBuilder(ABC):
    """
    Abstract Class for Profile Builders containing shared functionality.
    """

    def __init__(self, profiles_client: Union[ProfilesRestClient, CortexClient],
                 schema_id: Optional[str] = None, force_casting: bool = False):
        casting = force_casting or schema_id is not None
        if isinstance(profiles_client, CortexClient):
            profiles_client = ProfilesRestClient.from_cortex_client(profiles_client)
        # Refreshing the client to ensure that there is a valid jwt token!
        self._profiles_client: ProfilesRestClient = profiles_client.refresh_client()
        self._schemaId = schema_id
        if self._schemaId is None:
            self._schema = None
        else:
            self._schema = profiles_client.describeSchema(self._schemaId)
        if casting and not self._schema:
            error_msg = "Schema could not be retrieved and casting is enabled. Schema is required for casting."
            log.error(error_msg)
            raise ValueError(f"Failed to Instantiate Profile Builder. {error_msg}")
        self._casting_enabled = casting and self._schema
        if self._schema is not None:
            self._attrs_in_schema = self._schema.attributes_in_schema()
            self._mapping_of_attrs_in_schema = self._schema.mapping_of_attributes_in_schema()

    @abstractmethod
    def with_events(self, *args, **kwargs) -> 'AbstractProfilesBuilder':
        pass

    @abstractmethod
    def with_attributes(self, *args, **kwargs) -> 'AbstractProfilesBuilder':
        pass

    @abstractmethod
    def build(self):
        pass

    def keep_event(self, ee: TProfileBuildingEventAlternatives) -> bool:
        # If casting is disabled ... save everything ...
        if not self._casting_enabled:
            return True
        if ee.entityType == cast(ProfileSchema, self._schema).profileType and ee.event in self._attrs_in_schema:
            return True
        return False

    def cast_event(self,
                   ee: TProfileBuildingEventAlternatives
                   ) -> TValidatedProfileBuildingEventAlternatives:
        if not self._casting_enabled:
            return ee, None
        if not self.keep_event(ee):
            return None, f"Event[{ee.event}] for ProfileType[{ee.entityType}] not found in Schema[{self._schemaId}]"
        attribute_value = cast_ee_into_attr_value_according_to_schema(
            ee=ee, attr_schema=self._mapping_of_attrs_in_schema[ee.event]
        )
        if attribute_value is None:
            return None, f"Failed to cast Entity Event {ee} according to schema {self._schemaId}"
        return ee.with_attribute_value(dict(attribute_value)), None

    def cast_events(self,
                    events: Iterator[TProfileBuildingEventAlternatives]
                    ) -> Iterator[TValidatedProfileBuildingEventAlternatives]:
        return (self.cast_event(ee) for ee in events)

    def stream_valid_events(self,
                            stream_of_casted_events: Iterator[TValidatedProfileBuildingEventAlternatives],
                            remove_invalid_events: bool = True
                            ) -> Iterator[Optional[TProfileBuildingEventAlternatives]]:
        event_is_valid = lambda ee, error : error is None and self.keep_event(ee)
        stream_with_determined_validity = (
            (ee, event_is_valid(ee, error))
            for (ee, error) in stream_of_casted_events
        )
        return (
            ee if validity_of_event else None
            for (ee, validity_of_event) in stream_with_determined_validity
            if optional_filter(validity_of_event is True, remove_invalid_events)
        )

    def stream_errors(self,
                      stream_of_casted_events: Iterator[TValidatedProfileBuildingEventAlternatives]
                      ) -> Iterator[str]:
        return (
            error
            for (_, error) in stream_of_casted_events
            if error is not None
        )

    def _extract_tenant_id(self):
        """
        Extract JWT token from clients the builder was initialized with.
        :return:
        """
        return decode_JWT(
            self._profiles_client._serviceconnector.token, verify=False
        ).get("tenant")


def timed_mongo_bulk_load(collection, *args, precision=6, **kwargs):
    """
    Time mongo bulk load and get errors properly

    :param collection:
    :param args:
    :param precision:
    :param kwargs:
    :return:
    """
    ts = time.time()
    result = None
    exception = None
    exception_details = None
    try:
        result = collection.insert_many(*args, **kwargs)
    except BulkWriteError as bwe:
        exception = sys.exc_info()
        exception_details = pformat(bwe.details)
    te = time.time()
    return (f'%2.{precision}f' % (te - ts), result, exception, exception_details)


class BulkProfilesBuilder(AbstractProfilesBuilder):
    """
    Build Profiles in Bulk, bypassing the graph service.
    """

    def __init__(self, cortex_client: CortexClient, schemaId: Optional[str] = None, db_uri: Optional[str] = None):
        """
        - [ ] Todo ... add param of schemaId:Optional[str] to enable validation against schema before saving events
        :param cortex_client:
        :param db_uri:
        """
        super().__init__(cortex_client, schemaId)
        # Database Stuff (explicitly referencing mongo for now ... will eventually decouple)
        self._db_uri = db_uri
        self._mongo_client: MongoClient = MongoClient(db_uri)
        self._mongo_db = urlparse(db_uri).path[1:]

        # Initializing Builder State ...
        self._events: List[Iterator[TValidatedProfileBuildingEventAlternatives]] = []
        self._attributes: List[Iterator[ProfileAttributeType]] = []
        self._event_casting_args: List[dict] = []
        log.debug("Done Instantiating BulkProfilesBuilder")

    def _get_collection(self, collection):
        return self._mongo_client[self._mongo_db][collection]

    def ee_overrides(self, tenant_id, version):
        """
        What properties need to be set on entity events before they get loaded into the database

        :param tenant_id:
        :param version:
        :return:
        """
        return {
            "_environmentId": "cortex/default",
            "_tenantId": tenant_id,
            "meta": {
                "bulk_inserted_at": version
            }
        }

    def attr_overrides(self, tenant_id, version):
        """
        What properties need to be set on attributes before they get loaded into the database

        :param tenant_id:
        :param version:
        :return:
        """
        return {
            "tenantId": tenant_id,
            "seq": version,
            "environmentId": "cortex/default",
            "createdAt": arrow.utcnow().datetime,
        }

    def with_events(self, event_chunk: Iterator[EntityEvent], *args, **kwargs) -> 'BulkProfilesBuilder':  # type:ignore
        """
        Appends the provided events to the list of events that will be used to build profiles.

        At this level ... we need to know what the attribute type is {inferred, observed, ...}
            ... currently the graph service assumes that entity events lead to observed attributes ...

        # I was using teeing, but it looks like it is not preforming well ...
            # log.debug("Teeing Casted Events into separate streams")
            # event_chunk_for_events, event_chunk_for_invalid_events = tee(casted_events, 2)

        :param event_chunk:
        :param args:
        :param kwargs: params for ee_to_attr_convertor_kwargs ...
        :return:
        """
        log.debug("Casting Events")
        casted_events = (self.cast_event(ee) for ee in event_chunk)
        self._events.append(casted_events)
        self._event_casting_args.append(kwargs)
        return self

    def with_attributes(self, attribute_chunk: Iterator[ProfileAttributeType]) -> 'BulkProfilesBuilder':  # type:ignore
        """
        Converts the provided attributes into a list of events and appends them to the list of events that will be
        used to build profiles.
        :param attribute_chunk:
        :return:
        """
        self._attributes.append(attribute_chunk)
        return self

    def _format_chunk_response(self, items_in_chunk, chunk_index,
                               chunk_insert_duration, chunk_insert_response, chunk_insert_exception,
                               chunk_insert_exception_details, chunk_completion_time, verbose) -> dict:
        """
        Format the response for a bulk load operation appropriately

        :param items_in_chunk:
        :param chunk_index:
        :param chunk_insert_duration:
        :param chunk_insert_response:
        :param chunk_insert_exception:
        :param chunk_insert_exception_details:
        :param chunk_completion_time:
        :param verbose:
        :return:
        """
        response = {
            "chunk_number": chunk_index + 1,
            "total_items_in_chunk": len(items_in_chunk),
            "time_taken_to_insert_chunk": chunk_insert_duration,
            "insert_finished_at": str(chunk_completion_time),
            "exception_occurred": chunk_insert_exception is not None,
        }
        if verbose:
            if chunk_insert_exception is None:
                response["insert_response_inserted_ids"] = [str(y) for y in chunk_insert_response.inserted_ids]
                response["insert_response_acknowledged"] = chunk_insert_response.acknowledged
            # If an exception happened ... add traceback
            else:
                response["exception_traceback"] = traceback.format_exception(
                    *chunk_insert_exception
                )
                response["exception_type"] = chunk_insert_exception[0]
                response["exception_value"] = str(chunk_insert_exception[1])
                response["exception_details"] = str(chunk_insert_exception_details)
        return response

    def bulk_insert_chunk(self, chunk_index:int, document_chunk:List, processing_seq:int, collection:Any,
                          override_func:Callable, chunk_name_in_logs:str, profile_id_field:str,
                          total_items_processed:int, total_processing_time:float,
                          verbose:bool) -> Tuple[Set, dict, int, float]:
        """
        Insert a chunk of documents in bulk into the database

        :param chunk_index:
        :param document_chunk:
        :param processing_seq:
        :param collection:
        :param override_func:
        :param chunk_name_in_logs:
        :param profile_id_field:
        :param total_items_processed:
        :param total_processing_time:
        :param verbose:
        :return:
        """
        loaded_attrs_in_chunk = [
            pydash.merge({}, dict(a), override_func(self._extract_tenant_id(), processing_seq))
            for a in document_chunk
        ]
        (duration, bi_response, bi_exception, bi_exception_details) = timed_mongo_bulk_load(
            collection, loaded_attrs_in_chunk, ordered=False
        )
        resp = self._format_chunk_response(
            items_in_chunk=loaded_attrs_in_chunk, chunk_index=chunk_index, chunk_insert_duration=duration,
            chunk_insert_response=bi_response, chunk_insert_exception=bi_exception,
            chunk_insert_exception_details=bi_exception_details,
            chunk_completion_time=arrow.utcnow().datetime, verbose=verbose
        )
        total_items_processed += resp['total_items_in_chunk']
        total_processing_time += float(resp['time_taken_to_insert_chunk'])
        insert_responses = resp
        a, b, c, d = (
            resp['total_items_in_chunk'], total_items_processed,
            resp['time_taken_to_insert_chunk'], total_processing_time
        )
        log.info(
            f"Inserted {a:,d} {chunk_name_in_logs} in {c} seconds. {b:,d} so far in {d:2.4f} seconds"
        )
        profile_ids_to_flush = set([
            pydash.get(attr, profile_id_field)
            for attr in loaded_attrs_in_chunk
        ])
        return profile_ids_to_flush, insert_responses, total_items_processed, total_processing_time

    def build(self, verbose: bool = False, chunk_size: int = 10_000) -> Tuple[int, List, List]:
        """
        Saves attributes to profiles in bulk, one chunk at a time.
        (Optionally) Saves profile building events in bulk ...
        * It is the responsibility of the invoker to ensure that all chunks were properly inserted and retry as needed.
        * This method does not assert that all the chunks get saved fully;
            It does however return status of the bulk save for each chunk.
        * This method logs progress as chunks are incrementally saved ...

        For reference's sake ...:
        >>> arrow.utcnow().datetime                   # datetime(2020, 2, 17, 16, 37, 25, 350303, tzinfo=tzutc())
        >>> arrow.utcnow().datetime.timestamp()       # 1581957467.937602
        >>> arrow.utcnow().datetime.timestamp()*1000  # 1581957467937.602
        :return: the resulting responses from the bulk output
        """
        # The version of attributes is based on the time this method was invoked
        seq = math.floor(arrow.utcnow().datetime.timestamp() * 1000)

        # Interleave Attribute and Event Chunks so that the iterators tees dont get out of sync ...
        log.debug('Chaining streams')
        attribute_stream = enumerated_chain(*self._attributes)
        event_stream = enumerated_chain(*self._events)

        log.debug('Chunking streams')
        attribute_chunk_stream = chunk_iterable(attribute_stream, chunk_size)
        event_chunk_stream = chunk_iterable(event_stream, chunk_size)

        log.debug('Initializing Counters / Output')
        chunk_num = 0
        attribute_insert_responses, total_attrs_processed, total_attrs_processing_time = [], 0, 0.0
        event_insert_responses, total_events_processed, total_events_processing_time = [], 0, 0.0

        log.debug('Consuming Initial Chunks')
        next_event_chunk = next(event_chunk_stream, None)
        log.debug('Consumed Valid Event Chunk')
        next_attr_chunk = next(attribute_chunk_stream, None)
        log.debug('Consumed Attr Chunk')

        while (next_attr_chunk is not None) or (next_event_chunk is not None):
            log.debug(f"Processing level {chunk_num} of chunks.")
            validated_events_in_chunk = []
            indexes_of_validated_events_in_chunk = []
            profile_ids_to_flush: Set[str] = set([])

            # Insert Each Chunk of Events ...
            if next_event_chunk is not None:
                events_in_chunk = list(next_event_chunk)

                log.debug('Logging Invalid Events in Chunk')
                for error_message in self.stream_errors((x[1] for x in events_in_chunk)):
                    log.warning(error_message)

                validated_events_in_chunk = list(self.stream_valid_events(
                    (x[1] for x in events_in_chunk),
                    remove_invalid_events=False
                ))
                indexes_of_validated_events_in_chunk = [x[0] for x in events_in_chunk]
                only_valid_events = [x for x in validated_events_in_chunk if x is not None]
                if len(only_valid_events) > 0:
                    log.debug('Handling Valid Events in Chunk')
                    (
                        new_profile_ids,
                        new_insert_records,
                        total_events_processed,
                        total_events_processing_time
                    ) = self.bulk_insert_chunk(
                        chunk_index=chunk_num, document_chunk=only_valid_events,
                        override_func=self.ee_overrides, processing_seq=seq,
                        collection=self._get_collection("entity-events"),
                        chunk_name_in_logs="EntityEvents", profile_id_field="entityId",
                        total_items_processed=total_events_processed,
                        total_processing_time=total_events_processing_time,
                        verbose=verbose
                    )
                    profile_ids_to_flush = profile_ids_to_flush.union(new_profile_ids)
                    event_insert_responses.append(new_insert_records)
                else:
                    log.warning(f"No valid events were found in chunk {chunk_num}")

            if validated_events_in_chunk:
                indexes_of_valid_events = [i for (i, ee) in enumerate(validated_events_in_chunk) if ee is not None]
                log.info('Handling Chunk of Attributes extracted from Events')
                attributes_in_events = [
                    turn_entity_event_into_attribute(
                        cast(EntityEvent, validated_events_in_chunk[i]),  # TODO ... is it right to assume this is an EE
                        **pydash.defaults(
                            pydash.get(self._event_casting_args, indexes_of_validated_events_in_chunk[i], {}),
                            {
                                "attributeType": ObservedProfileAttribute
                            }
                        )
                    )
                    for i in indexes_of_valid_events
                ]
                log.debug("Extracted Attribute from Events")
                (
                    new_profile_ids,
                    new_insert_records,
                    total_attrs_processed,
                    total_attrs_processing_time
                ) = self.bulk_insert_chunk(
                    chunk_index=chunk_num, document_chunk=attributes_in_events,
                    override_func=self.attr_overrides, processing_seq=seq,
                    collection=self._get_collection("attributes"),
                    chunk_name_in_logs="Attributes  ", profile_id_field="profileId",
                    total_items_processed=total_attrs_processed,
                    total_processing_time=total_attrs_processing_time,
                    verbose=verbose
                )

            # Insert Each Chunk of attributes
            if next_attr_chunk is not None:
                log.debug('Handling Chunk of Attributes')
                (
                    new_profile_ids,
                    new_insert_records,
                    total_attrs_processed,
                    total_attrs_processing_time
                ) = self.bulk_insert_chunk(
                    chunk_index=chunk_num, document_chunk=[ a for (_, a) in next_attr_chunk],
                    override_func = self.attr_overrides, processing_seq=seq,
                    collection=self._get_collection("attributes"),
                    chunk_name_in_logs="Attributes  ", profile_id_field = "profileId",
                    total_items_processed=total_attrs_processed,
                    total_processing_time=total_attrs_processing_time,
                    verbose=verbose
                )
                profile_ids_to_flush = profile_ids_to_flush.union(new_profile_ids)
                attribute_insert_responses.append(new_insert_records)

            # Flush cache ...
            log.debug(self._profiles_client.delete_cache_for_specific_profiles(list(profile_ids_to_flush)))

            # Move on to next chunks
            log.debug('Consuming Next Chunks')
            next_attr_chunk = next(attribute_chunk_stream, None) if next_attr_chunk is not None else None
            next_event_chunk = next(event_chunk_stream, None) if next_event_chunk is not None else None

            chunk_num += 1
        return (seq, attribute_insert_responses, event_insert_responses)


class ProfilesBuilder(AbstractProfilesBuilder):

    """
    A builder utility to aid in programmatic creation of Cortex Profiles.
    Not meant to be directly instantiated by users of the sdk.
    """

    def __init__(self, profiles_client: ProfilesRestClient, schemaId: Optional[str] = None):
        """
        :param profiles_client:
        :param schemaId:
        """
        super().__init__(profiles_client, schemaId)
        self._events: List[TProfileBuildingEventAlternatives] = []

    def with_events(self, events: List[TProfileBuildingEventAlternatives]) -> 'ProfilesBuilder':  # type:ignore
        """
        Appends the provided events to the list of events that will be used to build profiles.
        :param events:
        :return:
        """
        casted_events = list(self.cast_events(iter(events)))
        errors = self.stream_errors(iter(casted_events))
        for error in errors:
            log.warning(error)
        valid_events = list(self.stream_valid_events(iter(casted_events)))
        self._events.extend(cast(Iterable[Union[EntityEvent, EntityRelationshipEvent]], valid_events))
        return self

    @deprecation.deprecated(deprecated_in='6.0.1b1', details='Use with_events instead.')
    def with_attributes(self, attributes: List[ProfileAttributeType]) -> 'ProfilesBuilder':
        """
        Converts the provided attributes into a list of events and appends them to the list of events that will be
        used to build profiles.
        :param attributes:
        :return:
        """
        self._events.extend([
            turn_attribute_into_entity_event(a, defaultEntityType=self._schemaId)
            for a in attributes
        ])
        return self

    def build(self) -> List[str]:
        """
        Pushes profile building events and returns the response from the building process ...
        :return: the resulting Connection
        """
        # return Profile.get_profile(self._profileId, self._schemaId, self._profiles_client)
        return self._profiles_client.pushEvents(self._events)


class ProfileSchemaBuilder(object):

    """
    A builder utility to aid in programmatic creation of Schemas for Cortex Profiles.
    Not meant to be directly instantiated by users of the sdk.
    """

    def __init__(self, schema:ProfileSchema, profiles_client:ProfilesRestClient):
        """
        Initializes the builder from the profile schema type ...
        :param schema:
        :return:
        """
        self._schema = schema
        self._profiles_client = profiles_client

    def name(self, name:str) -> 'ProfileSchemaBuilder':
        """
        Sets the name of the schema ...
        :param name:
        :return:
        """
        self._schema = attr.evolve(self._schema, name=name)
        return self

    def title(self, title:str) -> 'ProfileSchemaBuilder':
        """
        Sets the title of the schema ...
        :param title:
        :return:
        """
        self._schema = attr.evolve(self._schema, title=title)
        return self

    def profileType(self, profileType:str) -> 'ProfileSchemaBuilder':
        """
        Sets the profileType of the schema ...
        :param profileType:
        :return:
        """
        self._schema = attr.evolve(self._schema, profileType=profileType)
        return self

    def description(self, description:str) -> 'ProfileSchemaBuilder':
        """
        Sets the description of the schema ...
        :param description:
        :return:
        """
        self._schema = attr.evolve(self._schema, description=description)
        return self

    def facets(self, facets:List[ProfileFacetSchema]) -> 'ProfileSchemaBuilder':
        """
        Sets the facets of the schema ...
        :param facets:
        :return:
        """
        self._schema = attr.evolve(self._schema, facets=facets)
        return self

    def taxonomy(self, taxonomy:List[ProfileTaxonomySchema]) -> 'ProfileSchemaBuilder':
        """
        Sets the taxonomy of the schema ...
        :param taxonomy:
        :return:
        """
        self._schema = attr.evolve(self._schema, taxonomy=taxonomy)
        return self

    def attributes(self, attributes:List[ProfileAttributeSchema]) -> 'ProfileSchemaBuilder':
        """
        Sets the attributes of the schema ...
        :param attributes:
        :return:
        """
        self._schema = attr.evolve(self._schema, attributes=attributes)
        return self

    def attributeTags(self, attributeTags:List[ProfileTagSchema]) -> 'ProfileSchemaBuilder':
        """
        Sets the attributeTags of the schema ...
        :param attributeTags:
        :return:
        """
        self._schema = attr.evolve(self._schema, attributeTags=attributeTags)
        return self

    def build(self) -> clients.ProfileSchema:
        """
        Builds and saves a new Profile Schema using the properties configured on the builder
        :return:
        """
        # Push Schema ...
        self._profiles_client.pushSchema(self._schema)
        # Get latest schema ...
        return clients.ProfileSchema.get_schema(
            cast(str, self._schema.name), self._profiles_client)


if __name__ == '__main__':
    pass
    # log.debug(bulk_profile_builder.build(verbose=True))
    # Test to iteratively insert a million attributes!
    # Sum up all the times at the end!