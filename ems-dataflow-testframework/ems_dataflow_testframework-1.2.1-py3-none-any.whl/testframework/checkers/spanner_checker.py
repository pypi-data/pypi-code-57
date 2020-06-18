from collections import Generator

from spanner import ems_spanner_client


class SpannerChecker:

    def __init__(self, project_id: str, instance_id: str, db_name: str) -> None:
        self._client = ems_spanner_client.EmsSpannerClient(project_id, instance_id, db_name)

    def execute_sql(self, query: str) -> Generator:
        return self._client.execute_sql(query)
