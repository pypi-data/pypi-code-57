import logging
from typing import Any, Dict, Iterable
from decimal import Decimal

from pyspark.sql import Row, DataFrame

logger = logging.getLogger(__name__)


def make_payload(row: Row,) -> Any:
    payload = {}

    payload["items_scores"] = {
        rec.recommended_item_id: Decimal(rec.score) for rec in row.recommendations
    }
    payload["source_item_id"] = row.source_item_id

    return payload


def publish(dataset: DataFrame, dynamodb_table: Any) -> Any:

    logger.info("Iniciando publicação na tabela: %s", dynamodb_table.name)
    for item in dataset.collect():
        payload = make_payload(item)
        dynamodb_table.update_item(
            Key={"source_item_id": payload["source_item_id"]},
            AttributeUpdates={
                "items_scores": {"Value": payload["items_scores"], "Action": "PUT"}
            },
        )
        logger.info("Recomendação atualizada: %s", payload["source_item_id"])
