"""
   SDC Engine subscription model module
"""
from sqlalchemy import func, case, literal
from sqlalchemy.orm import query_expression
from sqlalchemy.sql.functions import _FunctionGenerator
from sdc_helpers.models.subscription import Subscription as BaseSubscription


class Subscription(BaseSubscription):
    """
       SDC Engine Subscription model class
    """
    # pylint: disable=too-few-public-methods
    __tablename__ = 'subscriptions'

    engine_index = query_expression()
    engine_node = query_expression()

    @classmethod
    def engine_json_search_expression(cls, engine_slug: str) -> _FunctionGenerator:
        """
            JSON_SEARCH SQL function to find the path of a specific engine_slug
            in subscription properties

            args:
                engine_slug (str): The engine slug to search for

            returns:
                function (_FunctionGenerator): The JSON_SEARCH SQL function

        """
        return func.json_search(
            cls.properties,
            'one',
            engine_slug,
            None,
            '$.engines[*].slug'
        )

    @classmethod
    def engine_index_expression(cls, engine_slug: str):
        """
            SQL expression to find the index of an engine slug in properties

            args:
                engine_slug (str): The engine slug to search for

            returns:
                function (_FunctionGenerator): The JSON_SEARCH SQL function

            Example SQL expression:

                REGEXP_REPLACE(
                    JSON_SEARCH(properties, "one", "personalize", NULL, "$.engines[*].slug"),
                    '[^0-9]',
                    ''
                )
        """
        return func.regexp_replace(
            cls.engine_json_search_expression(engine_slug=engine_slug),
            '[^0-9]',
            ''
        )

    @classmethod
    def engine_node_expression(cls, engine_slug: str, entity_key: str) -> _FunctionGenerator:
        """
            SQL expression to get an entity node for an engine slug in properties

            Get the JSON path of the given engine_slug e.g "$.engines[0].slug

            If the the JSON search did not return a path return None
            Else get the path of the entity key being looked for by just replacing
            `slug` by `{entity_key}` e.g "$.engines[0].slug" -> "$.engines[0].campaigns"

            args:
                engine_slug (str): The engine slug to search for
                entity_key (str): The entity key to search for

            returns:
                function (_FunctionGenerator): The JSON_SEARCH SQL function

            Example SQL expression:

                CASE
                    WHEN JSON_SEARCH(
                        properties,
                        "one",
                        "personalize",
                        NULL,
                        "$.engines[*].slug"
                    ) IS NULL THEN NULL
                    ELSE JSON_EXTRACT(
                        properties,
                        JSON_UNQUOTE(
                            REPLACE(
                                JSON_SEARCH(
                                    properties,
                                    "one",
                                    "personalize",
                                    NULL,
                                    "$.engines[*].slug"
                                ),
                                'slug',
                                'campaigns'
                            )
                        )
                    )
                END
        """
        engine_json_search = cls.engine_json_search_expression(engine_slug=engine_slug)

        return case(
            [
                (
                    engine_json_search == literal('NULL'),
                    None
                )
            ],
            else_=func.json_extract(
                Subscription.properties,
                func.json_unquote(
                    func.replace(
                        engine_json_search,
                        'slug',
                        entity_key
                    )
                )
            )
        )
