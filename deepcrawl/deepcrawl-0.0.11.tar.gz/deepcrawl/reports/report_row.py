"""
ReportRow
=========
"""

from deepcrawl.utils import ImmutableAttributesMixin

report_row_extra_fields = (
    "id",
    "account_id",
    "project_id",
    "crawl_id",
    "report_id",
)

report_row_mutable_fields = report_row_extra_fields + (

)

report_row_immutable_fields = (
    "data",
)

report_row_fields = report_row_extra_fields + report_row_mutable_fields + report_row_immutable_fields


class DeepCrawlReportRow(ImmutableAttributesMixin):
    """
    Report row class
    """
    __slots__ = report_row_fields

    mutable_attributes = report_row_mutable_fields

    def __init__(self, account_id, project_id, crawl_id, report_id, row_data: dict):

        # relations
        self.id = row_data.get("_href", "").split("/")[-1]
        self.account_id = account_id
        self.project_id = project_id
        self.crawl_id = crawl_id
        self.report_id = report_id

        # attributes
        self.data = row_data.get('data')

        super(DeepCrawlReportRow, self).__init__()

    @property
    def to_dict_mutable_fields(self):
        """
        :return: dictionary with the mutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in report_row_mutable_fields}

    @property
    def to_dict_immutable_fields(self):
        """
        :return: dictionary with the immutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in report_row_immutable_fields}

