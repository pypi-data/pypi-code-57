from typing import Iterable, List, Optional

from pyspark.sql.functions import col, collect_set, struct, dense_rank
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import DoubleType
from pyspark.sql.window import Window


def get_raw_recommendations(actions: DataFrame, min_occurrence: int = 2) -> DataFrame:
    source_actions = actions.alias("source")
    target_actions = actions.alias("target")

    return (
        source_actions.join(target_actions, "customer_id", "inner")
        .filter("source.product_id <> target.product_id")
        .groupBy("source.product_id", "target.product_id")
        .count()
        .filter(col("count") > min_occurrence)
        .selectExpr(
            "source.product_id as source_item_id",
            "target.product_id as recommended_item_id",
            "count as score",
        )
    )


def limit_recommendations(
    recommendations: DataFrame,
    max_recommendations: int,
    partition_by_attrs: Iterable[str],
) -> DataFrame:
    window = Window.partitionBy(*partition_by_attrs).orderBy(
        recommendations.score.cast(DoubleType()).desc()
    )
    return recommendations.withColumn("rank", dense_rank().over(window)).filter(
        f"rank <= {max_recommendations}"
    )


def group_recommendations(
    recommendations: DataFrame, group_by_attrs: Iterable[str],
) -> DataFrame:
    group_by = recommendations.groupBy(*group_by_attrs)
    return group_by.agg(
        collect_set(
            struct(
                recommendations.recommended_item_id,
                recommendations.score.cast(DoubleType()).alias("score"),
            )
        ).alias("recommendations")
    )


def calculate(
    actions: DataFrame,
    min_occurrence: int,
    max_recommendations: Optional[int],
    attributes: Iterable[str],
) -> DataFrame:
    raw_recommendations = get_raw_recommendations(actions, min_occurrence)

    if max_recommendations is None:
        max_recommendations = 200

    dataframe = limit_recommendations(
        raw_recommendations, max_recommendations, attributes
    )
    return group_recommendations(dataframe, attributes)
