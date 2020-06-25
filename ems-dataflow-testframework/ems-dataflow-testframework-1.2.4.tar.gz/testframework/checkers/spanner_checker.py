import logging
from collections import Generator
from typing import Dict

from spanner import ems_spanner_client
from tenacity import retry, stop_after_attempt, wait_fixed


class SpannerChecker:
    STOP_AFTER_ATTEMPT_SECS = 15
    WAIT_FIXED = 3

    def __init__(self, project_id: str, instance_id: str, db_name: str) -> None:
        self._client = ems_spanner_client.EmsSpannerClient(project_id, instance_id, db_name)

    def execute_sql(self, query: str) -> Generator:
        logging.info(f"Executing query: {query}")
        return self._client.execute_sql(query)

    def execute_update(self, query: str):
        logging.info(f"Executing update: {query}")
        self._client.execute_update(query)

    def has_row_for(self, table_name: str, conditions: Dict):
        @retry(stop=stop_after_attempt(self.STOP_AFTER_ATTEMPT_SECS), wait=wait_fixed(self.WAIT_FIXED))
        def is_found(query: str):
            if list(self.execute_sql(query))[0][0] == 0:
                raise ValueError("Spanner table row not found.")
            return True

        query = self._compose_query(table_name, conditions)
        return is_found(query)

    @staticmethod
    def _compose_query(table_name, conditions) -> str:
        normalized_conditions = []
        for key, value in conditions.items():
            quoted_value = f"'{value}'" if isinstance(value, str) else value
            normalized_conditions.append(f'{key} = {quoted_value}')
        where = ' AND '.join(normalized_conditions)
        return f'SELECT COUNT(*) FROM {table_name} WHERE {where}'
