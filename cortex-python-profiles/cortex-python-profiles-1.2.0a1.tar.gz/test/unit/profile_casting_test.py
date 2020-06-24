import logging
import unittest
import warnings

import attr
from objectpath import Tree

from cortex_common.constants import ATTRIBUTE_VALUES
from cortex_common.constants import CONTEXTS
from cortex_common.types import Dimension
from cortex_common.types import EntityEvent, EntityRelationshipEvent, ProfileLink, DimensionalAttributeValue, \
    ListAttributeValue, BooleanAttributeValue, ProfileRelationshipAttributeValue, EntityRelationshipAttributeValue, \
    EntityAttributeValue, NumberAttributeValue, StringAttributeValue, ProfileRelationshipEvent
from cortex_profiles.ext.casting import cast_ee_into_attr_value_according_to_schema

base_ee = EntityEvent(event="", entityId="", entityType="")
base_ere = EntityRelationshipEvent(event="", entityId="", entityType="", targetEntityId="", targetEntityType="")
log = logging.getLogger()


schema_value_types = {
    "just_dimensional": {
        "valueType": {
            "outerType": ATTRIBUTE_VALUES.DIMENSIONAL_PROFILE_ATTRIBUTE_VALUE
        }
    },
    "dimensional_with_profile_link": {
        "valueType": {
            "outerType": ATTRIBUTE_VALUES.DIMENSIONAL_PROFILE_ATTRIBUTE_VALUE,
            "innerTypes": [
                dict(ProfileLink.detailed_schema_type("schema/in-schema"))
            ]
        }
    },
    "just_list": {
        "valueType": {
            "outerType": ATTRIBUTE_VALUES.LIST_PROFILE_ATTRIBUTE_VALUE
        }
    },
    "list_with_profile_link": {
        "valueType": {
            "outerType": ATTRIBUTE_VALUES.LIST_PROFILE_ATTRIBUTE_VALUE,
            "innerTypes": [
                dict(ProfileLink.detailed_schema_type("schema/in-schema"))
            ]
        }
    },
    "list_with_inner_type": {
        "valueType": {
            "outerType": ATTRIBUTE_VALUES.LIST_PROFILE_ATTRIBUTE_VALUE,
            "innerTypes": [
                dict(NumberAttributeValue.detailed_schema_type())
            ]
        }
    },
    "dimensional_with_inner_type": {
        "valueType": {
            "outerType": ATTRIBUTE_VALUES.LIST_PROFILE_ATTRIBUTE_VALUE,
            "innerTypes": [
                dict(StringAttributeValue.detailed_schema_type()),
                dict(NumberAttributeValue.detailed_schema_type())
            ]
        }
    },
    "profile_rel":  {
        "valueType": dict(ProfileRelationshipAttributeValue.detailed_schema_type())
    },
}


