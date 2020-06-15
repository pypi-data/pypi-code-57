

from spintop.services.target_bigquery import emit_state, persist_lines_job
from spintop.utils import repr_obj, utcnow_aware

from .base import AbstractSingerTarget, SingerMessagesFactory


class BigQuerySingerTarget(AbstractSingerTarget):
    add_null_to_fields = False

    def __init__(self, project_id, dataset_id, validate_records=True, truncate=False):
        super().__init__()
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.validate_records = validate_records
        self.truncate = truncate

    def send_messages(self, messages_dict):
        state = persist_lines_job(self.project_id, self.dataset_id, messages_dict, truncate=self.truncate, validate_records=self.validate_records)
        emit_state(state)

    def __repr__(self):
        return repr_obj(self, ['project_id', 'dataset_id'])

class BigQueryAnalytics(BigQuerySingerTarget):
    def __init__(self, spintop_api=None, uri=None, database_name=None, env=None):
        super().__init__(project_id=uri, dataset_id=database_name)