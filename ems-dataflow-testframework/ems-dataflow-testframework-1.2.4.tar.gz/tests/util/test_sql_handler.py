from datetime import datetime

import pytest

from testframework.util.sql_handler import SqlHandler


@pytest.mark.skip
def test_build_query_returns_properly_formatted_query_as_string():
    partition_filter = datetime.utcnow().replace(microsecond=0)
    params = {"gcp_project_id": "testing",
              "dataset_name": "test_dataset",
              "table_name": "test_table_name",
              "filter": "customer_id = test_customer_id AND campaign_id = test_campaign_id AND message_id = test_message_id",
              "partition_filter": partition_filter,
              "where": "a = b"}

    expected_query = "SELECT * FROM `testing.test_dataset.test_table_name` WHERE (_PARTITIONTIME IS NULL OR _PARTITIONTIME = TIMESTAMP('" + str(
        partition_filter) + "')) AND (customer_id = test_customer_id AND campaign_id = test_campaign_id AND message_id = test_message_id) AND (a = b)"

    sql_handler = SqlHandler()

    assert expected_query == sql_handler.build_query(params)