class TestAgent(unittest.TestCase):

    def test_what_we_expect_to_work_with_warnings(self):
        test_pairs = [
            [
                {
                    "value": [
                        dict(Dimension("1", 2)),
                    ]
                },
                schema_value_types["just_dimensional"]
                ,
                base_ee,
                lambda x: isinstance(x, DimensionalAttributeValue) and x.value[0].dimensionId == "1" and x.value[0].dimensionValue.value == 2,
                "1: just dimensional at outermost level"
            ],
            [
                {
                    "value": [
                        dict(Dimension("1", 2)),
                    ]
                },
                schema_value_types["dimensional_with_profile_link"],
                base_ee,
                lambda x: isinstance(x, DimensionalAttributeValue) and set(list(Tree(dict(x)).execute('$.value.dimensionId.schemaId'))) == set(["schema/in-schema"]),
                "2: casting profile links in dimensional"
            ],
            [
                {
                    "value": [
                        dict(Dimension("1", 2)),
                        dict(Dimension(ProfileLink(profileId="1", schemaId="schema/in-data"), 2)),
                    ]
                },
                schema_value_types["dimensional_with_profile_link"],
                base_ee,
                lambda x: isinstance(x, DimensionalAttributeValue) and set(list(Tree(dict(x)).execute('$.value.dimensionId.schemaId'))) == set(["schema/in-schema", "schema/in-data"]),
                "2a: mixed casting profile links in dimensional with already casted ..."
            ],
            [
                {
                    "value": [ "1", 2, ProfileLink("3", "schema/in-data"), BooleanAttributeValue(True) ]
                },
                schema_value_types["just_list"],
                base_ee,
                lambda x: isinstance(x, ListAttributeValue) and set(list(Tree(dict(x)).execute('$.value.context'))) == set(
                    [CONTEXTS.PROFILE_LINK, ATTRIBUTE_VALUES.NUMBER_PROFILE_ATTRIBUTE_VALUE, ATTRIBUTE_VALUES.STRING_PROFILE_ATTRIBUTE_VALUE, ATTRIBUTE_VALUES.BOOLEAN_PROFILE_ATTRIBUTE_VALUE]
                ),
                "3: mixed list"
            ],
            [
                {
                    "value": [{"value":1}, 1, NumberAttributeValue(1)]
                },
                schema_value_types["just_list"],
                base_ee,
                lambda x: isinstance(x, ListAttributeValue) and sum(list(Tree(dict(x)).execute('$.value.value'))) == 3,
                "3aa: mixed list"
            ],
            [
                {
                    "value": [ "1", "2", ProfileLink("3", "schema/in-data"), dict(ProfileLink("3", "schema/in-data")) ]
                },
                schema_value_types["list_with_profile_link"],
                base_ee,
                lambda x: isinstance(x, ListAttributeValue) and set(list(Tree(dict(x)).execute('$.value.schemaId'))) == set(["schema/in-schema", "schema/in-data"]),
                "3ab: profile links in lists"
            ],
            [
                dict(ProfileLink("3", "schema/in-data")),
                schema_value_types["profile_rel"],
                base_ee,
                lambda x: isinstance(x, ProfileRelationshipAttributeValue) and x.value.targetLink.schemaId == "schema/in-data",
                "4: profile relationships casting"
            ],
            [
                {"a":1},
                schema_value_types["profile_rel"],
                attr.evolve(base_ere, targetEntityType="schema/in-data"),
                lambda x: isinstance(x, ProfileRelationshipAttributeValue) and x.value.targetLink.schemaId == "schema/in-data" and x.value.properties["a"] == 1,
                "4a: profile relationships casting from EntityRelationshipEvent"
            ],
            [
                {},
                {
                    "valueType": dict(EntityRelationshipAttributeValue.detailed_schema_type())
                },
                base_ere,
                lambda x: isinstance(x, EntityRelationshipAttributeValue) and x.value.targetEntityType == "",
                "5: entity relationships casting"
            ],
            [
                {
                    "some": "stuff"
                },
                {
                 "valueType": dict(EntityAttributeValue.detailed_schema_type())
                },
                base_ee,
                lambda x: isinstance(x, EntityAttributeValue) and x.value.properties["some"] == "stuff",
                "6: entity casting"
            ],
            [
                {
                    "value": 2
                },
                {
                    "valueType": dict(NumberAttributeValue.detailed_schema_type())
                },
                base_ee,
                lambda x: isinstance(x, NumberAttributeValue) and x.value == 2,
                "7: Context free primitive"
            ],

        ]
        for [ee_properties, attr_schema, base, validator, test_pair_identifier] in (test_pairs):
            with warnings.catch_warnings(record=True) as ws:
                log.debug(f"Running {test_pair_identifier}")
                casted_value = cast_ee_into_attr_value_according_to_schema(
                    attr.evolve(base, properties=ee_properties),
                    attr_schema=attr_schema
                )
                # try:
                #     log.debug(attr_schema)
                #     log.debug(set(list(Tree(dict(casted_value)).execute('$.value.dimensionId.schemaId'))))
                # except Exception as e:
                #     pass
                log.debug(ws)
                log.debug(casted_value)
                assert validator(casted_value), f"{test_pair_identifier} failed"
                assert len(ws) > 0, "Expecting at least 1 warning ..."

    def test_what_we_expect_to_fail(self):
        test_pairs = [
            [
                {
                    "value": ["1", 2, ProfileLink("3", "schema/in-data")]
                },
                schema_value_types["list_with_profile_link"],
                base_ee,
                "1: casting number in list with links"
            ],
            [
                {
                    "value": [True]
                },
                schema_value_types["list_with_profile_link"],
                base_ee,
                "1a: casting number in list with links"
            ],
            [
                {
                    "value": [{"value": None}]
                },
                schema_value_types["list_with_profile_link"],
                base_ee,
                "1b: casting number in list with links"
            ],
            # Validation not yet enabled ...
            # [
            #     {
            #         "value": ["1", StringAttributeValue("2")]
            #     },
            #     schema_value_types["list_with_inner_type"],
            #     base_ee,
            #     "2: when inner list types dont match"
            # ],
            # [
            #     {
            #         "value": [
            #             Dimension("a", "1"),
            #             Dimension("a", {"value": "2"}),
            #         ]
            #     },
            #     schema_value_types["dimensional_with_inner_type"],
            #     base_ee,
            #     "2: when inner dimensional types dont match"
            # ]
            # EE in EE should fail
            # ERE in EE should fail
            # PL in EE should fail as ENTITY_REL
        ]
        for [ee_properties, attr_schema, base, test_pair_identifier] in (test_pairs):
            with warnings.catch_warnings(record=True) as ws:
                log.debug(f"Running {test_pair_identifier}")
                casted_value = cast_ee_into_attr_value_according_to_schema(
                    attr.evolve(base, properties=ee_properties),
                    attr_schema=attr_schema
                )
                log.debug(ws)
                log.debug(casted_value)
                assert casted_value == None, f"{test_pair_identifier} failed"
                assert len(ws) > 0, "Expecting at least 1 warning ..."

    def tests_we_expect_to_pass_without_warnings(self):
        test_pairs = [
            [
                EntityAttributeValue(value=attr.evolve(base_ee, properties={"a": 1})),
                {
                    "valueType": {
                        "outerType": ATTRIBUTE_VALUES.ENTITY_ATTRIBUTE_VALUE,
                    }
                },
                base_ee,
                lambda x: isinstance(x, EntityAttributeValue) and x.value.properties["a"] == 1,
                "1: EE without casting"
            ],
            [
                EntityRelationshipAttributeValue(value=attr.evolve(base_ere, properties={"a": 1})),
                {
                    "valueType": {
                        "outerType": ATTRIBUTE_VALUES.ENTITY_REL_PROFILE_ATTRIBUTE_VALUE,
                    }
                },
                base_ee,
                lambda x: isinstance(x, EntityRelationshipAttributeValue) and x.value.properties["a"] == 1,
                "2: ERE without casting"
            ],
            [
                ProfileRelationshipAttributeValue(value=ProfileRelationshipEvent(targetLink=ProfileLink("123", ""), **dict(base_ere))),
                {
                    "valueType": {
                        "outerType": ATTRIBUTE_VALUES.PROFILE_REL_PROFILE_ATTRIBUTE_VALUE,
                    }
                },
                base_ee,
                lambda x: isinstance(x, ProfileRelationshipAttributeValue) and x.value.targetLink.profileId == "123",
                "3: PRE without casting"
            ],
        ]
        for [ee_properties, attr_schema, base, validator, test_pair_identifier] in (test_pairs):
            with warnings.catch_warnings(record=True) as ws:
                log.debug(f"Running {test_pair_identifier}")
                casted_value = cast_ee_into_attr_value_according_to_schema(
                    attr.evolve(base, properties=ee_properties),
                    attr_schema=attr_schema
                )
                # try:
                #     log.debug(attr_schema)
                #     log.debug(set(list(Tree(dict(casted_value)).execute('$.value.dimensionId.schemaId'))))
                # except Exception as e:
                #     pass
                log.debug(f"warnings: {ws}")
                log.debug(f"casted value: {casted_value}")
                assert validator(casted_value), f"{test_pair_identifier} failed"
                assert len(ws) == 0, "Expecting no warnings ..."

# Interesting
# [
#     dict(ProfileLink("3", "schema/in-data")),
#     {
#         "valueType": {
#             "outerType": ATTRIBUTE_VALUES.ENTITY_REL_PROFILE_ATTRIBUTE_VALUE,
#         }
#     },
#     base_ere
# ],