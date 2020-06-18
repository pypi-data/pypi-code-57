import datetime
import logging

from tenacity import retry, stop_after_attempt, wait_fixed


class BigqueryChecker:

    def __init__(self, bq_helper, sql_handler):
        self.__bq_helper = bq_helper
        self.__bq_client = bq_helper._bq_client
        self.__sql_handler = sql_handler

    @retry(stop=stop_after_attempt(20), wait=wait_fixed(10))
    def table_has_row_for(self, dataset_name, table_name, message, is_partitioned=True, where=None, check_loaded_at=True, loaded_at_field="loaded_at"):
        is_found = self.message_found(dataset_name, table_name, message, is_partitioned, where, check_loaded_at, loaded_at_field)

        if is_found is False:
            raise TimeoutError("Bigquery table row not found.")

        return is_found

    def table_returns_row_for(self, dataset_name, table_name, message, is_partitioned=True, where=None, check_loaded_at=True, loaded_at_field="loaded_at", max_attempts: int = 20,
                              wait_seconds: float = 10.):
        @retry(stop=stop_after_attempt(max_attempts), wait=wait_fixed(wait_seconds))
        def _table_returns_row_for():
            results = self.get_messages(dataset_name, table_name, message, is_partitioned, where, check_loaded_at, loaded_at_field)

            if len(results) == 0:
                raise TimeoutError("Bigquery table row not found!")

            return results[0]

        return _table_returns_row_for()

    def message_found(self, dataset_name, table_name, message, is_partitioned=True, where=None, check_loaded_at=True, loaded_at_field="loaded_at"):
        results = self.get_messages(dataset_name, table_name, message, is_partitioned, where, check_loaded_at, loaded_at_field)

        return len(results) > 0

    def get_messages(self, dataset_name, table_name, message, is_partitioned=True, where=None, check_loaded_at=True, loaded_at_field="loaded_at"):
        config_fields = {"gcp_project_id": self.__bq_client.project,
                         "dataset_name": dataset_name,
                         "table_name": table_name}

        unique_fields = message.get_unique_fields()
        filter_parts = []
        for field, value in unique_fields.items():
            filter_parts.append("CAST({field:s} AS STRING) = '{value:s}'".format(field=field, value=str(value)))

        loaded_at_check = "{} is not null".format(loaded_at_field) if check_loaded_at else "true"

        params = dict()
        params["filter"] = " AND ".join(filter_parts)
        params["partition_filter"] = self._get_partition_filter_sql(is_partitioned)
        params["where"] = loaded_at_check if where is None or where is False else where + " AND " + loaded_at_check

        query = self.__sql_handler.build_query({**config_fields, **params})

        logging.debug("Query built: {}".format(query))
        logging.debug("Poll for query result has started.")
        results = self.__bq_helper.execute_sync_query(query)
        logging.debug("Poll for query result has ended.")

        return results

    def _get_partition_filter_sql(self, is_partitioned: bool = True) -> str:
        if is_partitioned:
            today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
            return ("(_PARTITIONTIME IS NULL OR _PARTITIONTIME" +
                    " BETWEEN TIMESTAMP_ADD(TIMESTAMP('{partition_day:s}'), INTERVAL -1 DAY)" +
                    " AND TIMESTAMP_ADD(TIMESTAMP('{partition_day:s}'), INTERVAL 1 DAY))").format(
                partition_day=today)
        else:
            return "true"
