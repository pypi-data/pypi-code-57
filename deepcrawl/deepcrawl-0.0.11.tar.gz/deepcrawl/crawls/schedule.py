"""
Schedule
========
"""

from deepcrawl.utils import ImmutableAttributesMixin
from deepcrawl.utils import safe_string_to_datetime

schedule_mutable_attributes = (
    'id',
    'account_id',
    'project_id',
    'schedule_frequency',
    'next_run_time',
)

schedule_immutable_attributes = schedule_mutable_attributes + (
    '_account_href',
    '_project_href',
    '_schedule_frequency_href',
    '_href',
)

schedule_fields = schedule_mutable_attributes + schedule_immutable_attributes


class DeepCrawlSchedule(ImmutableAttributesMixin):
    """
    Schedule class
    """
    __slots__ = schedule_fields

    mutable_attributes = schedule_mutable_attributes

    def __init__(self, account_id, project_id, schedule_data):
        # relations
        self.id = schedule_data.get("_href", "").split("/")[-1]
        self.account_id = account_id
        self.project_id = project_id

        # mutable attributes
        self.schedule_frequency = schedule_data.get("schedule_frequency")
        self.next_run_time = safe_string_to_datetime(schedule_data.get("next_run_time"))

        # immutable attributes
        self._account_href = schedule_data.get("_account_href")
        self._project_href = schedule_data.get("_project_href")
        self._schedule_frequency_href = schedule_data.get("_schedule_frequency_href")
        self._href = schedule_data.get("_href")

        super(DeepCrawlSchedule, self).__init__()

    def __repr__(self):
        return f"[{self.account_id} {self.project_id} {self.id}] {self.next_run_time}"

    def __str__(self):
        return f"[{self.account_id} {self.project_id} {self.id}] {self.next_run_time}"

    @property
    def to_dict_mutable_fields(self):
        """
        :return: dictionary with the mutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in schedule_mutable_attributes}

    @property
    def to_dict_immutable_fields(self):
        """
        :return: dictionary with the immutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in schedule_immutable_attributes}
